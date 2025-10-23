from rest_framework import serializers
from exercise.models.exercise import GrammarExercise, VocabularyExercise

class GrammarSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrammarExercise
        fields = ['id', 'range', 'topic_name', 'name', 'description', 'image']

class VocabularySerializer(serializers.ModelSerializer):
    class Meta:
        model = VocabularyExercise
        fields = ['id', 'words_count', 'level', 'title', 'image']