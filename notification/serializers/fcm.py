from rest_framework import serializers
from notification.models.fcm import FCMToken

class FcmTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = FCMToken
        fields = ['id', 'token', 'device_type', 'os', 'browser']