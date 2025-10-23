from rest_framework import serializers
from users.models.home import Home
from users.serializers.user_signup import UserSignUpSerializer
from users.serializers.english_serializer import GoalSerializer, UserGoalGetSerializer
from users.models.onboarding import Goal, UserGoal

class HomeSerializer(serializers.ModelSerializer):
    user = UserSignUpSerializer(read_only=True)
    goal = GoalSerializer(read_only=True)
    user_goal = UserGoalGetSerializer(many=True, read_only=True)

    user_goal_ids = serializers.PrimaryKeyRelatedField(
        queryset=UserGoal.objects.all(),
        source='user_goal',
        write_only=True,
        many=True,
        required=True
    )
    goal_ids = serializers.PrimaryKeyRelatedField(
        queryset=Goal.objects.all(),
        source='goal',
        write_only=True,
        required=True
    )
    class Meta:
        model = Home
        fields = ['id','user', 'plan', 'date', 'goal',
                  'user_goal', 'goal_ids', 'user_goal_ids', 'title', 'time']