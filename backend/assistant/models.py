from django.conf import settings
from django.db import models


class ChatMessage(models.Model):
    """One question + one answer. Used both for history and for AI monitoring."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="chat_messages"
    )
    message = models.TextField()
    response = models.TextField()
    response_type = models.CharField(max_length=40, default="general")
    provider = models.CharField(max_length=20, default="fallback")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.user.name}: {self.message[:40]}"
