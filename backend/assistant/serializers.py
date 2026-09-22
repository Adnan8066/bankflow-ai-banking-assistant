from rest_framework import serializers

from .models import ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ("id", "message", "response", "response_type", "provider", "created_at")
        read_only_fields = fields


class ChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=1000, allow_blank=False)

    def validate_message(self, value):
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError("Please type a longer question.")
        return value
