from django.db import models
from common.models import CommonFields


class FCMToken(CommonFields):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="fcm_tokens")
    token = models.TextField(blank=True)
    device_type = models.CharField(max_length=50, null=True, blank=True)
    os = models.CharField(max_length=150, null=True, blank=True)
    browser = models.CharField(max_length=50, null=True, blank=True)
