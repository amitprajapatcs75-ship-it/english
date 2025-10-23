from rest_framework import serializers
from exercise.models.study import *

class SongSerializers(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id', 'title', 'description', 'image', 'tag', 'file', 'uploaded_at']

class BooksSerializers(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ['id', 'title', 'description', 'image', 'tag']

class ArticleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'description', 'image', 'tag']

class InterviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = ['id', 'title', 'description', 'image', 'tag']

class QuestionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id','phrase', 'question', "option_a", "option_b"]

class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = ['id', 'user', 'question', 'user_answer', 'is_correct']