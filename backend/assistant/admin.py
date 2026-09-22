from django.contrib import admin

from .models import ChatMessage


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("user", "message", "response_type", "provider", "created_at")
    list_filter = ("response_type", "provider")
    search_fields = ("message", "response", "user__email", "user__name")
