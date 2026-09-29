from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from users.views import ChangePasswordView, RegisterView, SafeTokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("refresh/", SafeTokenRefreshView.as_view(), name="token_refresh"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
]
