from django.db import models
from users.models.users import User
from djmoney.models.fields import MoneyField
from common.models.common import CommonFields

class BillingFrequency(models.TextChoices):
    MONTHLY = "Monthly", "Monthly"
    ANNUAL = "Annual", "Annual"

class Plan(CommonFields):
    name = models.CharField(max_length=256)
    plan_image = models.FileField(upload_to="plan_images/", null=True, blank=True)
    description = models.TextField()
    price = MoneyField(max_digits=14, decimal_places=2, default_currency="INR")
    retail_price = MoneyField(max_digits=14, decimal_places=2, default_currency="INR", null=True, blank=True)
    storage_capacity = models.PositiveIntegerField()
    billing_frequency = models.CharField(max_length=10, choices=BillingFrequency.choices)
    status = models.BooleanField(default=True)
    time = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_plan')

    def __str__(self):
        return self.name