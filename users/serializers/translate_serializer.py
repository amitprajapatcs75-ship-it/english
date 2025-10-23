from rest_framework import serializers
from users.models.translate import Translate

class TranslateSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    # user = UserSignUpSerializer()
    class Meta:
        model = Translate
        fields = ['id', 'user', 'source_text', 'translated_text']

    def get_user(self, value):
        if value.user:
            return value.user.full_name
        return None