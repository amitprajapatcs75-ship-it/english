from django.db import models
from users.models.event import User
from users.models.onboarding import Goal
from common.models.common import CommonFields
from users.models.onboarding import UserGoal

class Home(CommonFields):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_profile')
    plan = models.CharField(max_length=120)
    date = models.DateField()
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    user_goal = models.ManyToManyField(UserGoal, related_name='user_goal', blank=True)
    title = models.CharField(max_length=120)
    time = models.TimeField(auto_now_add=False)

    def __str__(self):
        return self.title
