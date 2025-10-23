from django.db import models
from users.models.users import User
from common.models.common import CommonFields

class Translate(CommonFields):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    source_text = models.TextField()
    source_language = models.CharField(max_length=15, default='')
    target_language = models.CharField(max_length=15, default='')
    translated_text = models.TextField(null=True, blank=True)