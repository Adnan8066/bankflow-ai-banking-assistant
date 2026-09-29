from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView

from .models import CustomerProfile
from .serializers import (
    ChangePasswordSerializer,
    CustomerProfileSerializer,
    ProfileUpdateSerializer,
    RegisterSerializer,
)


class RegisterView(generics.CreateAPIView):
    """POST /api/auth/register/ - create a demo customer."""

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "message": "Registration successful. Please log in.",
                "user": {"id": user.id, "name": user.name, "email": user.email,
                         "role": user.role},
            },
            status=status.HTTP_201_CREATED,
        )


class ProfileView(APIView):
    """GET /api/profile/ and PUT /api/profile/"""

    permission_classes = [IsAuthenticated]

    def _profile(self, request):
        profile, _ = CustomerProfile.objects.get_or_create(user=request.user)
        return profile

    def get(self, request):
        return Response(CustomerProfileSerializer(self._profile(request)).data)

    def put(self, request):
        profile = self._profile(request)
        serializer = ProfileUpdateSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(CustomerProfileSerializer(profile).data)

    def patch(self, request):
        return self.put(request)


class ChangePasswordView(APIView):
    """POST /api/auth/change-password/"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Password updated. Use the new password the next time you log in."}
        )


class SafeTokenRefreshView(TokenRefreshView):
    """Answer 401 when a refresh token points at an account that no longer exists.

    Without this the token serializer raises DoesNotExist and the client sees a 500.
    """

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return Response(
                {"detail": "This session is no longer valid. Please log in again."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
