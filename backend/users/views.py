from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView

from .models import CustomerProfile
from .serializers import (
    ChangePasswordSerializer,
    CustomerProfileSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    ProfileUpdateSerializer,
    RegisterSerializer,
)

User = get_user_model()


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


class PasswordResetRequestView(APIView):
    """POST /api/auth/password-reset/ - start a password reset.

    BankFlow has no email server, so the response includes the reset link and the
    interface displays it on screen. A real deployment would email the same link
    instead of returning it.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(email__iexact=serializer.validated_data["email"]).first()

        response = {
            "message": (
                "If that email belongs to an account, a reset link has been created. "
                "Check your inbox."
            ),
            "demo_mode": True,
        }
        if user:
            response["reset"] = {
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": default_token_generator.make_token(user),
                "email": user.email,
            }
            response["message"] = (
                "Account found. BankFlow has no email server, so use the reset link shown here."
            )
        return Response(response)


class PasswordResetConfirmView(APIView):
    """POST /api/auth/password-reset/confirm/ - finish the reset with the token."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = None
        try:
            user = User.objects.get(pk=force_str(urlsafe_base64_decode(data["uid"])))
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is None or not default_token_generator.check_token(user, data["token"]):
            return Response(
                {"detail": "This reset link is not valid or has already been used."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(data["new_password"])
        user.save(update_fields=["password"])
        return Response({"message": "Password updated. You can log in with your new password."})
