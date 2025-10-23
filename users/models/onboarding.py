import uuid
from django.db import models
from common.models.common import CommonFields
from django.core.validators import FileExtensionValidator

class UserAim(CommonFields):
    title = models.CharField(max_length=120, unique=True, null=False, blank=False)
    description = models.CharField(max_length=250, null=False, blank=False)

    def __str__(self):
        return self.title

class UserGoal(CommonFields):
    title = models.CharField(max_length=120, unique=True)
    value = models.IntegerField(editable=False, null=True, blank=True)

    def __str__(self):
        return self.title

class ChooseTopics(CommonFields):
    title = models.CharField(max_length=255, null=False, blank=False)
    logo = models.ImageField(
        upload_to='topic_image',
        validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'heic', 'jfif'])
    ],
        null=True, blank=True)

    def __str__(self):
        return self.title

class Goal(CommonFields):
    WEEK_DAYS = (
        ('Sun', 'Sun'),
        ('Mon', 'Mon'),
        ('Tue', 'Tue'),
        ('Wed', 'Wed'),
        ('Thu', 'Thu'),
        ('Fri', 'Fri'),
        ('Sat', 'Sat')
    )
    week = models.CharField(max_length=50, choices=WEEK_DAYS, unique=True)

    def __str__(self):
        return self.week

class SelectLevel(CommonFields):
    level = models.CharField(max_length=120, null=True, blank=True)
    description = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.description

class GoalRelation(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    user_goal = models.ForeignKey(Goal, on_delete=models.CASCADE)

class UserTopicsRelation(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    topics = models.ForeignKey(ChooseTopics, on_delete=models.CASCADE)

class UserGoalRelation(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    user_goal = models.ForeignKey(UserGoal, on_delete=models.CASCADE)

class EnglishLevel(CommonFields):
    ENGLISH_LEVEl = (
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Elementary', 'Elementary'),
        ('Advanced', 'Advanced'),
    )
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    level = models.CharField(max_length=120, choices=ENGLISH_LEVEl)