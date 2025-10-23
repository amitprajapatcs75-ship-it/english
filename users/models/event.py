from django.db import models
from users.models.users import User
from django.utils import timezone
from common.models.common import CommonFields

class Event(CommonFields):
    MONTH_CHOICES = (
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June','June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December')
    )
    name = models.CharField(max_length=200)
    date = models.DateField()
    day = models.CharField(max_length=120)
    time = models.TimeField(default=timezone.now)
    month = models.CharField(max_length=120, choices=MONTH_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_event")

    def __str__(self):
        return self.name