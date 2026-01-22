from rest_framework import serializers

class ChatBotSerializer(serializers.Serializer):
    message = serializers.CharField(required=True)
    user_id = serializers.CharField(required=False)
    app_name = serializers.CharField(required=True)
