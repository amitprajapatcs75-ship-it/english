from rest_framework import serializers
from users.models.event import Event


class EventSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format="%Y-%m-%d",
                                     input_formats=["%Y-%m-%d"])
    time = serializers.TimeField(
        format="%I:%M:%S %p",
        input_formats=["%H:%M:%S", "%I:%M:%S %p"]
    )
    class Meta:
        model = Event
        fields = ['id', 'name', 'date', 'month', 'day', 'time']

    def validate_time(self, value):
        hour = value.hour
        if 1 <= hour < 12:
            self.am_pm = "AM"
        elif 12 <= hour <= 23:
            self.am_pm = "PM"
        else:
            raise serializers.ValidationError("Invalid time hour must be between 1 to 24")
        return value

    def get_time(self, obj):
        return obj.time.strftime(("%I:%M:%S %p"))


