from rest_framework import serializers
from users.models import *
from notification.serializers.fcm import FcmTokenSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('is_superuser', 'last_login', 'is_staff', 'is_active', 'groups', 'user_permissions', 'date_joined',
                   'first_name', 'last_name', 'phone_number', 'onboarding_steps', 'password')


class UserSignUpSerializer(serializers.ModelSerializer):
    password =serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        exclude =('is_superuser','last_login', 'is_staff', 'is_active','groups','user_permissions', 'date_joined', 'first_name', 'last_name')
        extra_kwargs ={
            'fullname': {"fullname": True},
            'email': {"required": True},
            'password': {'write_only': True}
        }
    def validate_email(self, value):
        value=value
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email already exists.")
        return value

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     data['full_name'] = f"{instance.first_name} {instance.last_name}"
    #     return data

class OtpVerificationSerializer(serializers.Serializer):
    email=serializers.EmailField()
    otp=serializers.IntegerField(min_value=100000, max_value=999999,error_messages={
        'min_value': 'otp must be 6 digit number',
        'max_value': 'otp must be 6 digit number',
        'invalid': 'invalid otp ! please enter valid 6 digit number'
    })

    def validate(self, attrs):
        email=attrs.get('email').lower()
        user=User.objects.filter(email=email)
        if user.exists() is True:
            attrs['user'] = user.first()
        else:
            raise serializers.ValidationError({'email': 'email does not exists', 'status': False})
        return attrs

class SignInSerializer(serializers.Serializer):
    email=serializers.CharField()
    password=serializers.CharField()
    fcm = FcmTokenSerializer(required=False)
    user = UserSignUpSerializer(read_only=True)

    def validate(self, attrs):
        email=attrs.get('email')
        user=User.objects.filter(email=email)
        if user.exists() is False:
            raise serializers.ValidationError({"email": "We couldn't find an account associated with this email"})
        attrs['user']=user.first()
        return attrs

class ForgotPasswordSerializer(serializers.Serializer):
    email=serializers.EmailField()

    def validate(self, attrs):
        email=attrs.get('email')
        user=User.objects.filter(email=email)
        if user.exists() is False:
            raise serializers.ValidationError({'email': "We couldn't find an account associated with this email"})
        attrs['user']=user.first()
        return attrs

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField()
    confirm_new_password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        user=User.objects.filter(email=email)
        if user.exists() is False:
            raise serializers.ValidationError({"email": "We couldn't find an account associated with this email"})

        new_password = attrs.get("new_password")
        confirm_new_password = attrs.get("confirm_new_password")

        if new_password != confirm_new_password:
            raise serializers.ValidationError({"confirm_new_password": "confirm_new_password does not match"})

        attrs['user']=user.first()
        return attrs

class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField()
    new_password = serializers.CharField()


class FriendshipSerializer(serializers.ModelSerializer):
    from_user = UserSerializer(read_only=True)
    to_user = UserSerializer(read_only=True)
    class Meta:
        model = Friendship
        fields = ['id', 'from_user', 'to_user', 'status', 'notification']

class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'level', 'quizzes', 'leaderboard']

    def get_user(self, obj):
        return {
            "user_id": obj.user.id,
            "full_name": obj.user.full_name,
            "profile_image": obj.user.profile_image.url if obj.user.profile_image else None
        }

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', "user", "problem"]

class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ['id', "user", "topic", "problem"]

