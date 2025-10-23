from rest_framework import serializers
from users.models.onboarding import *
from users.models.users import User

class UserAimSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAim
        fields = ['id', 'title', 'description']

class UserGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGoal
        fields = ['id', 'value', 'title']

class UserGoalGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGoal
        fields = ['id', 'title']

class ChooseTopicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChooseTopics
        fields = ['id', 'title', 'logo']

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['id', 'week']

class SelectLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectLevel
        fields = ['id', 'level', 'description']

class UserOnboardingSerializer(serializers.ModelSerializer):
    user_aim = UserAimSerializer(read_only=True)
    user_goal = UserGoalSerializer(many=True, read_only=True)
    user_topics = ChooseTopicsSerializer(many=True, read_only=True)
    goal = GoalSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email','full_name', 'user_aim', 'user_goal', 'user_topics',
            'goal','per_day']

class EnglishLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnglishLevel
        fields = ['id', 'user', 'level']
