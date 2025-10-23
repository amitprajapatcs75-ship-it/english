from django.db import models
import uuid


class CommonFields(models.Model):
    id=models.CharField(max_length=255, primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    deleted_at=models.DateTimeField(auto_now_add=True)
    is_deleted=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)

    class Meta:
        abstract = True