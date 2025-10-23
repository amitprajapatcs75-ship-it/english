import uuid
import re
import phonenumbers
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from .user_manager import UserManager
from .onboarding import *
from users.constants import (
    STEP_1,
    STEP_2,
    STEP_3,
    STEP_4,
    STEP_5,
    STEP_6,
    STEP_7,
    STEP_8,
    STEP_9,
    STEP_10,
    STEP_11,
    COMPLETED
)
from django.db.models import (
TextChoices
)
from common.models.common import CommonFields
# from notification.models.notification import Notification

def validate_phone_number(value):
    if not value.startswith('+'):
        value = '+' + value
    try:
        number = phonenumbers.parse(value, None)
        if not phonenumbers.is_possible_number(number):
            raise ValidationError('Phone number is not possible')
        if not phonenumbers.is_valid_number(number):
            raise ValidationError('phone number is not valid')

    except phonenumbers.NumberParseException:
        raise ValidationError("Invalid phone number format. Use +<countrycode><number> (e.g. +919876543210).")

def validate_fullname(name):
    pattern = r"^[A-Za-z\s]+$"
    if not re.match(pattern, name):
        raise ValidationError('fullname contain only alphabets')
    return name


class ONBOARDING_STEPS_CHOICES(TextChoices):
    STEP_1 = STEP_1, "STEP 1"
    STEP_2 = STEP_2, "STEP 2"
    STEP_3 = STEP_3, "STEP 3"
    STEP_4 = STEP_4, "STEP 4"
    STEP_5 = STEP_5, "STEP 5"
    STEP_6 = STEP_6, "STEP 6"
    STEP_7 = STEP_7, "STEP 7"
    STEP_8 = STEP_8, "STEP 8"
    STEP_9 = STEP_9, "STEP 9"
    STEP_10 = STEP_10, "STEP 10"
    STEP_11 = STEP_11, "STEP 11"
    COMPLETED = COMPLETED, "COMPLETED"


class User(AbstractUser):
    id = models.CharField(primary_key=True, default=uuid.uuid4, unique=True, editable=False, max_length=255)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    full_name = models.CharField(max_length=255, null=False, blank=False, validators=[validate_fullname])
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True, validators=[validate_phone_number
    ])
    profile_image = models.ImageField(upload_to='user-profile/', null=True, blank=True)
    onboarding_steps = models.CharField(max_length=3, choices=ONBOARDING_STEPS_CHOICES.choices, null=True, blank=True)

    user_aim = models.OneToOneField(UserAim, on_delete=models.CASCADE, related_name='users_aim', null=True, blank=True)
    user_goal = models.ManyToManyField(UserGoal, related_name='users_goal', through=UserGoalRelation, blank=True)
    user_topics = models.ManyToManyField(ChooseTopics, related_name='users_topics', through=UserTopicsRelation, blank=True)
    goal = models.ManyToManyField(Goal, related_name="goals", through=GoalRelation, blank=True)

    per_day = models.CharField(max_length=120, null=True, blank=True)

    username = None

    REQUIRED_FIELDS = ["first_name", "last_name", "password"]
    USERNAME_FIELD = 'email'
    objects = UserManager()

class Friendship(CommonFields):
    STATUS_CHOICE = (
    ('pending', 'pending'),
    ('accepted', 'accepted'),
    ('rejected', 'rejected'),
    ('cancelled', 'cancelled')
    )
    from_user = models.ForeignKey(User, related_name="friendship_sent", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name="friendship_receive", on_delete=models.CASCADE)
    status = models.CharField(max_length=200, choices=STATUS_CHOICE, default='pending')
    notification = models.ForeignKey("notification.Notification", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return self.status

class UserProfile(CommonFields):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.CharField(max_length=120)
    quizzes = models.CharField(max_length=120)
    leaderboard = models.CharField(max_length=120)

    def __str__(self):
        return self.level

class Report(CommonFields):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.CharField(max_length=250)

class ContactUs(CommonFields):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(ChooseTopics, on_delete=models.CASCADE)
    problem = models.CharField(max_length=250)