from django.urls import path

from .views import (
    AssistantChatView,
    AssistantHistoryView,
    AssistantMonitorView,
    AssistantSuggestionsView,
)

urlpatterns = [
    path("chat/", AssistantChatView.as_view(), name="assistant-chat"),
    path("history/", AssistantHistoryView.as_view(), name="assistant-history"),
    path("suggestions/", AssistantSuggestionsView.as_view(), name="assistant-suggestions"),
    path("monitor/", AssistantMonitorView.as_view(), name="assistant-monitor"),
]
