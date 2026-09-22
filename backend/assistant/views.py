from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import IsBankStaff

from . import ai_service
from .models import ChatMessage
from .serializers import ChatMessageSerializer, ChatRequestSerializer


class AssistantChatView(APIView):
    """POST /api/assistant/chat/ -> ask BankFlow AI a banking question."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChatRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.validated_data["message"]

        result = ai_service.answer(request.user, message)
        chat = ChatMessage.objects.create(
            user=request.user,
            message=message,
            response=result["response"],
            response_type=result.get("type", "general"),
            provider=result.get("provider", "fallback"),
        )
        return Response(
            {
                "id": chat.id,
                "message": chat.message,
                "response": result["response"],
                "type": result.get("type", "general"),
                "intent": result.get("intent"),
                "provider": result.get("provider", "fallback"),
                "data": result.get("data"),
                "created_at": chat.created_at,
            },
            status=status.HTTP_200_OK,
        )


class AssistantHistoryView(APIView):
    """GET /api/assistant/history/ and DELETE /api/assistant/history/"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        messages = ChatMessage.objects.filter(user=request.user)
        return Response({
            "count": messages.count(),
            "results": ChatMessageSerializer(messages, many=True).data,
            "suggestions": ai_service.suggested_questions(),
        })

    def delete(self, request):
        deleted, _ = ChatMessage.objects.filter(user=request.user).delete()
        return Response({"deleted": deleted})


class AssistantSuggestionsView(APIView):
    """GET /api/assistant/suggestions/ - prompt chips for the chat UI."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"suggestions": ai_service.suggested_questions()})


class AssistantMonitorView(APIView):
    """GET /api/assistant/monitor/ - bank employee view of AI activity."""

    permission_classes = [IsBankStaff]

    def get(self, request):
        messages = ChatMessage.objects.select_related("user").order_by("-created_at")
        search = request.query_params.get("search", "").strip()
        if search:
            messages = messages.filter(message__icontains=search) | messages.filter(
                user__name__icontains=search
            )
        stats = {}
        for chat in ChatMessage.objects.all():
            stats[chat.response_type] = stats.get(chat.response_type, 0) + 1
        return Response({
            "total_messages": ChatMessage.objects.count(),
            "providers": {
                "fallback": ChatMessage.objects.filter(provider="fallback").count(),
                "openai": ChatMessage.objects.filter(provider="openai").count(),
            },
            "intent_breakdown": [
                {"type": key, "count": value} for key, value in sorted(
                    stats.items(), key=lambda item: item[1], reverse=True
                )
            ],
            "results": [
                {
                    "id": chat.id,
                    "customer": chat.user.name,
                    "email": chat.user.email,
                    "message": chat.message,
                    "response": chat.response,
                    "type": chat.response_type,
                    "provider": chat.provider,
                    "created_at": chat.created_at,
                }
                for chat in messages[:100]
            ],
        })
