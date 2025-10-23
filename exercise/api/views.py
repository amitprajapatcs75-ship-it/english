from django.db.models import Q
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from exercise.models.exercise import GrammarExercise, VocabularyExercise
from exercise.serializers.exercise_serializers import GrammarSerializer, VocabularySerializer
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from exercise.services.filters import GrammarFilter
from exercise.models.study import *
from exercise.serializers.study_serializers import *

class ExerciseApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, *args, **kwargs):
        grammar_data = GrammarExercise.objects.all().order_by('created_at')
        vocabulary_data = VocabularyExercise.objects.all().order_by('created_at')
        grammar_serializer = GrammarSerializer(grammar_data, many=True)
        vocabulary_serializer = VocabularySerializer(vocabulary_data, many=True)
        return Response({
            'grammar': grammar_serializer.data,
            'vocabulary': vocabulary_serializer.data
        }, status=status.HTTP_200_OK)

class GrammarApiView(generics.ListCreateAPIView):
    queryset = GrammarExercise.objects.all().order_by('-created_at')
    serializer_class = GrammarSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_class = GrammarFilter

class VocabularyApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        query = request.query_params.get('q')
        data = VocabularyExercise.objects.all().order_by('-created_at')
        if query:
            data = data.filter(
                Q(title__icontains=query)|
                Q(words_count__icontains=query)|
                Q(level__icontains=query)
            )
        serializer = VocabularySerializer(data, many=True)
        response_data = {
            "message": "Fetch User Vocabulary Successfully",
            "data": serializer.data
        }
        return Response(response_data, status.HTTP_200_OK)

    def post(self, request):
        serializer = VocabularySerializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"message": "vocabulary create successfully", "status": True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"Error due to {e}")

class SongApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        query = request.query_params.get('q')
        songs = Song.objects.all().order_by('created_at')
        if query:
            songs = songs.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )
        serializer = SongSerializers(songs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = SongSerializers(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'message': 'Song create successfully', 'status': True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"Error occur due to {e}")


class BookApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        query = request.query_params.get('q')
        books = Books.objects.all().order_by('created_at')
        if query:
            books = books.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )
        serializer = BooksSerializers(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = BooksSerializers(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'message': 'books create successfully', 'status': True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"Error occur due to {e}")

class ArticleApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        query = request.query_params.get('q')
        article = Article.objects.all().order_by('created_at')
        if query:
            article = article.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )
        serializer = ArticleSerializers(article, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = ArticleSerializers(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'message': 'article create successfully', 'status': True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"Error occur due to {e}")

class InterviewApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        query = request.query_params.get('q')
        interview = Interview.objects.all().order_by('created_at')
        if query:
            interview = interview.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )
        serializer = InterviewSerializers(interview, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = InterviewSerializers(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'message': 'interview create successfully', 'status': True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"Error occur due to {e}")

class QuestionApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        questions = Question.objects.all()
        serializer = QuestionSerializers(questions, many=True)
        return Response({
            "message": "Questions Fetch successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        question = request.data.get("question_id")
        user_answer = request.data.get("answer")
        if not question or not user_answer:
            return Response({'message': 'please provide question id and answer', "status": False},status=status.HTTP_400_BAD_REQUEST)
        try:
            question = Question.objects.get(id=question)
        except Question.DoesNotExist:
            return Response({"message": "invalid question id", "status": False}, status=status.HTTP_400_BAD_REQUEST)

        is_correct = user_answer == question.correct_option

        data_exist = UserAnswer.objects.filter(user=user, question=question).first()
        if data_exist:
            data_exist.user_answer = user_answer
            data_exist.is_correct = is_correct
            data_exist.save()
        else:
            UserAnswer.objects.create(
                user=user,
                question=question,
                user_answer=user_answer,
                is_correct=is_correct
            )
        total_questions = Question.objects.count()

        return Response({"message": "Answer submitted successfully", "status": True,
                    "total_questions": total_questions,
                    "question": question.question,
                    "correct_answer": question.correct_option,
                    "user_answered": user_answer,
                    "is_correct": is_correct}, status=status.HTTP_200_OK)


