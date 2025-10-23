from rest_framework import serializers
from subscription.models.subscriptions import Plan

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'name', 'plan_image', 'description', 'price', 'retail_price', 'storage_capacity', 'billing_frequency',
                  'status', 'time']