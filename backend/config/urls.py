"""Root URL configuration - every app exposes its own urls.py."""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("users.urls.auth_urls")),
    path("api/", include("users.urls.profile_urls")),
    path("api/", include("banking.urls.customer_urls")),
    path("api/admin/", include("banking.urls.admin_urls")),
    path("api/assistant/", include("assistant.urls")),
]
