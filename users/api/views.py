from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from users.serializers.user_signup import *
from users.services import send_otp_to_mail, send_forget_password_otp
from users.models.users import *
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache
from notification.models.fcm import FCMToken
from django.contrib.auth import login, logout
from users.models.onboarding import UserAim, Goal, UserGoal, ChooseTopics, SelectLevel
from users.serializers.english_serializer import *
from rest_framework.views import APIView
from users.models.event import Event
from users.serializers.event_serializers import EventSerializer
from users.models.home import Home
from users.serializers.home_serializers import HomeSerializer
from users.models.translate import Translate
from users.serializers.translate_serializer import TranslateSerializer
from users.models.onboarding import UserTopicsRelation, GoalRelation
from notification.models.notification import Notification
from notification.push_notification import send_push_notification
from notification.tasks import send_notification_task

# Sign-up/sign-in process
class UserSignUp(generics.CreateAPIView):
    serializer_class = UserSignUpSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = UserSignUpSerializer(data=request.data)
        if data.is_valid(raise_exception=True):
            usr = data.save()
            usr.set_password(data.validated_data['password'])
            usr.is_active = True
            usr.save()
            send_otp_to_mail(username=f'{usr.full_name}', user_email=usr.email.lower())
            response_data = {
                "message": "User Register Successfully",
                "data": data.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

class OtpVerification(generics.CreateAPIView):
    serializer_class = OtpVerificationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = OtpVerificationSerializer(data=request.data)
        if data.is_valid(raise_exception=True):
            user=data.validated_data['user']

            cache_otp =cache.get(f"otp_{user.email}")
            if cache_otp is None:
                send_otp_to_mail(username=f'{user.full_name}', user_email=user.email.lower())
                return Response({'otp': 'your previous opt was expired. we have resend otp please check your mail.', 'status': False},status=status.HTTP_404_NOT_FOUND)

            if cache_otp == data.validated_data['otp']:
                user.is_verified = True
                user.save()
                return Response({'message': 'OTP verify successfully', 'status': True}, status=status.HTTP_200_OK)

            return Response({'message': 'invalid otp please check', 'status': False}, status=status.HTTP_400_BAD_REQUEST)

class ResendOtp(generics.CreateAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')

        if not email:
            return Response({
                'message': 'Email is required', "status": False,
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email).lower()
            if user.is_verified:
                return Response({
                    "message": "User with this email already verified", "status": False
                }, status=status.HTTP_400_BAD_REQUEST)
            send_otp_to_mail(username = f'{user.full_name}', user_email=user.email.lower())
            return Response({"message": "Otp send successfully", "status": True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Exception(f"error occur in {e}")

class SignIn(generics.CreateAPIView):
    serializer_class = SignInSerializer
    permission_classes = [AllowAny]

    @staticmethod
    def fcm_token_handle(user, fcm_data, request):
        pre_sorted_token=FCMToken.objects.select_related("user").filter(user=user)
        if pre_sorted_token.exists():
            pre_sorted_token.delete()

        if fcm_data.get('device_type') is None or fcm_data.get("device_type") == "":
            fcm_data['device_type'] = request.user_agent.device.family

        if fcm_data.get("os") is None or fcm_data.get("os") == "":
            fcm_data['os'] = request.user_agent.os

        if fcm_data.get("browser") is None or fcm_data.get("browser") == "":
            fcm_data['browser'] = request.user_agent.browser.family

        FCMToken.objects.create(
            user=user,
            **fcm_data
        )

    def post(self, request, *args, **kwargs):
        data = SignInSerializer(data=request.data)
        if data.is_valid(raise_exception=True):
            email=data.validated_data['email']
            password=data.validated_data['password']
            try:
                user=User.objects.get(email=email)
                if user.is_verified is False:
                    return Response({'message': 'Please verify email', 'status': False},
                                    status=status.HTTP_400_BAD_REQUEST)
                if user:
                    login(request, user)
                    if data.validated_data.get('fcm') is not None:
                        self.fcm_token_handle(user, data.validated_data.get('fcm'), request)

                if not user.check_password(password):
                    raise serializers.ValidationError({'password': 'Invalid password please try again', 'status': False})

                refresh = RefreshToken.for_user(user)
                return Response({
                    'message': 'Account logged in successfully',
                    'status': True,
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                    'user': UserSignUpSerializer(user).data
                }, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

class ForgotPassword(generics.CreateAPIView):
    serializer_class = ForgotPasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = ForgotPasswordSerializer(data=request.data)
        if data.is_valid(raise_exception=True):
            user=data.validated_data['user']
            send_forget_password_otp(fullname=f"{user.full_name}", user_email=user.email)
            return Response({'message': 'Verification mail sent successfully', 'status': True}, status=status.HTTP_200_OK)

class ValidateForgetPasswordOTP(generics.CreateAPIView):
    serializer_class = OtpVerificationSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = OtpVerificationSerializer(data=request.data)
        if data.is_valid(raise_exception=True):
            user = data.validated_data['user']
            cache_otp = cache.get(f"forgot_otp_{user.email}")
            print("cache_otp", cache_otp)

            if cache_otp == data.validated_data['otp']:
                cache.set(f"forget_verified_{user.email}", True, 60*10)
                return Response({'message': 'otp verify successfully', 'status': True}, status=status.HTTP_200_OK)

            elif cache_otp is None:
                send_forget_password_otp(fullname=f"{user.full_name}", user_email=user.email)
                return Response(
                    {'message': 'OTP has expired resend to your mail please recheck.', 'status': False},
                    status=status.HTTP_404_NOT_FOUND)

            return Response({'message': 'invalid otp please check', 'status': False}, status=status.HTTP_400_BAD_REQUEST)

class ResetPassword(generics.CreateAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = ResetPasswordSerializer(data=request.data)
        if data.is_valid(raise_exception=True):
            user = data.validated_data['user']
            if cache.get(f"forget_verified_{user.email}"):
                user.set_password(data.validated_data['new_password'])
                user.save()
                return Response({'message': "password set successfully", 'status': True}, status=status.HTTP_200_OK
                                )
            return Response({'message': 'password reset fail please verify', 'status': False}, status=status.HTTP_400_BAD_REQUEST)

class ChangePassword(generics.CreateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = ChangePasswordSerializer(data=request.data)
        if data.is_valid(raise_exception=True):
            if request.user.check_password(data.validated_data["current_password"]):
                user=request.user
                user.set_password(data.validated_data['new_password'])
                user.save()
                return Response({"message": "Password change successfully", "status": True}, status=status.HTTP_200_OK)
            return Response({'current_password': "Incorrect password", "status": False}, status=status.HTTP_400_BAD_REQUEST)

class LogoutApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        fcm_tokens = FCMToken.objects.filter(user=request.user)
        fcm_tokens.delete()

        return Response({
            "message": "User logout successful",
            "status": True
        }, status=status.HTTP_200_OK)

# Onboarding process
class UserAimApiView(APIView):

    def get(self, request, *args, **kwargs):
        data = UserAim.objects.all()
        serializer = UserAimSerializer(data, many=True)
        response_data = {
            "message": "Fetch User Aim Successfully",
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

class UserGoalApiView(APIView):

    def get(self, request, *args, **kwargs):
        data = UserGoal.objects.all()
        serializer = UserGoalGetSerializer(data, many=True)
        response_data = {
            "message": "Fetch User Goal Successfully",
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

class ChooseTopicsApiView(APIView):

    def get(self,request, *args, **kwargs):
        query = request.query_params.get('q')
        data = ChooseTopics.objects.all().order_by('-created_at')
        if query:
            data = data.filter(
                Q(title__icontains=query)
            )
        serializer = ChooseTopicsSerializer(data, many=True)
        response_data = {
            "message": "Fetch User Topics Successfully",
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

class GoalApiView(APIView):

    def get(self, request, *args, **kwargs):
        data = Goal.objects.all()
        serializer = GoalSerializer(data, many=True)
        response_data = {
            "message": "Fetch Goal Successfully",
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

class SelectLevelApi(APIView):

    def get(self, request, *args, **kwargs):
        data = SelectLevel.objects.all()
        serializer = SelectLevelSerializer(data, many=True)
        response_data = {
            "message": "Fetch Level Successfully",
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = SelectLevelSerializer(data=request.data)
        if data.is_valid(raise_exception=True):
            data.save()
            response_data = {
                "message": "Create Level Successfully",
                "data": data.data
            }
            return Response(response_data, status=status.HTTP_200_OK)

class UserOnboardingApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            user=request.user
            user_data = UserOnboardingSerializer(user).data
            return Response({'message': 'Success', 'status': True, "user":user_data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"error occur due to {e}")

    def post(self, request, *args, **kwargs):
        user = request.user
        user_aim_id = request.data.get('user_aim')
        user_goals = request.data.get('user_goal')
        goal_ids = request.data.get('goal')
        per_days = request.data.get('per_day')
        user_topics_ids = request.data.get('user_topics')

        try:
            # user aim
            if not user_aim_id:
                return Response({'message': "provide user_aim_id", "status": False}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user.user_aim = UserAim.objects.get(id=user_aim_id)
            except UserAim.DoesNotExist:
                return Response({"message": "Invalid user aim id", "status": False}, status=status.HTTP_400_BAD_REQUEST)

            # user goals
            if not user_goals:
                return Response({'message': "provide user goal id", "status": False}, status=status.HTTP_400_BAD_REQUEST)

            multiple_users_goals = []
            for goal_data in user_goals:
                goal_id = goal_data.get("id")
                value = goal_data.get("value")

                if not goal_id or value is None:
                    return Response({"message": "Please provide goal id and value", "status": False},status=status.HTTP_400_BAD_REQUEST)

                if value > 100:
                    return Response({"message": "The value range in between 1 to 100", "status": False},status=status.HTTP_400_BAD_REQUEST)

                try:
                    goal_obj = UserGoal.objects.get(id=goal_id)
                except UserGoal.DoesNotExist:
                    return Response({"message": f"Invalid user goal id", "status": False},status=status.HTTP_400_BAD_REQUEST)
                goal_obj.value = value
                goal_obj.save()
                multiple_users_goals.append(goal_obj)
            user.user_goal.set(multiple_users_goals)
            user.save()

            # goal
            if not goal_ids:
                return Response({'message': "provide goal ids", "status": False}, status=status.HTTP_400_BAD_REQUEST)

            goals = Goal.objects.filter(id__in=goal_ids)
            if not goals.exists():
                return Response({'message': "goal ids not found", "status": False}, status=status.HTTP_400_BAD_REQUEST)

            user.goal.set(goals)
            user.per_day = per_days
            user.save()

            # user topics
            if not user_topics_ids:
                return Response({'message': "provide user topics ids", "status": False}, status=status.HTTP_400_BAD_REQUEST)

            multiple_topics = []
            for data in user_topics_ids:
                try:
                    topic = ChooseTopics.objects.get(id=data)
                    multiple_topics.append(topic)
                except Exception as e:
                    return Response({"message": f"Invalid user topics id: {e}", "status": False},status=status.HTTP_400_BAD_REQUEST)

            user.user_topics.set(multiple_topics)
            user.save()

            return Response({"message": "Data create successfully", "status": True,
                "user": UserOnboardingSerializer(user).data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"error occur due to {e}"}, status=status.HTTP_400_BAD_REQUEST)

# Home process
class HomeApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        data = Home.objects.all()
        serializer = HomeSerializer(data, many=True)
        response_data = {
            "message": ["Success"],
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = HomeSerializer(data=request.data)
        if data.is_valid(raise_exception=True):
            data.save(user=request.user)
            response_data = {
                "data": data.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

class TranslateApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        data = Translate.objects.all().order_by("-created_at")
        serializer = TranslateSerializer(data, many=True)
        response_data = {
            "message": "Success",
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

#     def post(self, request, *args, **kwargs):
#         serializer = TranslateRequestSerializer(data=request.data)
#         if not serializer.is_valid(raise_exception=True):
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#         text = serializer.validated_data['text']
#         # source_lang = serializer.validated_data['source_lang']
#         target_lang = serializer.validated_data['target_lang']
#         users = request.user
#
#         try:
#             translated = GoogleTranslator(
#                 # source = source_lang,
#                 target=target_lang,
#             ).translate(text)
#
#             Translate.objects.create(
#                 source_text=text,
#                 # source_language=source_lang,
#                 target_language=target_lang,
#                 translated_text=translated,
#                 users=users
#             )
#             return Response({"message":"Translation complete", "status": True, "source_text": text, "translated_text": translated,
#             }, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"status": False,"errors":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EventApiView(APIView):
    serializer = EventSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        data = Event.objects.all().order_by('-created_at')
        serializer = EventSerializer(data, many=True)

        response_data = {
            "message": "Success",
            "data": serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = EventSerializer(data=request.data)
        if data.is_valid(raise_exception=True):
            data.save(user=request.user)

            response_data = {
                "message": "Success",
                "data": data.data
            }

            return Response(response_data, status=status.HTTP_200_OK)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        event_id = request.query_params.get('id')
        if not event_id:
            return Response({'event id': 'Event id is required', 'status': False}, status=status.HTTP_400_BAD_REQUEST)
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({"message": "Event not found!"}, status=status.HTTP_404_NOT_FOUND)

        serializer = EventSerializer(event, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            response_data = {
                "message": "Success",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateGoalApiView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        user = request.user
        goal_ids = request.data.get("goal_id")
        per_day_value = request.data.get('per_day')

        if not goal_ids:
            return Response({'goal id': "please provide goal id", "status": False}, status=status.HTTP_400_BAD_REQUEST)

        if not per_day_value:
            return Response({'per_day': "please provide per day value", "status": False}, status=status.HTTP_400_BAD_REQUEST)

        try:
            goal = Goal.objects.filter(id__in=goal_ids)
            if not goal.exists():
                return Response({'goal': "Invalid goal ids provide", "status": False},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(f"Error occur due to {e}")

        user.per_day = per_day_value
        user.save()
        user.goal.set(goal)
        user.save()
        return Response({"message": "Goal and per_day updated successfully","status": True}, status=status.HTTP_200_OK)


class FriendRequestApiView(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request, *args, **kwargs):
        user = request.user
        query = request.query_params.get('q')
        data = User.objects.all()
        friendship = Friendship.objects.filter(from_user=user, status="accepted")

        if query:
            data.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(full_name__icontains=query)
            )
            print(data)
        serializer = FriendshipSerializer(friendship, many=True)
        return Response({"message": "Friend list get successfully", "status": True,"friends": serializer.data}, status=200)


    def post(self, request, *args, **kwargs):
        to_user_id = request.data.get("to_user_id")

        if not to_user_id:
            return Response({"message": "required to_user id please provide", "status": False}, status=status.HTTP_400_BAD_REQUEST)

        try:
            to_user = User.objects.get(id=to_user_id)
        except User.DoesNotExist:
            return Response({"message": "user does not exist", "status": False}, status=status.HTTP_400_BAD_REQUEST)

        if to_user == request.user:
            return Response({"message": "You cannot add yourself", "status": False}, status=status.HTTP_400_BAD_REQUEST)

        existing = Friendship.objects.filter(
            Q(from_user=request.user, to_user=to_user) |
            Q(from_user=to_user, to_user=request.user)
        ).first()

        if existing:
            return Response({"message": "Friend request already exists", "status": False}, status=status.HTTP_400_BAD_REQUEST)

        notification = Notification.objects.create(
            sender=request.user,
            receiver=to_user,
            status="pending",
            is_read=False,
            message=f"{request.user.full_name} sent you a friend request."
        )

        fcm_token_obj = FCMToken.objects.filter(user=to_user).last()
        if fcm_token_obj:
            try:
                send_notification_task.delay(
                    "New Friend Request",
                    f"{request.user.full_name} sent you a friend request",
                    token=fcm_token_obj.token
                )
            except Exception as e:
                print("FCM send error:", e)

        friendship = Friendship.objects.create(
            from_user=request.user,
            to_user=to_user,
            status="pending",
            notification=notification
        )

        serializer = FriendshipSerializer(friendship)
        return Response({"message": "Friend request sent successfully", "status": True, "data": serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        to_user_id = request.data.get('to_user_id')

        if not to_user_id:
            return Response({"message": "required to user id please provide", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        try:
            to_user = User.objects.get(id=to_user_id)
        except User.DoesNotExist:
            return Response({"message": "User not exist", "status": False}, status=status.HTTP_400_BAD_REQUEST)

        friendship = Friendship.objects.filter(
            Q(from_user=request.user, to_user=to_user) |
            Q(from_user=to_user, to_user=request.user),
            status = "accepted"
        ).first()

        if not friendship:
            return Response({"message": "No friendship found", "status": False}, status=status.HTTP_404_NOT_FOUND)

        friendship.delete()
        return Response({"message": "friend removed successfully", "status": True} ,status=status.HTTP_200_OK)


class ManageFriendRequestApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        action = request.query_params.get('status')

        if not action or action not in ['accept', 'reject', 'cancel']:
            return Response(
                {"message": "Invalid or missing status", "status": False},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            friendship = Friendship.objects.get(id=pk)
        except Friendship.DoesNotExist:
            return Response(
                {"message": "Friend request not found", "status": False},
                status=status.HTTP_404_NOT_FOUND
            )

        status_map = {'accept': 'accepted', 'rejected': 'reject', 'cancel': 'cancelled'}
        friendship.status = status_map[action]
        friendship.save()

        notification = friendship.notification

        if notification:
            notification.status = status_map[action]
            notification.is_read = True
            notification.message = f"{request.user.full_name} {status_map[action]} your friend request."
            notification.sender = request.user
            if action in ['accept', 'reject']:
                notification.receiver = friendship.from_user
            else:
                notification.receiver = friendship.to_user
            notification.save()
        else:
            print("No existing notification found")

        receiver = notification.receiver if notification else (
            friendship.from_user if action in ['accept', 'reject'] else friendship.to_user
        )

        fcm_token_obj = FCMToken.objects.filter(user=receiver).last()
        fcm_token = fcm_token_obj.token if fcm_token_obj else None

        if fcm_token:
            try:
                send_notification_task.delay(
                    title=f"Friend Request {status_map[action].capitalize()}",
                    body=notification.message,
                    token=fcm_token
                )
            except Exception as e:
                print("FCM Error:", e)

        return Response(
            {"message": f"Friend request {status_map[action]}", "status": True},
            status=status.HTTP_200_OK
        )

class UserProfileApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        data = UserProfile.objects.all().order_by('-created_at')
        serializer = UserProfileSerializer(data, many=True)
        return Response({
            "message": "Data fetched successfully",
            "status": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        try:
            user_profile = UserProfile.objects.get(user = request.user)

        except UserProfile.DoesNotExist:
            return Response({
                "message": "User profile does not exists",
                "status": False
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({
                "message": "Profile update successfully",
                "status": True,
                "data": serializer.data
            }, status = status.HTTP_200_OK)
        return Response({
            "message": "Invalid data",
            "status": False,
            "errors": serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)

class ReportApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        data = Report.objects.all().order_by('-created_at')
        serializer = ReportSerializer(data, many=True)
        return Response({
            "message": "data fetched successfully",
            "status": True,
            "data": serializer.data,
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = ReportSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({
                "message": "Report create successfully",
                "status": True,
                "data": serializer.data,
            }, status=status.HTTP_200_OK)


class ContactUsApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        data = ContactUs.objects.all().order_by('-created_at')
        serializer = ContactUsSerializer(data, many=True)
        return Response({
            "message": "data fetched successfully",
            "status": True,
            "data": serializer.data,
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = ContactUsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({
            "message": "ContactUs create successfully",
            "status": True,
            "data": serializer.data,
            }, status = status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        contactus_id = request.query_params.get('id')
        if not contactus_id:
            return Response({'ContactUs id': 'ContactUs id is required', 'status': False}, status=status.HTTP_400_BAD_REQUEST)
        try:
            contact = ContactUs.objects.get(id=contactus_id)
        except Event.DoesNotExist:
            return Response({"message": "Event not found!"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ContactUsSerializer(contact, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            response_data = {
                "message": "Success",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EnglishLevelApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        data = EnglishLevel.objects.all().order_by('-created_at')
        serializer = EnglishLevelSerializer(data, many=True)
        return Response({
            "message": "data fetched successfully",
            "status": True,
            "data": serializer.data,
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = EnglishLevelSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({
                "message": "level create successfully",
                "status": True,
                "data": serializer.data,
            }, status=status.HTTP_200_OK)
