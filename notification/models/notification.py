from django.db import models
from common.models.common import CommonFields
from users.models.users import User

class Notification(CommonFields):
    STATUS = (
    ('pending', 'pending'),
    ('accepted', 'accepted'),
    ('rejected', 'rejected'),
    ('cancelled', 'cancelled')
    )
    sender = models.ForeignKey(User, related_name="notifications_sent", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="notifications_received", on_delete=models.CASCADE)
    status = models.CharField(max_length=120, choices=STATUS, default="pending")
    message = models.CharField(max_length=120, null=True, blank=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        unique_together = ('sender', 'receiver')