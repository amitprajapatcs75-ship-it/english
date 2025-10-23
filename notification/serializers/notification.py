from rest_framework import serializers
from notification.models.notification import Notification
from users.serializers.user_signup import UserSerializer

class NotificationSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'sender', 'receiver', 'status', 'message', 'is_read']