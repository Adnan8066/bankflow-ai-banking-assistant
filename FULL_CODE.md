# BANKFLOW - AI BANKING ASSISTANT

Complete source code for every file in the project, organised headline-wise.
Copy each block into the same relative path inside a `banking_app` folder.

> Demo application only. All banking data is fictional; no real money movement.

---

## 0. INSTALL AND RUN (SUMMARY)

```bash
# backend
cd backend
python -m venv venv
venv\Scripts\activate            # Windows  (source venv/bin/activate on macOS/Linux)
pip install -r requirements.txt
copy .env.example .env           # cp on macOS/Linux
python manage.py makemigrations users banking assistant
python manage.py migrate
python manage.py seed_demo --flush
python manage.py runserver 127.0.0.1:8000

# frontend (new terminal)
cd frontend
npm install
copy .env.example .env           # cp on macOS/Linux
npm run dev                      # http://localhost:5173
```

---

## 1. BACKEND - CONFIGURATION FILES

### backend/requirements.txt

```text
Django==5.2.6
djangorestframework==3.16.1
djangorestframework-simplejwt==5.5.1
django-cors-headers==4.9.0
python-dotenv==1.1.1
psycopg[binary]==3.2.10
```

### backend/.env.example

```text
# Copy this file to .env and change the values before running the project.
DJANGO_SECRET_KEY=change-me-to-a-long-random-string
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# Use sqlite for local development (easiest) ...
DB_ENGINE=sqlite
# ... or switch to PostgreSQL by setting DB_ENGINE=postgres and filling these in
POSTGRES_DB=bankflow
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Optional: plug in a real LLM later. Leave empty to use the rule based fallback.
AI_PROVIDER=fallback
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini
```

### backend/manage.py

```python
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and available on your "
            "PYTHONPATH environment variable? Did you forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
```

### backend/config/__init__.py

```python

```

### backend/config/settings.py

```python
"""
Django settings for the BankFlow - AI Banking Assistant backend.

All secrets are read from the .env file (see .env.example).
"""
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def env(key, default=""):
    """Small helper so every setting can fall back to a safe default."""
    value = os.getenv(key, default)
    return value.strip() if isinstance(value, str) else value


def env_list(key, default=""):
    return [item.strip() for item in env(key, default).split(",") if item.strip()]


SECRET_KEY = env("DJANGO_SECRET_KEY", "insecure-demo-key")
DEBUG = env("DJANGO_DEBUG", "True").lower() == "true"
ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1")


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third party
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    # local apps
    "users",
    "banking",
    "assistant",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ---------------------------------------------------------------- database ---
if env("DB_ENGINE", "sqlite") == "postgres":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env("POSTGRES_DB", "bankflow"),
            "USER": env("POSTGRES_USER", "postgres"),
            "PASSWORD": env("POSTGRES_PASSWORD", "postgres"),
            "HOST": env("POSTGRES_HOST", "localhost"),
            "PORT": env("POSTGRES_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_USER_MODEL = "users.User"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
     "OPTIONS": {"min_length": 8}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ------------------------------------------------------------------- DRF -----
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DATETIME_FORMAT": "%Y-%m-%dT%H:%M:%S%z",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# ------------------------------------------------------------------ CORS -----
CORS_ALLOWED_ORIGINS = env_list(
    "CORS_ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"
)
CORS_ALLOW_CREDENTIALS = True

# --------------------------------------------------------------------- AI ----
AI_PROVIDER = env("AI_PROVIDER", "fallback")          # fallback | openai
OPENAI_API_KEY = env("OPENAI_API_KEY", "")
OPENAI_MODEL = env("OPENAI_MODEL", "gpt-4o-mini")
```

### backend/config/urls.py

```python
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
```

### backend/config/wsgi.py

```python
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()
```

### backend/config/asgi.py

```python
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_asgi_application()
```

## 2. BACKEND - USERS APP (auth, profile, roles)

### backend/users/__init__.py

```python

```

### backend/users/apps.py

```python
from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self):
        from . import signals  # noqa: F401  (registers the profile signal)
```

### backend/users/models.py

```python
"""Custom user model + customer profile.

Email is the login field so the demo can pretend to be a real banking portal.
"""
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Manager that creates users with an email instead of a username."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("An email address is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("role", User.Role.CUSTOMER)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", User.Role.ADMIN)
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = "CUSTOMER", "Customer"
        ADMIN = "ADMIN", "Bank Employee / Admin"

    username = None
    email = models.EmailField("email address", unique=True)
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = UserManager()

    @property
    def is_admin_role(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    def __str__(self):
        return f"{self.name} <{self.email}>"


class CustomerProfile(models.Model):
    """Everything a bank employee would see on the customer 360 page."""

    class EmploymentType(models.TextChoices):
        SALARIED = "SALARIED", "Salaried"
        SELF_EMPLOYED = "SELF_EMPLOYED", "Self Employed"
        STUDENT = "STUDENT", "Student"
        RETIRED = "RETIRED", "Retired"
        OTHER = "OTHER", "Other"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    occupation = models.CharField(max_length=120, blank=True)
    employment_type = models.CharField(
        max_length=20, choices=EmploymentType.choices, default=EmploymentType.SALARIED
    )
    monthly_income = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.name}"
```

### backend/users/signals.py

```python
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CustomerProfile, User


@receiver(post_save, sender=User)
def create_customer_profile(sender, instance, created, **kwargs):
    """Every user always has a profile so the API never returns a partial object."""
    if created:
        CustomerProfile.objects.get_or_create(user=instance)
```

### backend/users/permissions.py

```python
from rest_framework.permissions import BasePermission


class IsBankStaff(BasePermission):
    """Only bank employees / admins can reach the admin API."""

    message = "You do not have permission to access the bank employee area."

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.is_admin_role)
```

### backend/users/serializers.py

```python
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import CustomerProfile, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "name", "email", "role", "date_joined")
        read_only_fields = ("id", "email", "role", "date_joined")


class CustomerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = CustomerProfile
        fields = (
            "id", "user", "phone", "address", "occupation",
            "employment_type", "monthly_income", "created_at",
        )
        read_only_fields = ("id", "user", "created_at")


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """PUT /api/profile/ - the customer may only change name + phone."""

    name = serializers.CharField(max_length=150)

    class Meta:
        model = CustomerProfile
        fields = ("name", "phone", "address", "occupation", "monthly_income")

    def update(self, instance, validated_data):
        name = validated_data.pop("name", None)
        if name:
            instance.user.name = name
            instance.user.save(update_fields=["name"])
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return CustomerProfileSerializer(instance).data


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ("name", "email", "phone", "password", "confirm_password")

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("An account with this email already exists.")
        return value.lower()

    def validate(self, attrs):
        if attrs["password"] != attrs.pop("confirm_password"):
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        phone = validated_data.pop("phone", "")
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)
        profile, _ = CustomerProfile.objects.get_or_create(user=user)
        if phone:
            profile.phone = phone
            profile.save(update_fields=["phone"])
        # Every new demo customer gets a funded demo account + welcome data.
        from banking.services import bootstrap_customer

        bootstrap_customer(user)
        return user

    def to_representation(self, instance):
        return {"id": instance.id, "name": instance.name, "email": instance.email,
                "role": instance.role}
```

### backend/users/views.py

```python
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomerProfile
from .serializers import (
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
```

### backend/users/urls/__init__.py

```python

```

### backend/users/urls/auth_urls.py

```python
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
```

### backend/users/urls/profile_urls.py

```python
from django.urls import path

from users.views import ProfileView

urlpatterns = [
    path("profile/", ProfileView.as_view(), name="profile"),
]
```

### backend/users/admin.py

```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import CustomerProfile, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("email", "name", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("email", "name")
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("name", "first_name", "last_name")}),
        ("Permissions", {"fields": ("role", "is_active", "is_staff", "is_superuser",
                                    "groups", "user_permissions")}),
        ("Dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "name", "role", "password1", "password2"),
        }),
    )


admin.site.register(CustomerProfile)
```

### backend/users/tests.py

```python
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


class AuthFlowTests(APITestCase):
    """Register -> login -> call a protected endpoint."""

    def test_register_creates_customer_with_account(self):
        response = self.client.post(reverse("register"), {
            "name": "Test Customer",
            "email": "test@bankflow.com",
            "phone": "+91 90000 00000",
            "password": "Demo@12345",
            "confirm_password": "Demo@12345",
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email="test@bankflow.com")
        self.assertEqual(user.role, User.Role.CUSTOMER)
        self.assertTrue(user.accounts.exists())

    def test_register_rejects_mismatched_passwords(self):
        response = self.client.post(reverse("register"), {
            "name": "Bad Customer",
            "email": "bad@bankflow.com",
            "password": "Demo@12345",
            "confirm_password": "Other@12345",
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(email="bad@bankflow.com").exists())

    def test_login_returns_jwt_and_unlocks_dashboard(self):
        User.objects.create_user(
            email="login@bankflow.com", password="Demo@12345", name="Login User"
        )
        response = self.client.post(reverse("login"), {
            "email": "login@bankflow.com", "password": "Demo@12345",
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        dashboard = self.client.get("/api/dashboard/")
        self.assertEqual(dashboard.status_code, status.HTTP_200_OK)

    def test_dashboard_requires_authentication(self):
        self.assertEqual(self.client.get("/api/dashboard/").status_code,
                         status.HTTP_401_UNAUTHORIZED)


class ProfileTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="profile@bankflow.com", password="Demo@12345", name="Old Name"
        )
        self.user.profile.phone = "+91 90000 00000"
        self.user.profile.save()
        self.client.force_authenticate(self.user)

    def test_get_and_update_profile(self):
        response = self.client.get("/api/profile/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"]["email"], "profile@bankflow.com")

        updated = self.client.put("/api/profile/", {"name": "New Name",
                                                    "phone": "+91 91111 11111"})
        self.assertEqual(updated.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, "New Name")
        self.assertEqual(self.user.profile.phone, "+91 91111 11111")
```

## 3. BACKEND - BANKING APP (accounts, transactions, loans, notifications)

### backend/banking/__init__.py

```python

```

### backend/banking/apps.py

```python
from django.apps import AppConfig


class BankingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "banking"
```

### backend/banking/models.py

```python
"""Core banking models: Account -> Transaction, plus Loans and Notifications."""
import uuid

from django.conf import settings
from django.db import models
from django.db.models import Sum


def generate_reference(prefix):
    return f"{prefix}{uuid.uuid4().hex[:10].upper()}"


def default_transaction_id():
    return generate_reference("TXN")


def default_loan_id():
    return generate_reference("LOAN")


class Account(models.Model):
    class AccountType(models.TextChoices):
        SAVINGS = "SAVINGS", "Savings Account"
        CURRENT = "CURRENT", "Current Account"
        SALARY = "SALARY", "Salary Account"

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        DORMANT = "DORMANT", "Dormant"
        CLOSED = "CLOSED", "Closed"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="accounts"
    )
    account_number = models.CharField(max_length=20, unique=True)
    account_type = models.CharField(
        max_length=20, choices=AccountType.choices, default=AccountType.SAVINGS
    )
    balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    ifsc_code = models.CharField(max_length=20, default="BANKFL0001234")
    branch = models.CharField(max_length=120, default="BankFlow Demo Branch")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    @property
    def masked_account_number(self):
        return f"XXXX XXXX {self.account_number[-4:]}" if self.account_number else ""

    def __str__(self):
        return f"{self.account_number} ({self.user.name})"


class Transaction(models.Model):
    class Type(models.TextChoices):
        CREDIT = "CREDIT", "Credit"
        DEBIT = "DEBIT", "Debit"

    class Category(models.TextChoices):
        SALARY = "Salary", "Salary"
        FOOD = "Food", "Food"
        SHOPPING = "Shopping", "Shopping"
        TRAVEL = "Travel", "Travel"
        BILLS = "Bills", "Bills"
        ENTERTAINMENT = "Entertainment", "Entertainment"
        TRANSFER = "Transfer", "Transfer"
        OTHER = "Other", "Other"

    class Status(models.TextChoices):
        COMPLETED = "COMPLETED", "Completed"
        PENDING = "PENDING", "Pending"
        FAILED = "FAILED", "Failed"

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="transactions")
    transaction_id = models.CharField(max_length=30, unique=True, default=default_transaction_id)
    date = models.DateTimeField()
    description = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.OTHER)
    transaction_type = models.CharField(max_length=10, choices=Type.choices)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.COMPLETED)
    balance_after = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    class Meta:
        ordering = ["-date"]

    @property
    def signed_amount(self):
        value = float(self.amount)
        return value if self.transaction_type == self.Type.CREDIT else -value

    def __str__(self):
        return f"{self.transaction_id} - {self.description}"


class Loan(models.Model):
    class LoanType(models.TextChoices):
        PERSONAL = "PERSONAL", "Personal Loan"
        HOME = "HOME", "Home Loan"
        EDUCATION = "EDUCATION", "Education Loan"
        VEHICLE = "VEHICLE", "Vehicle Loan"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"
        ACTIVE = "ACTIVE", "Active"
        COMPLETED = "COMPLETED", "Completed"

    class EmploymentType(models.TextChoices):
        SALARIED = "SALARIED", "Salaried"
        SELF_EMPLOYED = "SELF_EMPLOYED", "Self Employed"
        STUDENT = "STUDENT", "Student"
        RETIRED = "RETIRED", "Retired"
        OTHER = "OTHER", "Other"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="loans"
    )
    loan_id = models.CharField(max_length=30, unique=True, default=default_loan_id)
    loan_type = models.CharField(max_length=20, choices=LoanType.choices)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=9.5)
    tenure_months = models.PositiveIntegerField(default=12)
    emi = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    remaining_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.PENDING)
    purpose = models.CharField(max_length=255, blank=True)
    monthly_income = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    employment_type = models.CharField(
        max_length=20, choices=EmploymentType.choices, default=EmploymentType.SALARIED
    )
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-applied_at"]

    @property
    def paid_amount(self):
        return float(self.amount) - float(self.remaining_amount)

    @property
    def progress_percent(self):
        if not self.amount:
            return 0
        return round(self.paid_amount / float(self.amount) * 100, 1)

    def save(self, *args, **kwargs):
        if self.remaining_amount in (None, 0) and self.status != self.Status.COMPLETED:
            self.remaining_amount = self.amount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.loan_id} - {self.get_loan_type_display()}"


class Notification(models.Model):
    class NotificationType(models.TextChoices):
        TRANSACTION = "TRANSACTION", "Transaction"
        LOAN = "LOAN", "Loan"
        SECURITY = "SECURITY", "Security"
        SUMMARY = "SUMMARY", "Summary"
        SYSTEM = "SYSTEM", "System"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications"
    )
    title = models.CharField(max_length=150)
    message = models.TextField()
    notification_type = models.CharField(
        max_length=20, choices=NotificationType.choices, default=NotificationType.SYSTEM
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @staticmethod
    def unread_count(user):
        return Notification.objects.filter(user=user, is_read=False).count()


def account_balance(user):
    """Total balance across every active account of a customer."""
    total = Account.objects.filter(user=user, status=Account.Status.ACTIVE).aggregate(
        total=Sum("balance")
    )["total"]
    return float(total or 0)
```

### backend/banking/services.py

```python
"""Business logic for BankFlow.

Views stay thin; every calculation that is reused by the dashboard, the EMI
calculator and the AI assistant lives here.
"""
import random
from datetime import date, datetime, timedelta

from django.utils import timezone

from .models import Account, Loan, Notification, Transaction, account_balance

CATEGORY_COLORS = {
    "Salary": "#16a34a",
    "Food": "#f97316",
    "Shopping": "#8b5cf6",
    "Travel": "#0ea5e9",
    "Bills": "#ef4444",
    "Entertainment": "#ec4899",
    "Transfer": "#64748b",
    "Other": "#94a3b8",
}


# ------------------------------------------------------------------ helpers --
def to_float(value):
    return float(value or 0)


def aware(value):
    """Turn a `date` or naive `datetime` into a timezone-aware datetime."""
    if isinstance(value, datetime):
        return value if timezone.is_aware(value) else timezone.make_aware(value)
    return timezone.make_aware(datetime.combine(value, datetime.min.time()))


def format_inr(value):
    """Format a number the Indian way: 18450 -> '18,450'."""
    value = float(value or 0)
    whole = f"{abs(value):,.0f}"
    return f"{'-' if value < 0 else ''}{whole}"


def calculate_emi(principal, annual_rate, months):
    """Standard reducing-balance EMI formula."""
    principal = float(principal)
    annual_rate = float(annual_rate)
    months = int(months) or 1
    monthly_rate = annual_rate / 12 / 100
    if monthly_rate == 0:
        emi = principal / months
    else:
        factor = (1 + monthly_rate) ** months
        emi = principal * monthly_rate * factor / (factor - 1)
    total_payment = emi * months
    return {
        "monthly_emi": round(emi, 2),
        "total_interest": round(total_payment - principal, 2),
        "total_payment": round(total_payment, 2),
        "principal": round(principal, 2),
        "tenure_months": months,
        "interest_rate": annual_rate,
    }


def month_bounds(reference=None):
    reference = reference or timezone.localdate()
    start = reference.replace(day=1)
    next_month = (start + timedelta(days=32)).replace(day=1)
    return start, next_month


def previous_month_bounds(reference=None):
    start, _ = month_bounds(reference)
    last_day_previous = start - timedelta(days=1)
    return month_bounds(last_day_previous)


def customer_transactions(user):
    return Transaction.objects.filter(account__user=user)


def period_totals(user, start, end):
    qs = customer_transactions(user).filter(date__gte=aware(start), date__lt=aware(end),
                                            status=Transaction.Status.COMPLETED)
    income = sum(to_float(t.amount) for t in qs if t.transaction_type == Transaction.Type.CREDIT)
    expense = sum(to_float(t.amount) for t in qs if t.transaction_type == Transaction.Type.DEBIT)
    return {"income": round(income, 2), "expense": round(expense, 2),
            "count": qs.count()}


# ---------------------------------------------------- dashboard + analytics --
def get_account(user):
    return Account.objects.filter(user=user).order_by("created_at").first()


def get_dashboard(user):
    """Everything the customer dashboard and the AI need in one place."""
    start, end = month_bounds()
    prev_start, prev_end = previous_month_bounds()
    current = period_totals(user, start, end)
    previous = period_totals(user, prev_start, prev_end)

    categories = category_breakdown(user, start, end)
    loans = Loan.objects.filter(user=user)
    active_loans = loans.filter(status__in=[Loan.Status.ACTIVE, Loan.Status.APPROVED])

    return {
        "balance": round(account_balance(user), 2),
        "monthly_income": current["income"],
        "monthly_expenses": current["expense"],
        "monthly_savings": round(current["income"] - current["expense"], 2),
        "previous_month_income": previous["income"],
        "previous_month_expenses": previous["expense"],
        "expense_change_percent": percent_change(previous["expense"], current["expense"]),
        "transaction_count": current["count"],
        "active_loans": active_loans.count(),
        "total_loans": loans.count(),
        "total_outstanding": round(sum(to_float(l.remaining_amount) for l in active_loans), 2),
        "monthly_emi_total": round(sum(to_float(l.emi) for l in active_loans), 2),
        "unread_notifications": Notification.unread_count(user),
        "top_category": categories[0] if categories else None,
        "spending_categories": categories,
        "monthly_trend": monthly_trend(user, months=6),
        "loan_status_breakdown": loan_status_breakdown(user),
        "recent_transactions": [
            {
                "id": t.id,
                "transaction_id": t.transaction_id,
                "date": t.date.isoformat(),
                "description": t.description,
                "category": t.category,
                "transaction_type": t.transaction_type,
                "amount": to_float(t.amount),
                "status": t.status,
            }
            for t in customer_transactions(user).select_related("account")[:5]
        ],
    }


def percent_change(old, new):
    old = float(old or 0)
    new = float(new or 0)
    if old == 0:
        return 0 if new == 0 else 100.0
    return round((new - old) / old * 100, 1)


def category_breakdown(user, start=None, end=None):
    start = start or month_bounds()[0]
    end = end or month_bounds()[1]
    qs = customer_transactions(user).filter(
        transaction_type=Transaction.Type.DEBIT,
        status=Transaction.Status.COMPLETED,
        date__gte=aware(start),
        date__lt=aware(end),
    )
    totals = {}
    for txn in qs:
        totals[txn.category] = totals.get(txn.category, 0) + to_float(txn.amount)
    data = [
        {"category": category, "amount": round(amount, 2),
         "color": CATEGORY_COLORS.get(category, "#94a3b8")}
        for category, amount in totals.items()
    ]
    return sorted(data, key=lambda item: item["amount"], reverse=True)


def category_total(user, category_names, start=None, end=None):
    breakdown = category_breakdown(user, start, end)
    wanted = [name.lower() for name in category_names]
    return round(
        sum(item["amount"] for item in breakdown if item["category"].lower() in wanted), 2
    )


def big_category_names():
    """All categories a customer can ask the assistant about."""
    return [category for category, _ in Transaction.Category.choices]


def monthly_trend(user, months=6):
    today = timezone.localdate()
    series = []
    cursor = today.replace(day=1)
    for _ in range(months):
        start, end = month_bounds(cursor)
        totals = period_totals(user, start, end)
        series.append({
            "month": start.strftime("%b %Y"),
            "short_month": start.strftime("%b"),
            "income": totals["income"],
            "expense": totals["expense"],
            "savings": round(totals["income"] - totals["expense"], 2),
            "transactions": totals["count"],
        })
        cursor = (start - timedelta(days=1)).replace(day=1)
    return list(reversed(series))


def loan_status_breakdown(user=None):
    qs = Loan.objects.all() if user is None else Loan.objects.filter(user=user)
    counts = {}
    for loan in qs:
        counts[loan.status] = counts.get(loan.status, 0) + 1
    return [{"status": status, "label": label, "count": counts.get(status, 0)}
            for status, label in Loan.Status.choices]


def biggest_expense(user, start=None, end=None):
    start = start or month_bounds()[0]
    end = end or month_bounds()[1]
    txn = customer_transactions(user).filter(
        transaction_type=Transaction.Type.DEBIT,
        status=Transaction.Status.COMPLETED,
        date__gte=aware(start),
        date__lt=aware(end),
    ).order_by("-amount").first()
    if not txn:
        return None
    return {
        "description": txn.description,
        "category": txn.category,
        "amount": to_float(txn.amount),
        "date": txn.date.isoformat(),
        "transaction_id": txn.transaction_id,
    }


# --------------------------------------------------------------- bootstrapping -
def random_account_number():
    return "5" + "".join(random.choices("0123456789", k=11))


def record_transaction(account, *, amount, description, category,
                       transaction_type, when=None, status="COMPLETED"):
    """Create a transaction and keep the account balance consistent."""
    when = when or timezone.now()
    amount = float(amount)
    if transaction_type == Transaction.Type.CREDIT:
        account.balance = to_float(account.balance) + amount
    else:
        account.balance = to_float(account.balance) - amount
    account.save(update_fields=["balance"])
    return Transaction.objects.create(
        account=account,
        date=when,
        description=description,
        category=category,
        transaction_type=transaction_type,
        amount=amount,
        status=status,
        balance_after=account.balance,
    )


def bootstrap_customer(user):
    """New demo customers immediately get an account + welcome notification."""
    account, _ = Account.objects.get_or_create(
        user=user,
        defaults={"account_number": random_account_number(), "balance": 0},
    )
    Notification.objects.get_or_create(
        user=user,
        title="Welcome to BankFlow",
        defaults={
            "message": (
                "Your demo savings account is ready. Explore the dashboard, the AI "
                "assistant and the EMI calculator with completely fictional data."
            ),
            "notification_type": Notification.NotificationType.SYSTEM,
        },
    )
    return account


def month_start_offset(offset=0):
    """First day of the current month, minus `offset` months."""
    start = timezone.localdate().replace(day=1)
    for _ in range(offset):
        start = (start - timedelta(days=1)).replace(day=1)
    return start


def demo_month_datetime(month_offset, day, hour=11, minute=30):
    """A safe date inside a month (never in the future, never past month end)."""
    start = month_start_offset(month_offset)
    next_month = (start + timedelta(days=32)).replace(day=1)
    last_day = (next_month - timedelta(days=1)).day
    day = min(day, last_day)
    if month_offset == 0:
        day = min(day, timezone.localdate().day)
    return timezone.make_aware(
        datetime.combine(start.replace(day=day), datetime.min.time())
    ) + timedelta(hours=hour, minutes=minute)


# (month offset, day, amount, description, category, type)
DEMO_LEDGER = [
    # ---------------------------------------------------- two months ago ----
    (2, 1, 45000, "Monthly salary credited - Infosys Ltd", "Salary", "CREDIT"),
    (2, 4, 8900, "Reliance Digital - headphones and speaker", "Shopping", "DEBIT"),
    (2, 7, 3600, "BigBasket monthly groceries", "Food", "DEBIT"),
    (2, 10, 2400, "Mobile postpaid bill - Airtel", "Bills", "DEBIT"),
    (2, 13, 1800, "Ola and Uber rides", "Travel", "DEBIT"),
    (2, 16, 1200, "PVR Cinemas and Netflix", "Entertainment", "DEBIT"),
    (2, 20, 2500, "Transfer to savings", "Transfer", "DEBIT"),
    (2, 25, 21500, "Credit card bill payment - BankFlow demo card", "Bills", "DEBIT"),
    # -------------------------------------------------------- last month ----
    (1, 1, 45000, "Monthly salary credited - Infosys Ltd", "Salary", "CREDIT"),
    (1, 3, 5600, "Myntra - festive shopping", "Shopping", "DEBIT"),
    (1, 5, 2100, "BigBasket groceries", "Food", "DEBIT"),
    (1, 8, 1400, "Water bill - BWSSB", "Bills", "DEBIT"),
    (1, 11, 2600, "Weekend trip fuel", "Travel", "DEBIT"),
    (1, 14, 700, "Spotify and Audible subscriptions", "Entertainment", "DEBIT"),
    (1, 18, 1900, "Restaurant - family dinner", "Food", "DEBIT"),
    (1, 22, 1900, "Transfer to savings", "Transfer", "DEBIT"),
    (1, 26, 12000, "Freelance project payment", "Other", "CREDIT"),
    # ------------------------------------------------------ this month -----
    (0, 1, 45000, "Monthly salary credited - Infosys Ltd", "Salary", "CREDIT"),
    (0, 2, 2450, "Amazon - electronics order", "Shopping", "DEBIT"),
    (0, 3, 1200, "Zomato - dinner order", "Food", "DEBIT"),
    (0, 4, 1500, "Electricity bill - BESCOM", "Bills", "DEBIT"),
    (0, 5, 2000, "IRCTC train tickets", "Travel", "DEBIT"),
    (0, 6, 800, "PVR Cinemas - movie tickets", "Entertainment", "DEBIT"),
    (0, 7, 4750, "Croma - new laptop accessories", "Shopping", "DEBIT"),
    (0, 8, 950, "Swiggy - lunch order", "Food", "DEBIT"),
    (0, 9, 1800, "UPI transfer to friend", "Transfer", "DEBIT"),
    (0, 10, 3000, "Insurance premium - demo policy", "Other", "DEBIT"),
]


def demo_transaction_seed():
    """28 fictional transactions across three months.

    This month: income ₹45,000, expenses ₹18,450, biggest category Shopping ₹7,200.
    """
    entries = []
    for month_offset, day, amount, description, category, txn_type in DEMO_LEDGER:
        entries.append({
            "when": demo_month_datetime(month_offset, day),
            "amount": amount,
            "description": description,
            "category": category,
            "transaction_type": txn_type,
        })
    return entries
```

### backend/banking/serializers.py

```python
from rest_framework import serializers

from .models import Account, Loan, Notification, Transaction
from .services import calculate_emi


class AccountSerializer(serializers.ModelSerializer):
    masked_account_number = serializers.ReadOnlyField()
    account_type_display = serializers.CharField(source="get_account_type_display", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    customer_name = serializers.CharField(source="user.name", read_only=True)
    customer_email = serializers.CharField(source="user.email", read_only=True)
    balance = serializers.FloatField()

    class Meta:
        model = Account
        fields = (
            "id", "account_number", "masked_account_number", "account_type",
            "account_type_display", "balance", "status", "status_display",
            "ifsc_code", "branch", "created_at", "customer_name", "customer_email",
        )


class TransactionSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source="get_category_display", read_only=True)
    type_display = serializers.CharField(source="get_transaction_type_display", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    amount = serializers.FloatField()
    balance_after = serializers.FloatField()
    signed_amount = serializers.ReadOnlyField()
    account_number = serializers.CharField(source="account.account_number", read_only=True)

    class Meta:
        model = Transaction
        fields = (
            "id", "transaction_id", "date", "description", "category",
            "category_display", "transaction_type", "type_display", "amount",
            "signed_amount", "status", "status_display", "balance_after",
            "account_number",
        )


class LoanSerializer(serializers.ModelSerializer):
    loan_type_display = serializers.CharField(source="get_loan_type_display", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    employment_type_display = serializers.CharField(
        source="get_employment_type_display", read_only=True
    )
    customer_name = serializers.CharField(source="user.name", read_only=True)
    customer_email = serializers.CharField(source="user.email", read_only=True)
    amount = serializers.FloatField()
    interest_rate = serializers.FloatField()
    emi = serializers.FloatField()
    remaining_amount = serializers.FloatField()
    paid_amount = serializers.ReadOnlyField()
    progress_percent = serializers.ReadOnlyField()

    class Meta:
        model = Loan
        fields = (
            "id", "loan_id", "loan_type", "loan_type_display", "amount",
            "interest_rate", "tenure_months", "emi", "remaining_amount",
            "paid_amount", "progress_percent", "status", "status_display",
            "purpose", "monthly_income", "employment_type",
            "employment_type_display", "applied_at", "customer_name", "customer_email",
            "user",
        )
        read_only_fields = (
            "id", "loan_id", "emi", "remaining_amount", "status", "applied_at", "user",
        )


class LoanApplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = (
            "loan_type", "amount", "interest_rate", "tenure_months",
            "purpose", "monthly_income", "employment_type",
        )

    def validate_amount(self, value):
        if value < 10000:
            raise serializers.ValidationError("The minimum demo loan amount is ₹10,000.")
        if value > 10000000:
            raise serializers.ValidationError("The maximum demo loan amount is ₹1,00,00,000.")
        return value

    def validate_tenure_months(self, value):
        if not 6 <= value <= 360:
            raise serializers.ValidationError("Tenure must be between 6 and 360 months.")
        return value

    def create(self, validated_data):
        emi_details = calculate_emi(
            float(validated_data["amount"]),
            float(validated_data.get("interest_rate") or 9.5),
            validated_data["tenure_months"],
        )
        loan = Loan.objects.create(
            emi=emi_details["monthly_emi"],
            remaining_amount=validated_data["amount"],
            **validated_data,
        )
        return loan


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ("id", "title", "message", "notification_type", "is_read", "created_at")
        read_only_fields = ("id", "title", "message", "notification_type", "created_at")


class EMICalculatorSerializer(serializers.Serializer):
    loan_amount = serializers.FloatField(min_value=1000)
    interest_rate = serializers.FloatField(min_value=0, max_value=50)
    tenure_months = serializers.IntegerField(min_value=1, max_value=480)
```

### backend/banking/views.py

```python
"""Customer facing API endpoints (JWT protected)."""
from django.db.models import Q
from django.utils.dateparse import parse_date
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Loan, Notification, Transaction
from .serializers import (
    AccountSerializer,
    EMICalculatorSerializer,
    LoanApplySerializer,
    LoanSerializer,
    NotificationSerializer,
    TransactionSerializer,
)
from .services import (
    calculate_emi,
    customer_transactions,
    get_account,
    get_dashboard,
)


class AccountView(APIView):
    """GET /api/account/"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        account = get_account(request.user)
        if not account:
            return Response({"detail": "No demo account found for this customer."},
                            status=status.HTTP_404_NOT_FOUND)
        return Response(AccountSerializer(account).data)


class TransactionListView(generics.ListAPIView):
    """GET /api/transactions/ with search, filters and pagination."""

    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = customer_transactions(self.request.user).select_related("account")
        params = self.request.query_params

        search = params.get("search")
        if search:
            qs = qs.filter(
                Q(description__icontains=search)
                | Q(transaction_id__icontains=search)
                | Q(category__icontains=search)
            )
        if params.get("category") and params["category"] != "ALL":
            qs = qs.filter(category=params["category"])
        if params.get("type") and params["type"] != "ALL":
            qs = qs.filter(transaction_type=params["type"].upper())
        if params.get("status") and params["status"] != "ALL":
            qs = qs.filter(status=params["status"].upper())

        start = parse_date(params.get("start_date") or "")
        end = parse_date(params.get("end_date") or "")
        if start:
            qs = qs.filter(date__date__gte=start)
        if end:
            qs = qs.filter(date__date__lte=end)

        ordering = params.get("ordering") or "-date"
        allowed = {"date", "-date", "amount", "-amount", "category", "-category"}
        return qs.order_by(ordering if ordering in allowed else "-date")

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        qs = self.filter_queryset(self.get_queryset())
        credits = sum(float(t.amount) for t in qs if t.transaction_type == Transaction.Type.CREDIT)
        debits = sum(float(t.amount) for t in qs if t.transaction_type == Transaction.Type.DEBIT)
        response.data["summary"] = {
            "total_credit": round(credits, 2),
            "total_debit": round(debits, 2),
            "net": round(credits - debits, 2),
        }
        return response


class TransactionDetailView(generics.RetrieveAPIView):
    """GET /api/transactions/<id>/"""

    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    def get_queryset(self):
        return customer_transactions(self.request.user).select_related("account")


class LoanListCreateView(generics.ListCreateAPIView):
    """GET /api/loans/ and POST /api/loans/ (demo application)."""

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Loan.objects.filter(user=self.request.user)
        status_filter = self.request.query_params.get("status")
        if status_filter and status_filter != "ALL":
            qs = qs.filter(status=status_filter.upper())
        loan_type = self.request.query_params.get("type")
        if loan_type and loan_type != "ALL":
            qs = qs.filter(loan_type=loan_type.upper())
        return qs

    def get_serializer_class(self):
        return LoanApplySerializer if self.request.method == "POST" else LoanSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        loan = serializer.save(user=request.user)
        Notification.objects.create(
            user=request.user,
            title="Loan application received",
            message=(
                f"Your {loan.get_loan_type_display()} application {loan.loan_id} for "
                f"₹{loan.amount:,.0f} is pending review by a bank employee."
            ),
            notification_type=Notification.NotificationType.LOAN,
        )
        return Response(LoanSerializer(loan).data, status=status.HTTP_201_CREATED)


class LoanDetailView(generics.RetrieveAPIView):
    """GET /api/loans/<id>/"""

    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Loan.objects.filter(user=self.request.user)


class NotificationListView(generics.ListAPIView):
    """GET /api/notifications/ - ?unread=true for unread only."""

    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        qs = Notification.objects.filter(user=self.request.user)
        if self.request.query_params.get("unread") == "true":
            qs = qs.filter(is_read=False)
        return qs


class NotificationUpdateView(generics.UpdateAPIView):
    """PUT /api/notifications/<id>/ -> mark as read (or unread)."""

    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


class MarkAllNotificationsReadView(APIView):
    """POST /api/notifications/read-all/"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        updated = Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({"updated": updated})


class DashboardView(APIView):
    """GET /api/dashboard/ - single call that powers the whole dashboard."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(get_dashboard(request.user))


class EMICalculatorView(APIView):
    """POST /api/emi/ - server side EMI calculation."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = EMICalculatorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        result = calculate_emi(
            data["loan_amount"], data["interest_rate"], data["tenure_months"]
        )
        return Response(result)
```

### backend/banking/admin_views.py

```python
"""Bank employee / admin API. Every endpoint requires the ADMIN role."""
from django.contrib.auth import get_user_model
from django.db.models import Count, Sum
from django.utils.dateparse import parse_date
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import IsBankStaff
from users.serializers import CustomerProfileSerializer

from .models import Account, Loan, Notification, Transaction, account_balance
from .serializers import AccountSerializer, LoanSerializer, TransactionSerializer
from .services import (
    aware,
    customer_transactions,
    format_inr,
    get_dashboard,
    loan_status_breakdown,
)

User = get_user_model()


class AdminAnalyticsView(APIView):
    """GET /api/admin/analytics/ - KPI cards + charts for the bank employee UI."""

    permission_classes = [IsBankStaff]

    def get(self, request):
        transactions = Transaction.objects.all()
        volume = sum(float(t.amount) for t in transactions)
        customers = User.objects.filter(role=User.Role.CUSTOMER)
        loans = Loan.objects.all()

        status_counts = {item["status"]: item["count"] for item in loan_status_breakdown()}

        return Response({
            "totals": {
                "customers": customers.count(),
                "accounts": Account.objects.count(),
                "transactions": transactions.count(),
                "loans": loans.count(),
                "pending_loans": status_counts.get("PENDING", 0),
                "active_loans": status_counts.get("ACTIVE", 0),
                "demo_volume": round(volume, 2),
                "demo_volume_display": format_inr(volume),
                "total_deposits": round(
                    float(Account.objects.aggregate(total=Sum("balance"))["total"] or 0), 2
                ),
                "outstanding": round(
                    float(loans.exclude(status=Loan.Status.COMPLETED)
                          .aggregate(total=Sum("remaining_amount"))["total"] or 0), 2
                ),
                "unread_notifications": Notification.objects.filter(is_read=False).count(),
            },
            "monthly_trend": monthly_trend_global(months=6),
            "category_breakdown": category_breakdown_global(),
            "loan_status_breakdown": loan_status_breakdown(),
            "transaction_type_split": transaction_type_split(),
            "top_customers": top_customers(),
        })


def monthly_trend_global(months=6):
    """Income vs expense across every demo customer."""
    from datetime import timedelta

    from django.utils import timezone

    from .services import month_bounds

    today = timezone.localdate()
    cursor = today.replace(day=1)
    series = []
    for _ in range(months):
        start, end = month_bounds(cursor)
        qs = Transaction.objects.filter(
            date__gte=aware(start), date__lt=aware(end),
            status=Transaction.Status.COMPLETED,
        )
        income = sum(float(t.amount) for t in qs if t.transaction_type == Transaction.Type.CREDIT)
        expense = sum(float(t.amount) for t in qs if t.transaction_type == Transaction.Type.DEBIT)
        series.append({
            "month": start.strftime("%b %Y"),
            "short_month": start.strftime("%b"),
            "income": round(income, 2),
            "expense": round(expense, 2),
            "transactions": qs.count(),
        })
        cursor = (start - timedelta(days=1)).replace(day=1)
    return list(reversed(series))


def category_breakdown_global():
    from .services import CATEGORY_COLORS

    totals = {}
    qs = Transaction.objects.filter(
        transaction_type=Transaction.Type.DEBIT, status=Transaction.Status.COMPLETED
    )
    for txn in qs:
        totals[txn.category] = totals.get(txn.category, 0) + float(txn.amount)
    data = [
        {"category": category, "amount": round(amount, 2),
         "color": CATEGORY_COLORS.get(category, "#94a3b8")}
        for category, amount in totals.items()
    ]
    return sorted(data, key=lambda item: item["amount"], reverse=True)


def transaction_type_split():
    return [
        {"type": "CREDIT", "label": "Credits", "count": Transaction.objects.filter(
            transaction_type=Transaction.Type.CREDIT).count()},
        {"type": "DEBIT", "label": "Debits", "count": Transaction.objects.filter(
            transaction_type=Transaction.Type.DEBIT).count()},
    ]


def top_customers(limit=5):
    rows = []
    for user in User.objects.filter(role=User.Role.CUSTOMER):
        rows.append({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "balance": round(account_balance(user), 2),
            "transactions": customer_transactions(user).count(),
            "loans": Loan.objects.filter(user=user).count(),
        })
    return sorted(rows, key=lambda row: row["balance"], reverse=True)[:limit]


class AdminCustomerListView(APIView):
    """GET /api/admin/customers/ - search + search-friendly customer table."""

    permission_classes = [IsBankStaff]

    def get(self, request):
        search = request.query_params.get("search", "").strip()
        qs = User.objects.filter(role=User.Role.CUSTOMER).prefetch_related(
            "accounts", "loans", "profile"
        )
        if search:
            qs = qs.filter(name__icontains=search) | qs.filter(email__icontains=search)

        rows = []
        for user in qs.distinct():
            account = Account.objects.filter(user=user).first()
            rows.append({
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "phone": getattr(getattr(user, "profile", None), "phone", ""),
                "role": user.role,
                "is_active": user.is_active,
                "joined": user.date_joined.isoformat(),
                "account_number": account.account_number if account else None,
                "masked_account_number": account.masked_account_number if account else None,
                "account_type": account.get_account_type_display() if account else None,
                "balance": round(account_balance(user), 2),
                "transaction_count": customer_transactions(user).count(),
                "loan_count": Loan.objects.filter(user=user).count(),
                "unread_notifications": Notification.unread_count(user),
            })
        return Response({"count": len(rows), "results": rows})


class AdminCustomerDetailView(APIView):
    """GET /api/admin/customers/<id>/ - customer 360 view."""

    permission_classes = [IsBankStaff]

    def get(self, request, pk):
        user = User.objects.filter(pk=pk).first()
        if not user:
            return Response({"detail": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)
        profile = getattr(user, "profile", None)
        account = Account.objects.filter(user=user).first()
        return Response({
            "customer": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "is_active": user.is_active,
                "joined": user.date_joined.isoformat(),
                "profile": CustomerProfileSerializer(profile).data if profile else None,
            },
            "accounts": AccountSerializer(Account.objects.filter(user=user), many=True).data,
            "dashboard": get_dashboard(user) if account else None,
            "loans": LoanSerializer(Loan.objects.filter(user=user), many=True).data,
        })


class AdminTransactionListView(generics.ListAPIView):
    """GET /api/admin/transactions/ - filter across every customer."""

    serializer_class = TransactionSerializer
    permission_classes = [IsBankStaff]

    def get_queryset(self):
        qs = Transaction.objects.select_related("account", "account__user")
        params = self.request.query_params
        if params.get("search"):
            qs = qs.filter(
                description__icontains=params["search"]
            ) | qs.filter(transaction_id__icontains=params["search"]) | qs.filter(
                account__user__name__icontains=params["search"]
            )
        if params.get("category") and params["category"] != "ALL":
            qs = qs.filter(category=params["category"])
        if params.get("type") and params["type"] != "ALL":
            qs = qs.filter(transaction_type=params["type"].upper())
        start = parse_date(params.get("start_date") or "")
        end = parse_date(params.get("end_date") or "")
        if start:
            qs = qs.filter(date__date__gte=start)
        if end:
            qs = qs.filter(date__date__lte=end)
        return qs.order_by("-date")

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        qs = self.filter_queryset(self.get_queryset())
        response.data["summary"] = {
            "count": qs.count(),
            "volume": round(sum(float(t.amount) for t in qs), 2),
        }
        return response


class AdminLoanListView(generics.ListAPIView):
    """GET /api/admin/loans/ - every demo loan with filters."""

    serializer_class = LoanSerializer
    permission_classes = [IsBankStaff]

    def get_queryset(self):
        qs = Loan.objects.select_related("user")
        params = self.request.query_params
        if params.get("search"):
            qs = qs.filter(loan_id__icontains=params["search"]) | qs.filter(
                user__name__icontains=params["search"]
            ) | qs.filter(user__email__icontains=params["search"])
        if params.get("status") and params["status"] != "ALL":
            qs = qs.filter(status=params["status"].upper())
        if params.get("type") and params["type"] != "ALL":
            qs = qs.filter(loan_type=params["type"].upper())
        return qs.order_by("-applied_at")


class AdminLoanUpdateView(APIView):
    """PATCH /api/admin/loans/<id>/ - approve / reject / activate a demo loan."""

    permission_classes = [IsBankStaff]

    def patch(self, request, pk):
        loan = Loan.objects.filter(pk=pk).first()
        if not loan:
            return Response({"detail": "Loan not found."}, status=status.HTTP_404_NOT_FOUND)
        new_status = str(request.data.get("status", "")).upper()
        valid = [choice[0] for choice in Loan.Status.choices]
        if new_status not in valid:
            return Response({"detail": f"status must be one of {valid}"},
                            status=status.HTTP_400_BAD_REQUEST)
        loan.status = new_status
        loan.save(update_fields=["status", "updated_at"])
        Notification.objects.create(
            user=loan.user,
            title=f"Loan {loan.loan_id} {loan.get_status_display()}",
            message=(
                f"Your {loan.get_loan_type_display()} application of ₹{loan.amount:,.0f} "
                f"is now {loan.get_status_display().lower()}."
            ),
            notification_type=Notification.NotificationType.LOAN,
        )
        return Response(LoanSerializer(loan).data)


class AdminUserListView(APIView):
    """GET /api/admin/users/ - user management table."""

    permission_classes = [IsBankStaff]

    def get(self, request):
        users = User.objects.all().order_by("role", "name")
        return Response({
            "count": users.count(),
            "results": [
                {
                    "id": u.id, "name": u.name, "email": u.email, "role": u.role,
                    "role_display": u.get_role_display(), "is_active": u.is_active,
                    "last_login": u.last_login.isoformat() if u.last_login else None,
                    "joined": u.date_joined.isoformat(),
                }
                for u in users
            ],
        })


class AdminOverviewView(APIView):
    """GET /api/admin/analytics/overview/ - the 6 KPI cards on the admin dashboard."""

    permission_classes = [IsBankStaff]

    def get(self, request):
        counts = Loan.objects.values("status").annotate(count=Count("id"))
        status_map = {row["status"]: row["count"] for row in counts}
        return Response({
            "total_customers": User.objects.filter(role=User.Role.CUSTOMER).count(),
            "total_accounts": Account.objects.count(),
            "total_transactions": Transaction.objects.count(),
            "total_loans": Loan.objects.count(),
            "pending_loans": status_map.get("PENDING", 0),
            "demo_transaction_volume": round(
                sum(float(t.amount) for t in Transaction.objects.all()), 2
            ),
        })
```

### backend/banking/urls/__init__.py

```python

```

### backend/banking/urls/customer_urls.py

```python
from django.urls import path

from banking.views import (
    AccountView,
    DashboardView,
    EMICalculatorView,
    LoanDetailView,
    LoanListCreateView,
    MarkAllNotificationsReadView,
    NotificationListView,
    NotificationUpdateView,
    TransactionDetailView,
    TransactionListView,
)

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("account/", AccountView.as_view(), name="account"),
    path("transactions/", TransactionListView.as_view(), name="transaction-list"),
    path("transactions/<int:pk>/", TransactionDetailView.as_view(), name="transaction-detail"),
    path("loans/", LoanListCreateView.as_view(), name="loan-list"),
    path("loans/<int:pk>/", LoanDetailView.as_view(), name="loan-detail"),
    path("emi/", EMICalculatorView.as_view(), name="emi-calculator"),
    path("notifications/", NotificationListView.as_view(), name="notification-list"),
    path("notifications/read-all/", MarkAllNotificationsReadView.as_view(),
         name="notification-read-all"),
    path("notifications/<int:pk>/", NotificationUpdateView.as_view(), name="notification-update"),
]
```

### backend/banking/urls/admin_urls.py

```python
from django.urls import path

from banking.admin_views import (
    AdminAnalyticsView,
    AdminCustomerDetailView,
    AdminCustomerListView,
    AdminLoanListView,
    AdminLoanUpdateView,
    AdminOverviewView,
    AdminTransactionListView,
    AdminUserListView,
)

urlpatterns = [
    path("analytics/", AdminAnalyticsView.as_view(), name="admin-analytics"),
    path("analytics/overview/", AdminOverviewView.as_view(), name="admin-overview"),
    path("customers/", AdminCustomerListView.as_view(), name="admin-customers"),
    path("customers/<int:pk>/", AdminCustomerDetailView.as_view(), name="admin-customer-detail"),
    path("transactions/", AdminTransactionListView.as_view(), name="admin-transactions"),
    path("loans/", AdminLoanListView.as_view(), name="admin-loans"),
    path("loans/<int:pk>/", AdminLoanUpdateView.as_view(), name="admin-loan-update"),
    path("users/", AdminUserListView.as_view(), name="admin-users"),
]
```

### backend/banking/admin.py

```python
from django.contrib import admin

from .models import Account, Loan, Notification, Transaction


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("account_number", "user", "account_type", "balance", "status", "created_at")
    list_filter = ("account_type", "status")
    search_fields = ("account_number", "user__name", "user__email")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("transaction_id", "date", "account", "description", "category",
                    "transaction_type", "amount", "status")
    list_filter = ("category", "transaction_type", "status")
    search_fields = ("transaction_id", "description", "account__user__name")
    date_hierarchy = "date"


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ("loan_id", "user", "loan_type", "amount", "interest_rate",
                    "tenure_months", "emi", "remaining_amount", "status")
    list_filter = ("loan_type", "status")
    search_fields = ("loan_id", "user__name", "user__email")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "notification_type", "is_read", "created_at")
    list_filter = ("notification_type", "is_read")
    search_fields = ("title", "message", "user__email")
```

### backend/banking/management/__init__.py

```python

```

### backend/banking/management/commands/__init__.py

```python

```

### backend/banking/management/commands/seed_demo.py

```python
"""python manage.py seed_demo

Creates 3 fictional customers, accounts, 20+ transactions, loans,
notifications and a couple of saved AI conversations.
"""
import random
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from assistant.models import ChatMessage
from banking.models import Account, Loan, Notification, Transaction
from banking.services import (
    calculate_emi,
    demo_transaction_seed,
    random_account_number,
    record_transaction,
)
from users.models import CustomerProfile

User = get_user_model()

DEMO_PASSWORD = "Demo@12345"
ADMIN_PASSWORD = "Admin@12345"

CUSTOMERS = [
    {
        "name": "Mohammed Adnan",
        "email": "mohammed@bankflow.com",
        "phone": "+91 98765 43210",
        "occupation": "Senior Software Engineer",
        "employment_type": "SALARIED",
        "monthly_income": 45000,
        "account_type": "SAVINGS",
        "balance": 85450,
        "address": "Bengaluru, Karnataka",
    },
    {
        "name": "Aisha Khan",
        "email": "aisha@bankflow.com",
        "phone": "+91 91234 56780",
        "occupation": "Product Designer",
        "employment_type": "SELF_EMPLOYED",
        "monthly_income": 78000,
        "account_type": "SALARY",
        "balance": 142300,
        "address": "Hyderabad, Telangana",
    },
    {
        "name": "Rahul Verma",
        "email": "rahul@bankflow.com",
        "phone": "+91 99887 76655",
        "occupation": "Chartered Accountant",
        "employment_type": "SELF_EMPLOYED",
        "monthly_income": 96000,
        "account_type": "CURRENT",
        "balance": 207800,
        "address": "Pune, Maharashtra",
    },
]


class Command(BaseCommand):
    help = "Seed BankFlow with fictional demo banking data."

    def add_arguments(self, parser):
        parser.add_argument("--flush", action="store_true",
                            help="Delete existing demo data before seeding.")

    def handle(self, *args, **options):
        random.seed(7)
        if options["flush"]:
            ChatMessage.objects.all().delete()
            Notification.objects.all().delete()
            Transaction.objects.all().delete()
            Loan.objects.all().delete()
            Account.objects.all().delete()
            CustomerProfile.objects.all().delete()
            User.objects.all().delete()
            self.stdout.write(self.style.WARNING("Existing data removed."))

        admin = self.create_admin()
        for index, data in enumerate(CUSTOMERS):
            user = self.create_customer(data)
            account = self.create_account(user, data)
            if index == 0:
                self.seed_transactions(account)
            else:
                self.seed_simple_transactions(account, data)
            self.stdout.write(self.style.SUCCESS(f"Seeded customer {user.name}"))

        self.seed_loans()
        self.seed_notifications()
        self.seed_chat_history()

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Demo data ready."))
        self.stdout.write(f"Admin    : {admin.email} / {ADMIN_PASSWORD}")
        for customer in CUSTOMERS:
            self.stdout.write(f"Customer : {customer['email']} / {DEMO_PASSWORD}")

    # ------------------------------------------------------------------ steps
    def create_admin(self):
        admin, created = User.objects.get_or_create(
            email="admin@bankflow.com",
            defaults={
                "name": "Priya Nair (Bank Employee)",
                "role": User.Role.ADMIN,
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if created:
            admin.set_password(ADMIN_PASSWORD)
            admin.save()
        return admin

    def create_customer(self, data):
        user, created = User.objects.get_or_create(
            email=data["email"],
            defaults={"name": data["name"], "role": User.Role.CUSTOMER},
        )
        if created:
            user.set_password(DEMO_PASSWORD)
            user.save()
        CustomerProfile.objects.update_or_create(
            user=user,
            defaults={
                "phone": data["phone"],
                "occupation": data["occupation"],
                "employment_type": data["employment_type"],
                "monthly_income": data["monthly_income"],
                "address": data["address"],
            },
        )
        return user

    def create_account(self, user, data):
        account, created = Account.objects.get_or_create(
            user=user,
            defaults={
                "account_number": random_account_number(),
                "account_type": data["account_type"],
                "balance": data["balance"],
                "ifsc_code": "BANKFL0001234",
                "branch": "BankFlow Demo Branch, MG Road",
            },
        )
        return account

    def seed_transactions(self, account):
        """The 28 transaction, three month history for Mohammed Adnan."""
        account.transactions.all().delete()
        for entry in demo_transaction_seed():
            Transaction.objects.create(
                account=account,
                date=entry["when"],
                description=entry["description"],
                category=entry["category"],
                transaction_type=entry["transaction_type"],
                amount=entry["amount"],
                status=Transaction.Status.COMPLETED,
                balance_after=0,
            )
        # Rebuild the running balance so the newest transaction row ends at ₹85,450.
        transactions = list(account.transactions.order_by("date"))
        target_balance = 85450.0
        running = target_balance - sum(t.signed_amount for t in transactions)
        for txn in transactions:
            running += txn.signed_amount
            txn.balance_after = round(running, 2)
            txn.save(update_fields=["balance_after"])
        account.balance = round(running, 2)
        account.save(update_fields=["balance"])

    def seed_simple_transactions(self, account, data):
        """Lighter history for the other two customers."""
        today = timezone.now()
        entries = [
            (2, data["monthly_income"], "Monthly salary credited", "Salary", "CREDIT"),
            (3, 4200, "Groceries - BigBasket", "Food", "DEBIT"),
            (5, 8900, "Home appliances - Croma", "Shopping", "DEBIT"),
            (8, 2400, "Electricity bill", "Bills", "DEBIT"),
            (12, 1800, "Movie night", "Entertainment", "DEBIT"),
            (16, 3200, "Weekend travel", "Travel", "DEBIT"),
            (24, 15000, "EMI paid - demo loan", "Transfer", "DEBIT"),
            (33, data["monthly_income"], "Monthly salary credited", "Salary", "CREDIT"),
            (40, 3600, "Restaurant bill", "Food", "DEBIT"),
        ]
        for days, amount, description, category, txn_type in reversed(entries):
            record_transaction(
                account,
                amount=amount,
                description=description,
                category=category,
                transaction_type=txn_type,
                when=today - timedelta(days=days),
            )
        account.balance = data["balance"]
        account.save(update_fields=["balance"])

    def seed_loans(self):
        mohammed = User.objects.get(email="mohammed@bankflow.com")
        aisha = User.objects.get(email="aisha@bankflow.com")
        rahul = User.objects.get(email="rahul@bankflow.com")

        loans = [
            (mohammed, "HOME", 1500000, 8.5, 180, "ACTIVE", "Home renovation"),
            (mohammed, "VEHICLE", 250000, 9.75, 60, "ACTIVE", "New car purchase"),
            (aisha, "EDUCATION", 600000, 7.25, 84, "APPROVED", "Executive MBA program"),
            (aisha, "PERSONAL", 150000, 11.5, 36, "REJECTED", "Business expansion"),
            (rahul, "HOME", 3500000, 8.1, 240, "ACTIVE", "Apartment purchase"),
            (rahul, "VEHICLE", 900000, 9.4, 72, "PENDING", "Family car upgrade"),
        ]
        for user, loan_type, amount, rate, tenure, status, purpose in loans:
            emi = calculate_emi(amount, rate, tenure)["monthly_emi"]
            paid_ratio = 0.35 if status == Loan.Status.ACTIVE else 0
            Loan.objects.update_or_create(
                user=user,
                loan_type=loan_type,
                purpose=purpose,
                defaults={
                    "amount": amount,
                    "interest_rate": rate,
                    "tenure_months": tenure,
                    "emi": emi,
                    "remaining_amount": round(amount * (1 - paid_ratio), 2),
                    "status": status,
                    "monthly_income": getattr(getattr(user, "profile", None),
                                              "monthly_income", 0) or 0,
                    "employment_type": getattr(getattr(user, "profile", None),
                                               "employment_type", "SALARIED"),
                },
            )

    def seed_notifications(self):
        for user in User.objects.filter(role=User.Role.CUSTOMER):
            items = [
                ("Salary credited",
                 "Your monthly salary has been credited to your demo account.",
                 "TRANSACTION", False),
                ("New transaction detected",
                 "A card transaction was detected. Review it in your transactions page.",
                 "SECURITY", False),
                ("Monthly spending summary available",
                 "Your fictional monthly spending report is ready to explore.",
                 "SUMMARY", False),
                ("Loan application updated",
                 "A demo loan application status changed. Check the loans page.",
                 "LOAN", True),
                ("Security notification",
                 "This is a demo environment - never enter real banking credentials.",
                 "SECURITY", True),
            ]
            for title, message, kind, is_read in items:
                Notification.objects.create(
                    user=user, title=title, message=message,
                    notification_type=kind, is_read=is_read,
                )

    def seed_chat_history(self):
        mohammed = User.objects.get(email="mohammed@bankflow.com")
        history = [
            ("What is my current balance?",
             "Your current available balance is ₹85,450 across 1 demo account.",
             "account_balance"),
            ("How much did I spend this month?",
             "You spent ₹18,450 this month. That is your total debit value for the "
             "current month.", "expense_summary"),
            ("What was my biggest expense?",
             "Your largest expense this month was Shopping at ₹7,200.",
             "biggest_expense"),
            ("Explain EMI.",
             "EMI stands for Equated Monthly Instalment. It is the fixed amount you pay "
             "every month towards a loan, covering both principal and interest.",
             "banking_knowledge"),
        ]
        for message, response, response_type in history:
            ChatMessage.objects.create(
                user=mohammed, message=message, response=response,
                response_type=response_type,
            )
```

### backend/banking/tests.py

```python
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Loan, Notification, Transaction
from .services import bootstrap_customer, calculate_emi, record_transaction

User = get_user_model()


class BankingApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="customer@bankflow.com", password="Demo@12345", name="Demo Customer"
        )
        self.account = bootstrap_customer(self.user)
        self.account.balance = 85450
        self.account.save()
        now = timezone.now()
        record_transaction(self.account, amount=45000, description="Monthly salary",
                           category="Salary", transaction_type="CREDIT",
                           when=now - timedelta(days=2))
        record_transaction(self.account, amount=7200, description="Croma shopping",
                           category="Shopping", transaction_type="DEBIT",
                           when=now - timedelta(days=5))
        record_transaction(self.account, amount=1200, description="Zomato order",
                           category="Food", transaction_type="DEBIT",
                           when=now - timedelta(days=6))
        self.account.refresh_from_db()
        self.account.balance = 85450
        self.account.save()
        self.client.force_authenticate(self.user)

    def test_account_endpoint_masks_number(self):
        response = self.client.get("/api/account/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["masked_account_number"].startswith("XXXX"))
        self.assertEqual(response.data["balance"], 85450.0)

    def test_dashboard_returns_cards_and_charts(self):
        response = self.client.get("/api/dashboard/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["balance"], 85450.0)
        self.assertEqual(response.data["monthly_income"], 45000.0)
        self.assertEqual(response.data["monthly_expenses"], 8400.0)
        self.assertEqual(response.data["top_category"]["category"], "Shopping")
        self.assertEqual(len(response.data["monthly_trend"]), 6)

    def test_transaction_filters_and_search(self):
        response = self.client.get("/api/transactions/", {"category": "Food"})
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["category"], "Food")

        response = self.client.get("/api/transactions/", {"type": "CREDIT"})
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["summary"]["total_credit"], 45000.0)

        response = self.client.get("/api/transactions/", {"search": "Zomato"})
        self.assertEqual(response.data["count"], 1)

    def test_loan_application_and_detail(self):
        payload = {
            "loan_type": "PERSONAL", "amount": 200000, "interest_rate": 10.5,
            "tenure_months": 24, "purpose": "Demo purpose",
            "monthly_income": 60000, "employment_type": "SALARIED",
        }
        response = self.client.post("/api/loans/", payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        loan_id = response.data["id"]
        expected_emi = calculate_emi(200000, 10.5, 24)["monthly_emi"]
        self.assertAlmostEqual(response.data["emi"], expected_emi, places=2)
        self.assertEqual(response.data["status"], Loan.Status.PENDING)

        detail = self.client.get(f"/api/loans/{loan_id}/")
        self.assertEqual(detail.status_code, status.HTTP_200_OK)
        self.assertEqual(detail.data["remaining_amount"], 200000.0)
        self.assertTrue(Notification.objects.filter(user=self.user,
                                                    notification_type="LOAN").exists())

    def test_emi_calculator_endpoint(self):
        response = self.client.post("/api/emi/", {
            "loan_amount": 500000, "interest_rate": 9, "tenure_months": 60,
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(response.data["monthly_emi"], 0)
        self.assertGreater(response.data["total_interest"], 0)
        self.assertAlmostEqual(
            response.data["total_payment"],
            response.data["principal"] + response.data["total_interest"],
            places=1,
        )

    def test_notifications_and_mark_read(self):
        notification = Notification.objects.create(
            user=self.user, title="Test", message="Demo message"
        )
        listing = self.client.get("/api/notifications/")
        self.assertGreaterEqual(listing.data["count"] if isinstance(listing.data, dict)
                                else len(listing.data), 1)

        updated = self.client.put(f"/api/notifications/{notification.id}/", {"is_read": True})
        self.assertEqual(updated.status_code, status.HTTP_200_OK)
        notification.refresh_from_db()
        self.assertTrue(notification.is_read)


class AdminApiTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            email="admin@bankflow.com", password="Admin@12345",
            name="Bank Employee", role=User.Role.ADMIN,
        )
        self.customer = User.objects.create_user(
            email="c@bankflow.com", password="Demo@12345", name="Customer One"
        )
        account = bootstrap_customer(self.customer)
        record_transaction(account, amount=5000, description="Salary", category="Salary",
                           transaction_type="CREDIT")

    def test_customer_cannot_open_admin_api(self):
        self.client.force_authenticate(self.customer)
        self.assertEqual(self.client.get("/api/admin/analytics/").status_code,
                         status.HTTP_403_FORBIDDEN)

    def test_admin_analytics_and_customer_table(self):
        self.client.force_authenticate(self.admin)
        analytics = self.client.get("/api/admin/analytics/")
        self.assertEqual(analytics.status_code, status.HTTP_200_OK)
        self.assertEqual(analytics.data["totals"]["customers"], 1)

        customers = self.client.get("/api/admin/customers/")
        self.assertEqual(customers.data["count"], 1)
        self.assertEqual(customers.data["results"][0]["email"], "c@bankflow.com")

        overview = self.client.get("/api/admin/analytics/overview/")
        self.assertEqual(overview.data["total_customers"], 1)

    def test_admin_can_approve_loan(self):
        loan = Loan.objects.create(user=self.customer, loan_type="PERSONAL",
                                   amount=100000, emi=5000, remaining_amount=100000)
        self.client.force_authenticate(self.admin)
        response = self.client.patch(f"/api/admin/loans/{loan.id}/", {"status": "APPROVED"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        loan.refresh_from_db()
        self.assertEqual(loan.status, Loan.Status.APPROVED)
        self.assertTrue(Notification.objects.filter(user=self.customer).exists())

    def test_transaction_type_split_present(self):
        self.client.force_authenticate(self.admin)
        analytics = self.client.get("/api/admin/analytics/")
        self.assertEqual(len(analytics.data["transaction_type_split"]), 2)
        self.assertEqual(len(analytics.data["loan_status_breakdown"]), 5)
```

## 4. BACKEND - ASSISTANT APP (AI service, chat, monitoring)

### backend/assistant/__init__.py

```python

```

### backend/assistant/apps.py

```python
from django.apps import AppConfig


class AssistantConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "assistant"
```

### backend/assistant/models.py

```python
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
```

### backend/assistant/ai_service.py

```python
"""BankFlow AI service.

Design goals
------------
1. `answer(user, message)` is the single entry point used by the view.
2. Intent detection + data retrieval are completely independent from the
   language model, so the demo always works offline (rule based fallback).
3. If `AI_PROVIDER=openai` and an API key is present, the *same* retrieved
   banking context is sent to the LLM so the wording becomes natural while the
   numbers stay grounded in the database.
"""
import json
import re

from django.conf import settings

from banking.services import (
    big_category_names,
    category_total,
    customer_transactions,
    format_inr,
    get_dashboard,
    to_float,
)
from banking.models import Account, Loan

BANKING_KNOWLEDGE = {
    "emi": (
        "EMI stands for Equated Monthly Instalment. It is the fixed amount you pay "
        "every month towards a loan; each instalment contains a principal part and an "
        "interest part. A higher tenure lowers the EMI but increases the total interest."
    ),
    "kyc": (
        "KYC (Know Your Customer) is the identity verification process banks must follow. "
        "It usually needs a photo ID, address proof and a recent photograph. KYC keeps "
        "accounts compliant and protects customers from fraud."
    ),
    "savings account": (
        "A savings account is a deposit account for everyday money. It earns interest, "
        "allows withdrawals and is meant for personal use rather than business transactions."
    ),
    "credit score": (
        "A credit score is a three digit number (typically 300-900 in India) that estimates "
        "how reliably you repay debt. It is built from repayment history, credit utilisation, "
        "credit age, loan mix and new enquiries."
    ),
    "cibil": (
        "CIBIL is one of India's credit bureaus. It publishes your credit score, which banks "
        "review before approving loans or credit cards. Scores above 750 are usually preferred."
    ),
    "fixed deposit": (
        "A fixed deposit (FD) locks a lump sum with the bank for a fixed period at a fixed "
        "interest rate. It usually earns more than a savings account and is low risk."
    ),
    "interest rate": (
        "An interest rate is the percentage a bank pays you on deposits or charges you on a "
        "loan. Loans usually use reducing-balance interest, so interest is charged on the "
        "outstanding amount."
    ),
    "upi": (
        "UPI (Unified Payments Interface) is an instant bank-to-bank payment system in India. "
        "This demo app does not move real money - transfers shown here are simulated."
    ),
    "neft": (
        "NEFT is a bank transfer system that settles transactions in batches. It is commonly "
        "used for larger transfers between accounts in India."
    ),
    "rtgs": (
        "RTGS is the Real Time Gross Settlement system used for high value transfers that "
        "settle instantly, transfer by transfer."
    ),
    "compound interest": (
        "Compound interest is interest calculated on both the original amount and the interest "
        "already earned, so money grows faster over long periods."
    ),
}

INTENT_KEYWORDS = {
    "account_balance": ["balance", "how much money", "account balance", "available amount"],
    "account_details": ["account details", "account number", "my account", "ifsc", "account info",
                        "account type"],
    "recent_transactions": ["transaction", "transactions", "recent activity", "statement",
                            "last payment", "history"],
    "expense_summary": ["spend", "spent", "expense", "expenses", "how much did i spend",
                        "total spending"],
    "biggest_expense": ["biggest expense", "largest expense", "highest expense", "most spent",
                        "biggest spend"],
    "category_spend": ["spend on", "spent on", "expenses on", "category", "categories"],
    "loan_list": ["what loans", "my loans", "do i have", "loan do i", "loans do i"],
    "loan_emi": ["what is my emi", "my emi", "emi amount", "monthly instalment", "monthly installment"],
    "loan_remaining": ["remaining", "outstanding", "left to pay", "how much loan amount"],
    "compare_months": ["compare", "last month", "previous month", "versus", "than last"],
    "category_breakdown": ["spending categories", "category breakdown", "where does my money go",
                           "breakdown of my spending"],
    "financial_summary": ["summary", "give me a summary", "overview", "how am i doing",
                          "financial health"],
    "banking_knowledge": list(BANKING_KNOWLEDGE.keys()) + ["what is", "explain", "define"],
    "loan_info": ["loan", "loans", "borrow", "eligibility"],
    "emi_calculator": ["calculate emi", "emi calculator", "emi for"],
    "greeting": ["hello", "hi ", "hey", "good morning", "good evening"],
    "help": ["what can you do", "help", "who are you", "your name"],
}


def normalise(text):
    return re.sub(r"\s+", " ", (text or "").strip().lower())


def detect_intent(message):
    """Score each intent by keyword overlaps - deterministic and explainable."""
    text = normalise(message)
    scores = {}
    for intent, keywords in INTENT_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            if keyword in text:
                score += len(keyword.split()) * 2 + 1
        if score:
            scores[intent] = score
    if not scores:
        return "unknown"

    # A few tie-breakers so common demo questions land on the right intent.
    if "balance" in text:
        return "account_balance"
    if "emi" in text:
        if any(word in text for word in ["my emi", "emi amount", "emi per month",
                                         "emi do i", "emi i pay", "calculate emi"]):
            return "loan_emi"
        if any(word in text for word in ["what is", "explain", "define", "mean",
                                         "stand for"]):
            return "banking_knowledge"
    if any(word in text for word in ["spend", "spent", "expense", "expenses"]) and any(
        category.lower() in text for category in big_category_names()
    ):
        return "category_spend"
    if "loan" in text and any(word in text for word in ["what loans", "my loans", "list"]):
        return "loan_list"
    return max(scores, key=scores.get)


# --------------------------------------------------------------------- data --
def build_context(user):
    """Structured snapshot of the customer data the assistant is allowed to see."""
    dashboard = get_dashboard(user)
    account = Account.objects.filter(user=user).first()
    loans = Loan.objects.filter(user=user)
    return {
        "customer_name": user.name,
        "balance": dashboard["balance"],
        "monthly_income": dashboard["monthly_income"],
        "monthly_expenses": dashboard["monthly_expenses"],
        "previous_month_expenses": dashboard["previous_month_expenses"],
        "monthly_savings": dashboard["monthly_savings"],
        "top_category": dashboard["top_category"],
        "spending_categories": dashboard["spending_categories"],
        "monthly_trend": dashboard["monthly_trend"],
        "active_loans": dashboard["active_loans"],
        "monthly_emi_total": dashboard["monthly_emi_total"],
        "total_outstanding": dashboard["total_outstanding"],
        "account": {
            "number": account.masked_account_number if account else None,
            "type": account.get_account_type_display() if account else None,
            "status": account.get_status_display() if account else None,
            "ifsc": account.ifsc_code if account else None,
            "branch": account.branch if account else None,
        },
        "loans": [
            {
                "loan_id": loan.loan_id,
                "type": loan.get_loan_type_display(),
                "amount": to_float(loan.amount),
                "emi": to_float(loan.emi),
                "remaining": to_float(loan.remaining_amount),
                "status": loan.get_status_display(),
                "interest_rate": to_float(loan.interest_rate),
                "tenure_months": loan.tenure_months,
            }
            for loan in loans
        ],
        "recent_transactions": [
            {
                "date": t.date.strftime("%d %b %Y"),
                "description": t.description,
                "category": t.category,
                "type": t.transaction_type,
                "amount": to_float(t.amount),
            }
            for t in customer_transactions(user)[:5]
        ],
    }


# ----------------------------------------------------------- rule responses --
def _balance_answer(context):
    return {
        "response": (
            f"Your current available balance is ₹{format_inr(context['balance'])}."
        ),
        "type": "account_balance",
        "data": {"amount": context["balance"]},
    }


def _account_details(context):
    account = context["account"]
    if not account["number"]:
        return _no_account()
    return {
        "response": (
            f"Here are your demo account details:\n"
            f"• Account number: {account['number']}\n"
            f"• Type: {account['type']}\n"
            f"• Status: {account['status']}\n"
            f"• IFSC: {account['ifsc']}\n"
            f"• Branch: {account['branch']}\n"
            f"• Available balance: ₹{format_inr(context['balance'])}"
        ),
        "type": "account_details",
        "data": account,
    }


def _expense_summary(context):
    return {
        "response": (
            f"You spent ₹{format_inr(context['monthly_expenses'])} this month. "
            f"Your income for the month is ₹{format_inr(context['monthly_income'])}, "
            f"so your net savings are ₹{format_inr(context['monthly_savings'])}."
        ),
        "type": "expense_summary",
        "data": {
            "amount": context["monthly_expenses"],
            "income": context["monthly_income"],
            "savings": context["monthly_savings"],
        },
    }


def _biggest_expense(context):
    top = context["top_category"]
    if not top:
        return {
            "response": "You have no debit transactions recorded this month yet.",
            "type": "biggest_expense",
            "data": None,
        }
    return {
        "response": (
            f"Your largest expense category this month was {top['category']} at "
            f"₹{format_inr(top['amount'])}."
        ),
        "type": "biggest_expense",
        "data": top,
    }


def _category_spend(user, message, context):
    text = normalise(message)
    matches = []
    for item in context["spending_categories"]:
        if item["category"].lower() in text:
            matches.append(item)
    for name in big_category_names():
        if name.lower() in text and not any(m["category"] == name for m in matches):
            amount = category_total(user, [name])
            if amount:
                matches.append({"category": name, "amount": amount})

    if not matches:
        return _category_breakdown(context)
    lines = ", ".join(f"{m['category']} ₹{format_inr(m['amount'])}" for m in matches)
    return {
        "response": f"Here is what you spent on this month: {lines}.",
        "type": "category_spend",
        "data": matches,
    }


def _category_breakdown(context):
    categories = context["spending_categories"]
    if not categories:
        return _empty_month()
    lines = "\n".join(
        f"• {item['category']}: ₹{format_inr(item['amount'])}" for item in categories
    )
    return {
        "response": (
            f"Your spending categories for this month are:\n{lines}\n"
            f"Total: ₹{format_inr(context['monthly_expenses'])}"
        ),
        "type": "category_breakdown",
        "data": categories,
    }


def _recent_transactions(context):
    rows = context["recent_transactions"]
    if not rows:
        return {
            "response": "You have no transactions yet in this demo account.",
            "type": "recent_transactions",
            "data": [],
        }
    lines = "\n".join(
        f"• {row['date']} - {row['description']} "
        f"({'credit' if row['type'] == 'CREDIT' else 'debit'} "
        f"₹{format_inr(row['amount'])})"
        for row in rows
    )
    return {
        "response": f"Here are your latest 5 demo transactions:\n{lines}",
        "type": "recent_transactions",
        "data": rows,
    }


def _loan_list(context):
    loans = context["loans"]
    if not loans:
        return {
            "response": "You do not have any demo loans on record right now.",
            "type": "loan_list",
            "data": [],
        }
    lines = "\n".join(
        f"• {loan['type']} {loan['loan_id']} - ₹{format_inr(loan['amount'])} at "
        f"{loan['interest_rate']}% ({loan['status']})"
        for loan in loans
    )
    active = sum(1 for loan in loans if loan["status"] in ("Active", "Approved"))
    if active == len(loans):
        headline = (
            f"You currently have {active} active demo loan"
            f"{'' if active == 1 else 's'}"
        )
    else:
        headline = (
            f"You currently have {len(loans)} demo loan"
            f"{'' if len(loans) == 1 else 's'}, of which {active} "
            f"{'is' if active == 1 else 'are'} active or approved"
        )
    return {
        "response": f"{headline}:\n{lines}",
        "type": "loan_list",
        "data": loans,
    }


def _loan_emi(context):
    loans = [loan for loan in context["loans"] if loan["status"] in ("Active", "Approved")]
    if not loans:
        return {
            "response": (
                "You have no active demo loans, so there is no EMI to pay right now. "
                "You can estimate an EMI on a new loan using the EMI calculator."
            ),
            "type": "loan_emi",
            "data": [],
        }
    lines = "\n".join(
        f"• {loan['type']} ({loan['loan_id']}): ₹{format_inr(loan['emi'])} per month"
        for loan in loans
    )
    return {
        "response": (
            f"Your total monthly EMI is ₹{format_inr(context['monthly_emi_total'])}:\n{lines}"
        ),
        "type": "loan_emi",
        "data": loans,
    }


def _loan_remaining(context):
    loans = [loan for loan in context["loans"] if loan["remaining"] > 0]
    if not loans:
        return {
            "response": "You have no outstanding demo loan amount. Everything is repaid.",
            "type": "loan_remaining",
            "data": None,
        }
    lines = "\n".join(
        f"• {loan['type']} ({loan['loan_id']}): ₹{format_inr(loan['remaining'])} remaining"
        for loan in loans
    )
    return {
        "response": (
            f"Your total remaining demo loan amount is "
            f"₹{format_inr(context['total_outstanding'])}:\n{lines}"
        ),
        "type": "loan_remaining",
        "data": loans,
    }


def _compare_months(context):
    current = context["monthly_expenses"]
    previous = context["previous_month_expenses"]
    if previous == 0:
        return {
            "response": (
                f"You spent ₹{format_inr(current)} this month. There is no spending history "
                "for last month in this demo account yet."
            ),
            "type": "compare_months",
            "data": {"current": current, "previous": previous},
        }
    difference = current - previous
    direction = "more" if difference > 0 else "less"
    percent = abs(difference) / previous * 100
    return {
        "response": (
            f"This month you spent ₹{format_inr(current)} compared with "
            f"₹{format_inr(previous)} last month - that is ₹{format_inr(abs(difference))} "
            f"({percent:.1f}%) {direction}."
        ),
        "type": "compare_months",
        "data": {"current": current, "previous": previous,
                 "difference": round(difference, 2)},
    }


def _financial_summary(context):
    top = context["top_category"]
    top_line = (
        f"Your biggest category was {top['category']} (₹{format_inr(top['amount'])})."
        if top else "You have no debit transactions this month yet."
    )
    return {
        "response": (
            f"Here is your financial summary, {context['customer_name'].split()[0]}:\n"
            f"• Available balance: ₹{format_inr(context['balance'])}\n"
            f"• Income this month: ₹{format_inr(context['monthly_income'])}\n"
            f"• Expenses this month: ₹{format_inr(context['monthly_expenses'])}\n"
            f"• Net savings: ₹{format_inr(context['monthly_savings'])}\n"
            f"• Active loans: {context['active_loans']} with a monthly EMI of "
            f"₹{format_inr(context['monthly_emi_total'])}\n"
            f"{top_line}"
        ),
        "type": "financial_summary",
        "data": context,
    }


def _knowledge(message):
    text = normalise(message)
    for key, explanation in BANKING_KNOWLEDGE.items():
        if key in text:
            return {
                "response": explanation,
                "type": "banking_knowledge",
                "data": {"topic": key},
            }
    return {
        "response": (
            "I can explain banking basics such as EMI, KYC, savings accounts, credit "
            "scores, fixed deposits, interest rates, UPI, NEFT and RTGS. Ask me about any "
            "of those, or ask about your own demo balance, spending or loans."
        ),
        "type": "banking_knowledge",
        "data": None,
    }


def _help(context):
    return {
        "response": (
            f"Hi {context['customer_name'].split()[0]}, I am BankFlow AI. I can help you with:\n"
            "• Balance and account details\n"
            "• Recent transactions\n"
            "• This month's spending, biggest expense and spending categories\n"
            "• Your loans, EMI and outstanding amount\n"
            "• Banking concepts like EMI, KYC and credit score\n"
            "Try: “How much did I spend on food?”"
        ),
        "type": "help",
        "data": None,
    }


def _greeting(context):
    return {
        "response": (
            f"Hello {context['customer_name'].split()[0]}! I am BankFlow AI, your demo "
            "banking assistant. Ask me about your balance, spending, loans or any banking term."
        ),
        "type": "greeting",
        "data": None,
    }


def _no_account():
    return {
        "response": "I could not find a demo account linked to your profile yet.",
        "type": "error",
        "data": None,
    }


def _empty_month():
    return {
        "response": "You have no debit transactions recorded this month, so there is nothing to break down.",
        "type": "category_breakdown",
        "data": [],
    }


def _unknown(context):
    return {
        "response": (
            "I could not map that question to your demo banking data. Try asking about your "
            "balance, this month's spending, your biggest expense, your loans, your EMI, or a "
            "banking term such as “What is KYC?”"
        ),
        "type": "unknown",
        "data": None,
    }


RULE_ANSWERS = {
    "account_balance": _balance_answer,
    "account_details": _account_details,
    "expense_summary": _expense_summary,
    "biggest_expense": _biggest_expense,
    "category_breakdown": _category_breakdown,
    "recent_transactions": _recent_transactions,
    "loan_list": _loan_list,
    "loan_emi": _loan_emi,
    "loan_remaining": _loan_remaining,
    "compare_months": _compare_months,
    "financial_summary": _financial_summary,
    "help": _help,
    "greeting": _greeting,
}


def rule_based_answer(user, message, context, intent):
    """Deterministic, offline, always-available answers."""
    if intent == "category_spend":
        return _category_spend(user, message, context)
    if intent == "banking_knowledge":
        return _knowledge(message)
    if intent in ("loan_info", "emi_calculator"):
        if "emi" in normalise(message) and "loan" not in normalise(message):
            return _knowledge("emi")
        return _loan_list(context)
    handler = RULE_ANSWERS.get(intent)
    if handler:
        return handler(context)
    return _unknown(context)


# ------------------------------------------------------------------ LLM hook --
def llm_answer(user, message, context, intent):
    """Optional natural-language layer.

    Kept deliberately small: the prompt is grounded with the retrieved demo data
    so an external model can never invent balances. If anything fails we silently
    return None and the caller falls back to the rule based answer.
    """
    api_key = getattr(settings, "OPENAI_API_KEY", "")
    if not api_key or getattr(settings, "AI_PROVIDER", "fallback") != "openai":
        return None
    try:
        import urllib.request

        payload = {
            "model": getattr(settings, "OPENAI_MODEL", "gpt-4o-mini"),
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are BankFlow AI, a demo banking assistant. Answer only using the "
                        "JSON customer data provided. Use Indian rupee formatting. Never invent "
                        "numbers and never mention real banking actions.\n\n"
                        f"Customer data:\n{json.dumps(context, default=str)}"
                    ),
                },
                {"role": "user", "content": message},
            ],
            "temperature": 0.2,
        }
        request = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",
            data=json.dumps(payload).encode(),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
        )
        with urllib.request.urlopen(request, timeout=20) as response:
            body = json.loads(response.read().decode())
        text = body["choices"][0]["message"]["content"].strip()
        return {"response": text, "type": intent, "data": None}
    except Exception:  # noqa: BLE001 - the demo must never break because of the API
        return None


def answer(user, message):
    """Main entry point used by POST /api/assistant/chat/."""
    context = build_context(user)
    intent = detect_intent(message)
    result = llm_answer(user, message, context, intent)
    provider = "openai" if result else "fallback"
    if result is None:
        result = rule_based_answer(user, message, context, intent)
    result["provider"] = provider
    result["intent"] = intent
    return result


def suggested_questions():
    return [
        "What is my current balance?",
        "How much did I spend this month?",
        "What was my biggest expense?",
        "How much did I spend on food?",
        "Show my recent transactions",
        "What loans do I have?",
        "What is my EMI?",
        "How much loan amount is remaining?",
        "Compare this month with last month",
        "Show my spending categories",
        "Give me a summary of my spending",
        "Explain EMI",
        "What is KYC?",
        "What is a credit score?",
    ]
```

### backend/assistant/serializers.py

```python
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
```

### backend/assistant/views.py

```python
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
```

### backend/assistant/urls.py

```python
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
```

### backend/assistant/admin.py

```python
from django.contrib import admin

from .models import ChatMessage


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("user", "message", "response_type", "provider", "created_at")
    list_filter = ("response_type", "provider")
    search_fields = ("message", "response", "user__email", "user__name")
```

### backend/assistant/tests.py

```python
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from banking.services import bootstrap_customer, calculate_emi, record_transaction

from .models import ChatMessage

User = get_user_model()


class AssistantTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="ai@bankflow.com", password="Demo@12345", name="Mohammed Adnan"
        )
        account = bootstrap_customer(self.user)
        now = timezone.now()
        record_transaction(account, amount=45000, description="Salary", category="Salary",
                           transaction_type="CREDIT", when=now - timedelta(days=2))
        record_transaction(account, amount=7200, description="Croma", category="Shopping",
                           transaction_type="DEBIT", when=now - timedelta(days=3))
        account.balance = 85450
        account.save()
        self.client.force_authenticate(self.user)

    def ask(self, message):
        return self.client.post("/api/assistant/chat/", {"message": message})

    def test_balance_question(self):
        response = self.ask("What is my current balance?")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["type"], "account_balance")
        self.assertIn("85,450", response.data["response"])

    def test_expense_question(self):
        response = self.ask("How much did I spend this month?")
        self.assertEqual(response.data["type"], "expense_summary")
        self.assertEqual(response.data["data"]["amount"], 7200.0)

    def test_biggest_expense_question(self):
        response = self.ask("What was my biggest expense?")
        self.assertEqual(response.data["type"], "biggest_expense")
        self.assertIn("Shopping", response.data["response"])

    def test_emi_knowledge_question(self):
        response = self.ask("Explain EMI")
        self.assertEqual(response.data["type"], "banking_knowledge")
        self.assertIn("Equated Monthly Instalment", response.data["response"])

    def test_transaction_question(self):
        response = self.ask("Show my recent transactions")
        self.assertEqual(response.data["type"], "recent_transactions")
        self.assertIn("Salary", response.data["response"])

    def test_category_spend_question(self):
        response = self.ask("How much did I spend on shopping?")
        self.assertEqual(response.data["type"], "category_spend")
        self.assertIn("7,200", response.data["response"])

    def test_loan_questions_with_seeded_loan(self):
        from banking.models import Loan

        Loan.objects.create(
            user=self.user, loan_type="HOME", amount=1500000, interest_rate=8.5,
            tenure_months=180, emi=calculate_emi(1500000, 8.5, 180)["monthly_emi"],
            remaining_amount=975000, status="ACTIVE",
        )
        loans = self.ask("What loans do I have?")
        self.assertEqual(loans.data["type"], "loan_list")
        self.assertIn("Home Loan", loans.data["response"])

        emi = self.ask("What is my EMI?")
        self.assertEqual(emi.data["type"], "loan_emi")

        remaining = self.ask("How much loan amount is remaining?")
        self.assertEqual(remaining.data["type"], "loan_remaining")

    def test_history_is_saved(self):
        self.ask("What is my balance?")
        self.ask("Explain KYC")
        history = self.client.get("/api/assistant/history/")
        self.assertEqual(history.status_code, status.HTTP_200_OK)
        self.assertEqual(history.data["count"], 2)
        self.assertEqual(ChatMessage.objects.filter(user=self.user).count(), 2)
        self.assertIn("suggestions", history.data)

    def test_unknown_question_is_handled(self):
        response = self.ask("Tell me a joke about penguins")
        self.assertEqual(response.data["type"], "unknown")
        self.assertIn("demo banking data", response.data["response"])

    def test_monitor_endpoint_is_admin_only(self):
        self.assertEqual(self.client.get("/api/assistant/monitor/").status_code,
                         status.HTTP_403_FORBIDDEN)
        self.user.role = User.Role.ADMIN
        self.user.save()
        self.assertEqual(self.client.get("/api/assistant/monitor/").status_code,
                         status.HTTP_200_OK)
```

## 5. FRONTEND - PROJECT CONFIGURATION

### frontend/package.json

```json
{
  "name": "bankflow-frontend",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "description": "BankFlow - AI Banking Assistant (React + Vite + MUI frontend)",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext js,jsx --report-unused-disable-directives"
  },
  "dependencies": {
    "@emotion/react": "^11.13.0",
    "@emotion/styled": "^11.13.0",
    "@mui/icons-material": "^5.16.7",
    "@mui/material": "^5.16.7",
    "axios": "^1.7.7",
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "react-icons": "^5.3.0",
    "react-router-dom": "^6.26.2",
    "recharts": "^2.12.7"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.3.1",
    "vite": "^5.4.8"
  }
}
```

### frontend/vite.config.js

```javascript
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    open: true,
  },
  build: {
    outDir: "dist",
    sourcemap: false,
  },
});
```

### frontend/index.html

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/bankflow.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta
      name="description"
      content="BankFlow - AI Banking Assistant. A React + Django demo banking application."
    />
    <title>BankFlow - AI Banking Assistant</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
```

### frontend/.env.example

```text
# Copy to .env and adjust if your Django server runs elsewhere.
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

### frontend/public/bankflow.svg

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <rect width="64" height="64" rx="14" fill="#1b3a8f" />
  <path d="M12 26 L32 12 L52 26 L52 32 L12 32 Z" fill="#4fc3f7" />
  <rect x="16" y="34" width="6" height="16" fill="#ffffff" />
  <rect x="29" y="34" width="6" height="16" fill="#ffffff" />
  <rect x="42" y="34" width="6" height="16" fill="#ffffff" />
  <rect x="12" y="50" width="40" height="4" fill="#4fc3f7" />
</svg>
```

## 6. FRONTEND - APP CORE, CONTEXT, SERVICES, UTILS

### frontend/src/main.jsx

```jsx
import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { CssBaseline, ThemeProvider } from "@mui/material";

import App from "./App.jsx";
import { AuthProvider } from "./context/AuthContext.jsx";
import theme from "./theme.js";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <CssBaseline />
      {/* The future flags remove the React Router v7 upgrade warnings in the console. */}
      <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
        <AuthProvider>
          <App />
        </AuthProvider>
      </BrowserRouter>
    </ThemeProvider>
  </React.StrictMode>
);
```

### frontend/src/App.jsx

```jsx
import { Route, Routes } from "react-router-dom";

import AppLayout from "./components/AppLayout.jsx";
import ProtectedRoute from "./components/ProtectedRoute.jsx";

import Landing from "./pages/Landing.jsx";
import Login from "./pages/Login.jsx";
import Register from "./pages/Register.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import Account from "./pages/Account.jsx";
import Transactions from "./pages/Transactions.jsx";
import TransactionDetails from "./pages/TransactionDetails.jsx";
import Loans from "./pages/Loans.jsx";
import LoanDetails from "./pages/LoanDetails.jsx";
import EMICalculator from "./pages/EMICalculator.jsx";
import AIAssistant from "./pages/AIAssistant.jsx";
import Notifications from "./pages/Notifications.jsx";
import Profile from "./pages/Profile.jsx";
import NotFound from "./pages/NotFound.jsx";

import AdminDashboard from "./pages/admin/AdminDashboard.jsx";
import CustomerManagement from "./pages/admin/CustomerManagement.jsx";
import TransactionManagement from "./pages/admin/TransactionManagement.jsx";
import LoanManagement from "./pages/admin/LoanManagement.jsx";
import AdminAnalytics from "./pages/admin/AdminAnalytics.jsx";
import AIMonitor from "./pages/admin/AIMonitor.jsx";

/**
 * Route map
 * ─ public      : /, /login, /register
 * ─ customer    : everything inside the protected AppLayout
 * ─ bank staff  : /admin/* (role="ADMIN" guard)
 */
export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      <Route element={<ProtectedRoute />}>
        <Route element={<AppLayout />}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/account" element={<Account />} />
          <Route path="/transactions" element={<Transactions />} />
          <Route path="/transactions/:id" element={<TransactionDetails />} />
          <Route path="/loans" element={<Loans />} />
          <Route path="/loans/:id" element={<LoanDetails />} />
          <Route path="/emi-calculator" element={<EMICalculator />} />
          <Route path="/assistant" element={<AIAssistant />} />
          <Route path="/notifications" element={<Notifications />} />
          <Route path="/profile" element={<Profile />} />
        </Route>
      </Route>

      <Route element={<ProtectedRoute role="ADMIN" />}>
        <Route element={<AppLayout />}>
          <Route path="/admin" element={<AdminDashboard />} />
          <Route path="/admin/customers" element={<CustomerManagement />} />
          <Route path="/admin/transactions" element={<TransactionManagement />} />
          <Route path="/admin/loans" element={<LoanManagement />} />
          <Route path="/admin/analytics" element={<AdminAnalytics />} />
          <Route path="/admin/ai-monitor" element={<AIMonitor />} />
        </Route>
      </Route>

      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}
```

### frontend/src/theme.js

```javascript
import { createTheme } from "@mui/material/styles";

/**
 * BankFlow design tokens.
 * A light, professional banking palette: deep navy + trustworthy blue + teal accent.
 */
const theme = createTheme({
  palette: {
    mode: "light",
    primary: { main: "#1b3a8f", light: "#4361ee", dark: "#122a68", contrastText: "#ffffff" },
    secondary: { main: "#0ea5e9", contrastText: "#ffffff" },
    success: { main: "#16a34a" },
    error: { main: "#e11d48" },
    warning: { main: "#f59e0b" },
    info: { main: "#6366f1" },
    background: { default: "#f4f6fb", paper: "#ffffff" },
    text: { primary: "#111a2e", secondary: "#5a6478" },
    divider: "#e6e9f2",
  },
  shape: { borderRadius: 12 },
  typography: {
    fontFamily: '"Inter", "Segoe UI", Roboto, Helvetica, Arial, sans-serif',
    h1: { fontWeight: 800, letterSpacing: "-0.02em" },
    h2: { fontWeight: 800, letterSpacing: "-0.02em" },
    h3: { fontWeight: 700 },
    h4: { fontWeight: 700 },
    h5: { fontWeight: 700 },
    h6: { fontWeight: 700 },
    button: { textTransform: "none", fontWeight: 600 },
  },
  components: {
    MuiPaper: {
      styleOverrides: {
        root: { backgroundImage: "none" },
      },
    },
    MuiCard: {
      defaultProps: { elevation: 0 },
      styleOverrides: {
        root: {
          border: "1px solid #e6e9f2",
          boxShadow: "0 1px 2px rgba(17, 26, 46, 0.04), 0 8px 24px rgba(17, 26, 46, 0.04)",
        },
      },
    },
    MuiButton: {
      defaultProps: { disableElevation: true },
      styleOverrides: {
        root: { borderRadius: 10, paddingInline: 18 },
        containedPrimary: { "&:hover": { backgroundColor: "#122a68" } },
      },
    },
    MuiChip: { styleOverrides: { root: { fontWeight: 600 } } },
    MuiTableCell: {
      styleOverrides: {
        head: { fontWeight: 700, color: "#5a6478", backgroundColor: "#f8f9fd" },
      },
    },
    MuiAppBar: {
      defaultProps: { elevation: 0, color: "inherit" },
    },
  },
});

export default theme;
```

### frontend/src/index.css

```css
:root {
  color-scheme: light;
}

html,
body,
#root {
  height: 100%;
  margin: 0;
}

body {
  font-family: "Inter", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  background-color: #f4f6fb;
  -webkit-font-smoothing: antialiased;
}

a {
  text-decoration: none;
}

/* Thin, banking-style scrollbar */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-thumb {
  background: #c7cede;
  border-radius: 8px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

.fade-in {
  animation: fadeIn 0.25s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(6px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

### frontend/src/context/AuthContext.jsx

```jsx
import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";

import authService from "../services/authService";
import { tokenStore } from "../services/api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [booting, setBooting] = useState(true);

  const loadUser = useCallback(async () => {
    const profile = await authService.profile();
    setUser(profile.user);
    return profile;
  }, []);

  useEffect(() => {
    let active = true;
    (async () => {
      if (!tokenStore.getAccess()) {
        setBooting(false);
        return;
      }
      try {
        const profile = await authService.profile();
        if (active) setUser(profile.user);
      } catch {
        tokenStore.clear();
        if (active) setUser(null);
      } finally {
        if (active) setBooting(false);
      }
    })();
    return () => {
      active = false;
    };
  }, []);

  const login = useCallback(
    async (credentials) => {
      await authService.login(credentials);
      return loadUser();
    },
    [loadUser]
  );

  const register = useCallback((payload) => authService.register(payload), []);

  const logout = useCallback(() => {
    authService.logout();
    setUser(null);
  }, []);

  const value = useMemo(
    () => ({
      user,
      booting,
      login,
      register,
      logout,
      isAuthenticated: Boolean(user),
      isAdmin: user?.role === "ADMIN",
      reloadProfile: loadUser,
      setUser,
    }),
    [user, booting, login, register, logout, loadUser]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used inside an AuthProvider");
  }
  return context;
}
```

### frontend/src/services/api.js

```javascript
import axios from "axios";

/**
 * One axios instance for the whole app.
 * - adds the JWT access token to every request
 * - refreshes the token once when the API answers 401
 * - turns network problems into friendly messages
 */
export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api";

const ACCESS_KEY = "bankflow_access";
const REFRESH_KEY = "bankflow_refresh";

export const tokenStore = {
  getAccess: () => localStorage.getItem(ACCESS_KEY),
  getRefresh: () => localStorage.getItem(REFRESH_KEY),
  set: ({ access, refresh }) => {
    if (access) localStorage.setItem(ACCESS_KEY, access);
    if (refresh) localStorage.setItem(REFRESH_KEY, refresh);
  },
  clear: () => {
    localStorage.removeItem(ACCESS_KEY);
    localStorage.removeItem(REFRESH_KEY);
  },
};

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { "Content-Type": "application/json" },
  timeout: 20000,
});

api.interceptors.request.use((config) => {
  const access = tokenStore.getAccess();
  if (access) {
    config.headers.Authorization = `Bearer ${access}`;
  }
  return config;
});

let refreshPromise = null;

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const { response, config } = error;
    const isAuthCall = config?.url?.includes("/auth/login") || config?.url?.includes("/auth/refresh");

    if (response?.status === 401 && !config._retry && !isAuthCall && tokenStore.getRefresh()) {
      config._retry = true;
      try {
        refreshPromise =
          refreshPromise ||
          axios.post(`${API_BASE_URL}/auth/refresh/`, { refresh: tokenStore.getRefresh() });
        const { data } = await refreshPromise;
        refreshPromise = null;
        tokenStore.set({ access: data.access });
        config.headers.Authorization = `Bearer ${data.access}`;
        return api(config);
      } catch (refreshError) {
        refreshPromise = null;
        tokenStore.clear();
        window.location.href = "/login?session=expired";
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

/** Convert any axios failure into a single readable sentence. */
export function getErrorMessage(error) {
  if (!error) return "Something went wrong.";
  if (error.code === "ERR_NETWORK" || !error.response) {
    return "Cannot reach the BankFlow API. Is the Django server running on port 8000?";
  }
  const { data, status } = error.response;
  if (typeof data === "string") return data;
  if (data?.detail) return data.detail;
  if (data?.message) return data.message;
  if (Array.isArray(data?.non_field_errors) && data.non_field_errors.length) {
    return data.non_field_errors[0];
  }
  if (data && typeof data === "object") {
    const [field, messages] = Object.entries(data)[0] || [];
    if (field && Array.isArray(messages) && messages.length) {
      return `${field}: ${messages[0]}`;
    }
    if (field && typeof messages === "string") return `${field}: ${messages}`;
  }
  if (status === 404) return "We could not find that record in the demo data.";
  return "The request failed. Please try again.";
}

export default api;
```

### frontend/src/services/authService.js

```javascript
import api, { tokenStore } from "./api";

const authService = {
  async register(payload) {
    const { data } = await api.post("/auth/register/", payload);
    return data;
  },

  async login({ email, password }) {
    const { data } = await api.post("/auth/login/", { email, password });
    tokenStore.set(data);
    return data;
  },

  async profile() {
    const { data } = await api.get("/profile/");
    return data;
  },

  async updateProfile(payload) {
    const { data } = await api.put("/profile/", payload);
    return data;
  },

  logout() {
    tokenStore.clear();
  },
};

export default authService;
```

### frontend/src/services/bankingService.js

```javascript
import api from "./api";

const bankingService = {
  getDashboard: () => api.get("/dashboard/").then((r) => r.data),
  getAccount: () => api.get("/account/").then((r) => r.data),

  getTransactions: (params = {}) =>
    api.get("/transactions/", { params }).then((r) => r.data),
  getTransaction: (id) => api.get(`/transactions/${id}/`).then((r) => r.data),

  getLoans: (params = {}) => api.get("/loans/", { params }).then((r) => r.data),
  getLoan: (id) => api.get(`/loans/${id}/`).then((r) => r.data),
  applyLoan: (payload) => api.post("/loans/", payload).then((r) => r.data),

  calculateEmi: (payload) => api.post("/emi/", payload).then((r) => r.data),

  getNotifications: () => api.get("/notifications/").then((r) => r.data),
  markNotificationRead: (id, isRead = true) =>
    api.put(`/notifications/${id}/`, { is_read: isRead }).then((r) => r.data),
  markAllNotificationsRead: () =>
    api.post("/notifications/read-all/").then((r) => r.data),
};

export default bankingService;
```

### frontend/src/services/aiService.js

```javascript
import api from "./api";

const aiService = {
  chat: (message) => api.post("/assistant/chat/", { message }).then((r) => r.data),
  history: () => api.get("/assistant/history/").then((r) => r.data),
  suggestions: () => api.get("/assistant/suggestions/").then((r) => r.data),
  clearHistory: () => api.delete("/assistant/history/").then((r) => r.data),
};

export default aiService;
```

### frontend/src/services/adminService.js

```javascript
import api from "./api";

const adminService = {
  analytics: () => api.get("/admin/analytics/").then((r) => r.data),
  overview: () => api.get("/admin/analytics/overview/").then((r) => r.data),
  customers: (params = {}) => api.get("/admin/customers/", { params }).then((r) => r.data),
  customer: (id) => api.get(`/admin/customers/${id}/`).then((r) => r.data),
  transactions: (params = {}) =>
    api.get("/admin/transactions/", { params }).then((r) => r.data),
  loans: (params = {}) => api.get("/admin/loans/", { params }).then((r) => r.data),
  updateLoanStatus: (id, status) =>
    api.patch(`/admin/loans/${id}/`, { status }).then((r) => r.data),
  users: () => api.get("/admin/users/").then((r) => r.data),
  aiMonitor: (params = {}) => api.get("/assistant/monitor/", { params }).then((r) => r.data),
};

export default adminService;
```

### frontend/src/utils/formatCurrency.js

```javascript
/** Currency, date and text helpers used across every page. */

export function formatCurrency(value, { compact = false, decimals = 0 } = {}) {
  const amount = Number(value || 0);
  if (compact && Math.abs(amount) >= 10000000) {
    return `₹${(amount / 10000000).toFixed(2)} Cr`;
  }
  if (compact && Math.abs(amount) >= 100000) {
    return `₹${(amount / 100000).toFixed(2)} L`;
  }
  return `₹${amount.toLocaleString("en-IN", {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  })}`;
}

export function formatSignedCurrency(value, type) {
  const sign = type === "CREDIT" ? "+" : "-";
  return `${sign}${formatCurrency(Math.abs(Number(value || 0)))}`;
}

export function formatDate(value, { withTime = false } = {}) {
  if (!value) return "-";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "-";
  return date.toLocaleDateString("en-IN", {
    day: "2-digit",
    month: "short",
    year: "numeric",
    ...(withTime ? { hour: "2-digit", minute: "2-digit" } : {}),
  });
}

export function relativeTime(value) {
  if (!value) return "";
  const diff = Date.now() - new Date(value).getTime();
  const minutes = Math.round(diff / 60000);
  if (minutes < 1) return "just now";
  if (minutes < 60) return `${minutes} min ago`;
  const hours = Math.round(minutes / 60);
  if (hours < 24) return `${hours} hr ago`;
  const days = Math.round(hours / 24);
  if (days < 30) return `${days} day${days === 1 ? "" : "s"} ago`;
  return formatDate(value);
}

export function greeting(date = new Date()) {
  const hour = date.getHours();
  if (hour < 12) return "Good Morning";
  if (hour < 17) return "Good Afternoon";
  if (hour < 21) return "Good Evening";
  return "Good Night";
}

export function initials(name = "") {
  return name
    .split(" ")
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase())
    .join("");
}

export const TRANSACTION_CATEGORIES = [
  "Salary",
  "Food",
  "Shopping",
  "Travel",
  "Bills",
  "Entertainment",
  "Transfer",
  "Other",
];

export const LOAN_TYPES = [
  { value: "PERSONAL", label: "Personal Loan", defaultRate: 12.5, max: 1500000 },
  { value: "HOME", label: "Home Loan", defaultRate: 8.5, max: 10000000 },
  { value: "EDUCATION", label: "Education Loan", defaultRate: 7.25, max: 2500000 },
  { value: "VEHICLE", label: "Vehicle Loan", defaultRate: 9.75, max: 2000000 },
];

export const CATEGORY_COLORS = {
  Salary: "#16a34a",
  Food: "#f97316",
  Shopping: "#8b5cf6",
  Travel: "#0ea5e9",
  Bills: "#ef4444",
  Entertainment: "#ec4899",
  Transfer: "#64748b",
  Other: "#94a3b8",
};
```

### frontend/src/utils/calculations.js

```javascript
/** Client side helpers used by the EMI calculator for instant feedback. */

export function calculateEmi(principal, annualRate, months) {
  const p = Number(principal) || 0;
  const r = (Number(annualRate) || 0) / 12 / 100;
  const n = Number(months) || 1;
  const emi = r === 0 ? p / n : (p * r * (1 + r) ** n) / ((1 + r) ** n - 1);
  const totalPayment = emi * n;
  return {
    monthly_emi: Number(emi.toFixed(2)),
    total_interest: Number((totalPayment - p).toFixed(2)),
    total_payment: Number(totalPayment.toFixed(2)),
    principal: Number(p.toFixed(2)),
    interest_rate: Number(annualRate) || 0,
    tenure_months: n,
  };
}

export function amortisationSchedule(principal, annualRate, months, limit = 12) {
  const p = Number(principal) || 0;
  const r = (Number(annualRate) || 0) / 12 / 100;
  const n = Number(months) || 1;
  const emi = r === 0 ? p / n : (p * r * (1 + r) ** n) / ((1 + r) ** n - 1);
  let balance = p;
  const rows = [];
  for (let month = 1; month <= Math.min(n, limit); month += 1) {
    const interest = balance * r;
    const principalPart = emi - interest;
    balance -= principalPart;
    rows.push({
      month,
      emi: Number(emi.toFixed(2)),
      principal: Number(principalPart.toFixed(2)),
      interest: Number(interest.toFixed(2)),
      balance: Number(Math.max(balance, 0).toFixed(2)),
    });
  }
  return rows;
}

export function tenureLabel(months) {
  const years = Math.floor(months / 12);
  const rest = months % 12;
  if (!years) return `${rest} months`;
  if (!rest) return `${years} year${years > 1 ? "s" : ""}`;
  return `${years} yr ${rest} mo`;
}
```

## 7. FRONTEND - COMPONENTS

### frontend/src/components/AppLayout.jsx

```jsx
import { useState } from "react";
import { Box, Container } from "@mui/material";
import { Outlet } from "react-router-dom";

import Navbar from "./Navbar.jsx";
import Sidebar, { DRAWER_WIDTH } from "./Sidebar.jsx";

/** Shell used by every private page: responsive sidebar + app bar + content. */
export default function AppLayout() {
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <Box sx={{ display: "flex", minHeight: "100vh", backgroundColor: "background.default" }}>
      <Sidebar mobileOpen={mobileOpen} onClose={() => setMobileOpen(false)} />
      <Box sx={{ flexGrow: 1, width: { md: `calc(100% - ${DRAWER_WIDTH}px)` } }}>
        <Navbar onMenuClick={() => setMobileOpen(true)} />
        <Container maxWidth="xl" sx={{ py: { xs: 2, md: 3 }, px: { xs: 2, md: 3 } }}>
          <Outlet />
        </Container>
      </Box>
    </Box>
  );
}
```

### frontend/src/components/Navbar.jsx

```jsx
import { useEffect, useState } from "react";
import {
  AppBar,
  Avatar,
  Badge,
  Box,
  Chip,
  Divider,
  IconButton,
  Menu,
  MenuItem,
  Stack,
  Toolbar,
  Tooltip,
  Typography,
} from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import NotificationsNoneIcon from "@mui/icons-material/NotificationsNone";
import LogoutIcon from "@mui/icons-material/Logout";
import PersonOutlineIcon from "@mui/icons-material/PersonOutline";
import SmartToyIcon from "@mui/icons-material/SmartToy";
import { useLocation, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext.jsx";
import bankingService from "../services/bankingService";
import { initials } from "../utils/formatCurrency.js";

const TITLES = {
  "/dashboard": "Dashboard",
  "/account": "My Account",
  "/transactions": "Transactions",
  "/loans": "Loans",
  "/emi-calculator": "EMI Calculator",
  "/assistant": "AI Banking Assistant",
  "/notifications": "Notifications",
  "/profile": "Profile",
  "/admin": "Admin Dashboard",
  "/admin/customers": "Customer Management",
  "/admin/transactions": "Transaction Management",
  "/admin/loans": "Loan Management",
  "/admin/analytics": "Analytics",
  "/admin/ai-monitor": "AI Assistant Monitoring",
};

export default function Navbar({ onMenuClick }) {
  const { user, isAdmin, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [anchorEl, setAnchorEl] = useState(null);
  const [unread, setUnread] = useState(0);

  useEffect(() => {
    let cancelled = false;
    const load = async () => {
      try {
        const notifications = await bankingService.getNotifications();
        if (!cancelled) {
          setUnread(notifications.filter((item) => !item.is_read).length);
        }
      } catch {
        if (!cancelled) setUnread(0);
      }
    };
    load();
    const timer = setInterval(load, 60000);
    return () => {
      cancelled = true;
      clearInterval(timer);
    };
  }, [location.pathname]);

  const title = TITLES[location.pathname] || "BankFlow";

  const handleLogout = () => {
    setAnchorEl(null);
    logout();
    navigate("/login");
  };

  return (
    <AppBar
      position="sticky"
      sx={{
        backgroundColor: "rgba(255,255,255,.92)",
        backdropFilter: "blur(8px)",
        borderBottom: "1px solid #e6e9f2",
      }}
    >
      <Toolbar sx={{ gap: 1.5 }}>
        <IconButton edge="start" onClick={onMenuClick} sx={{ display: { md: "none" } }}>
          <MenuIcon />
        </IconButton>

        <Typography variant="h6" sx={{ flexGrow: 1, fontSize: { xs: 16, md: 18 } }}>
          {title}
        </Typography>

        <Tooltip title="Ask BankFlow AI">
          <IconButton onClick={() => navigate("/assistant")} sx={{ display: { xs: "none", sm: "inline-flex" } }}>
            <SmartToyIcon />
          </IconButton>
        </Tooltip>

        <Tooltip title="Notifications">
          <IconButton onClick={() => navigate("/notifications")}>
            <Badge color="error" badgeContent={unread} max={9}>
              <NotificationsNoneIcon />
            </Badge>
          </IconButton>
        </Tooltip>

        <Divider orientation="vertical" flexItem sx={{ my: 1.5 }} />

        <Stack
          direction="row"
          spacing={1}
          alignItems="center"
          onClick={(event) => setAnchorEl(event.currentTarget)}
          sx={{ cursor: "pointer", borderRadius: 2, px: 0.5, py: 0.5 }}
        >
          <Avatar sx={{ width: 34, height: 34, bgcolor: "primary.main", fontSize: 13 }}>
            {initials(user?.name || "BF")}
          </Avatar>
          <Box sx={{ display: { xs: "none", md: "block" } }}>
            <Typography variant="subtitle2" lineHeight={1.2}>
              {user?.name}
            </Typography>
            <Typography variant="caption" color="text.secondary">
              {isAdmin ? "Bank Employee" : "Customer"}
            </Typography>
          </Box>
        </Stack>

        <Menu anchorEl={anchorEl} open={Boolean(anchorEl)} onClose={() => setAnchorEl(null)}>
          <MenuItem disabled sx={{ opacity: "1 !important" }}>
            <Stack direction="row" spacing={1} alignItems="center">
              <Typography variant="body2">{user?.email}</Typography>
              <Chip size="small" label={isAdmin ? "ADMIN" : "CUSTOMER"} color="primary" />
            </Stack>
          </MenuItem>
          <Divider />
          <MenuItem
            onClick={() => {
              setAnchorEl(null);
              navigate("/profile");
            }}
          >
            <PersonOutlineIcon fontSize="small" style={{ marginRight: 10 }} /> My profile
          </MenuItem>
          <MenuItem onClick={handleLogout}>
            <LogoutIcon fontSize="small" style={{ marginRight: 10 }} /> Logout
          </MenuItem>
        </Menu>
      </Toolbar>
    </AppBar>
  );
}
```

### frontend/src/components/Sidebar.jsx

```jsx
import {
  Avatar,
  Box,
  Divider,
  Drawer,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Stack,
  Toolbar,
  Typography,
} from "@mui/material";
import DashboardIcon from "@mui/icons-material/Dashboard";
import AccountBalanceIcon from "@mui/icons-material/AccountBalance";
import ReceiptLongIcon from "@mui/icons-material/ReceiptLong";
import RequestQuoteIcon from "@mui/icons-material/RequestQuote";
import CalculateIcon from "@mui/icons-material/Calculate";
import SmartToyIcon from "@mui/icons-material/SmartToy";
import NotificationsIcon from "@mui/icons-material/Notifications";
import PersonIcon from "@mui/icons-material/Person";
import GroupIcon from "@mui/icons-material/Group";
import InsightsIcon from "@mui/icons-material/Insights";
import MonitorHeartIcon from "@mui/icons-material/MonitorHeart";
import AccountBalanceWalletIcon from "@mui/icons-material/AccountBalanceWallet";
import LogoutIcon from "@mui/icons-material/Logout";
import { NavLink, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext.jsx";
import { initials } from "../utils/formatCurrency.js";

export const DRAWER_WIDTH = 252;

const CUSTOMER_LINKS = [
  { to: "/dashboard", label: "Dashboard", icon: <DashboardIcon /> },
  { to: "/account", label: "My Account", icon: <AccountBalanceIcon /> },
  { to: "/transactions", label: "Transactions", icon: <ReceiptLongIcon /> },
  { to: "/loans", label: "Loans", icon: <RequestQuoteIcon /> },
  { to: "/emi-calculator", label: "EMI Calculator", icon: <CalculateIcon /> },
  { to: "/assistant", label: "AI Assistant", icon: <SmartToyIcon /> },
  { to: "/notifications", label: "Notifications", icon: <NotificationsIcon /> },
  { to: "/profile", label: "Profile", icon: <PersonIcon /> },
];

const ADMIN_LINKS = [
  { to: "/admin", label: "Admin Dashboard", icon: <DashboardIcon /> },
  { to: "/admin/customers", label: "Customers", icon: <GroupIcon /> },
  { to: "/admin/transactions", label: "Transactions", icon: <ReceiptLongIcon /> },
  { to: "/admin/loans", label: "Loan Management", icon: <RequestQuoteIcon /> },
  { to: "/admin/analytics", label: "Analytics", icon: <InsightsIcon /> },
  { to: "/admin/ai-monitor", label: "AI Monitoring", icon: <MonitorHeartIcon /> },
];

function SidebarContent({ onNavigate }) {
  const { user, isAdmin, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <Box sx={{ display: "flex", flexDirection: "column", height: "100%" }}>
      <Toolbar sx={{ px: 2 }}>
        <Stack direction="row" spacing={1.25} alignItems="center">
          <Box
            sx={{
              display: "grid",
              placeItems: "center",
              width: 36,
              height: 36,
              borderRadius: 2,
              backgroundColor: "primary.main",
              color: "#fff",
            }}
          >
            <AccountBalanceWalletIcon fontSize="small" />
          </Box>
          <Box>
            <Typography variant="subtitle1" fontWeight={800} lineHeight={1.1}>
              BankFlow
            </Typography>
            <Typography variant="caption" color="text.secondary">
              AI Banking Assistant
            </Typography>
          </Box>
        </Stack>
      </Toolbar>
      <Divider />

      <List sx={{ px: 1.5, py: 2, flexGrow: 1 }}>
        <Typography
          variant="overline"
          sx={{ px: 1.5, color: "text.secondary", fontWeight: 700 }}
        >
          Banking
        </Typography>
        {CUSTOMER_LINKS.map((link) => (
          <ListItemButton
            key={link.to}
            component={NavLink}
            to={link.to}
            onClick={onNavigate}
            sx={{
              borderRadius: 2,
              mb: 0.5,
              color: "text.secondary",
              "& .MuiListItemIcon-root": { color: "text.secondary", minWidth: 42 },
              "&.active": {
                backgroundColor: "#eef2fd",
                color: "primary.main",
                "& .MuiListItemIcon-root": { color: "primary.main" },
                "& .MuiListItemText-primary": { fontWeight: 700 },
              },
            }}
          >
            <ListItemIcon>{link.icon}</ListItemIcon>
            <ListItemText primaryTypographyProps={{ fontSize: 14 }} primary={link.label} />
          </ListItemButton>
        ))}

        {isAdmin && (
          <>
            <Typography
              variant="overline"
              sx={{ px: 1.5, mt: 2, display: "block", color: "text.secondary", fontWeight: 700 }}
            >
              Bank Employee
            </Typography>
            {ADMIN_LINKS.map((link) => (
              <ListItemButton
                key={link.to}
                component={NavLink}
                to={link.to}
                end={link.to === "/admin"}
                onClick={onNavigate}
                sx={{
                  borderRadius: 2,
                  mb: 0.5,
                  color: "text.secondary",
                  "& .MuiListItemIcon-root": { color: "text.secondary", minWidth: 42 },
                  "&.active": {
                    backgroundColor: "#eef2fd",
                    color: "primary.main",
                    "& .MuiListItemIcon-root": { color: "primary.main" },
                    "& .MuiListItemText-primary": { fontWeight: 700 },
                  },
                }}
              >
                <ListItemIcon>{link.icon}</ListItemIcon>
                <ListItemText primaryTypographyProps={{ fontSize: 14 }} primary={link.label} />
              </ListItemButton>
            ))}
          </>
        )}
      </List>

      <Divider />
      <Stack direction="row" spacing={1.5} alignItems="center" sx={{ p: 2 }}>
        <Avatar sx={{ bgcolor: "primary.main", width: 38, height: 38, fontSize: 14 }}>
          {initials(user?.name || "BF")}
        </Avatar>
        <Box sx={{ flexGrow: 1, minWidth: 0 }}>
          <Typography variant="subtitle2" noWrap>
            {user?.name || "Demo Customer"}
          </Typography>
          <Typography variant="caption" color="text.secondary" noWrap>
            {user?.email}
          </Typography>
        </Box>
        <ListItemButton
          onClick={handleLogout}
          sx={{ borderRadius: 2, minWidth: 40, justifyContent: "center", p: 1 }}
        >
          <LogoutIcon fontSize="small" />
        </ListItemButton>
      </Stack>
    </Box>
  );
}

export default function Sidebar({ mobileOpen, onClose }) {
  return (
    <Box component="nav" sx={{ width: { md: DRAWER_WIDTH }, flexShrink: { md: 0 } }}>
      <Drawer
        variant="temporary"
        open={mobileOpen}
        onClose={onClose}
        ModalProps={{ keepMounted: true }}
        sx={{
          display: { xs: "block", md: "none" },
          "& .MuiDrawer-paper": { width: DRAWER_WIDTH, boxSizing: "border-box" },
        }}
      >
        <SidebarContent onNavigate={onClose} />
      </Drawer>
      <Drawer
        variant="permanent"
        open
        sx={{
          display: { xs: "none", md: "block" },
          "& .MuiDrawer-paper": {
            width: DRAWER_WIDTH,
            boxSizing: "border-box",
            borderRight: "1px solid #e6e9f2",
          },
        }}
      >
        <SidebarContent />
      </Drawer>
    </Box>
  );
}
```

### frontend/src/components/DashboardCard.jsx

```jsx
import { Box, Card, CardContent, Stack, Typography } from "@mui/material";
import TrendingDownIcon from "@mui/icons-material/TrendingDown";
import TrendingUpIcon from "@mui/icons-material/TrendingUp";

/**
 * The four KPI cards on the dashboard (balance, income, expenses, loans).
 */
export default function DashboardCard({
  title,
  value,
  icon,
  caption,
  trend,
  color = "primary.main",
  gradient,
}) {
  return (
    <Card
      sx={{
        height: "100%",
        background: gradient || "#ffffff",
        color: gradient ? "#ffffff" : "inherit",
        transition: "transform 0.18s ease, box-shadow 0.18s ease",
        "&:hover": { transform: "translateY(-3px)", boxShadow: "0 14px 30px rgba(17,26,46,.12)" },
      }}
    >
      <CardContent>
        <Stack direction="row" justifyContent="space-between" alignItems="flex-start">
          <Typography
            variant="body2"
            sx={{ fontWeight: 600, color: gradient ? "rgba(255,255,255,.85)" : "text.secondary" }}
          >
            {title}
          </Typography>
          <Box
            sx={{
              display: "grid",
              placeItems: "center",
              width: 42,
              height: 42,
              borderRadius: 2,
              backgroundColor: gradient ? "rgba(255,255,255,.18)" : "#eef2fd",
              color: gradient ? "#ffffff" : color,
            }}
          >
            {icon}
          </Box>
        </Stack>
        <Typography variant="h5" sx={{ mt: 1.5, fontWeight: 800 }}>
          {value}
        </Typography>
        {(caption || trend !== undefined) && (
          <Stack direction="row" spacing={1} alignItems="center" sx={{ mt: 1 }}>
            {trend !== undefined && (
              <Stack
                direction="row"
                alignItems="center"
                spacing={0.5}
                sx={{
                  color: gradient
                    ? "#ffffff"
                    : trend > 0
                      ? "success.main"
                      : trend < 0
                        ? "error.main"
                        : "text.secondary",
                  fontWeight: 700,
                }}
              >
                {trend > 0 ? <TrendingUpIcon fontSize="small" /> : <TrendingDownIcon fontSize="small" />}
                <Typography variant="caption" fontWeight={700}>
                  {trend > 0 ? "+" : ""}
                  {trend}%
                </Typography>
              </Stack>
            )}
            {caption && (
              <Typography
                variant="caption"
                sx={{ color: gradient ? "rgba(255,255,255,.8)" : "text.secondary" }}
              >
                {caption}
              </Typography>
            )}
          </Stack>
        )}
      </CardContent>
    </Card>
  );
}
```

### frontend/src/components/TransactionTable.jsx

```jsx
import {
  Box,
  Chip,
  IconButton,
  Skeleton,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Tooltip,
  Typography,
} from "@mui/material";
import VisibilityIcon from "@mui/icons-material/Visibility";
import { useNavigate } from "react-router-dom";

import { formatCurrency, formatDate } from "../utils/formatCurrency.js";
import { EmptyState, StatusChip } from "./Common.jsx";

/**
 * Reusable transaction table. `showCustomer` and `basePath` let the admin pages
 * reuse exactly the same component as the customer page.
 */
export default function TransactionTable({
  transactions = [],
  loading = false,
  showCustomer = false,
  basePath = "/transactions",
  emptyTitle = "No transactions found",
  emptyDescription = "Try clearing the filters or searching for something else.",
}) {
  const navigate = useNavigate();

  if (loading) {
    return (
      <Box>
        {[0, 1, 2, 3, 4].map((row) => (
          <Skeleton key={row} height={48} sx={{ borderRadius: 1 }} />
        ))}
      </Box>
    );
  }

  if (!transactions.length) {
    return <EmptyState title={emptyTitle} description={emptyDescription} />;
  }

  return (
    <TableContainer>
      <Table size="small" sx={{ minWidth: 720 }}>
        <TableHead>
          <TableRow>
            <TableCell>Transaction ID</TableCell>
            <TableCell>Date</TableCell>
            {showCustomer && <TableCell>Customer</TableCell>}
            <TableCell>Description</TableCell>
            <TableCell>Category</TableCell>
            <TableCell>Type</TableCell>
            <TableCell align="right">Amount</TableCell>
            <TableCell>Status</TableCell>
            <TableCell align="right">Details</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {transactions.map((txn) => (
            <TableRow
              key={txn.id}
              hover
              sx={{ cursor: basePath === "/admin/transactions" ? "default" : "pointer" }}
              onClick={() => basePath !== "/admin/transactions" && navigate(`${basePath}/${txn.id}`)}
            >
              <TableCell>
                <Typography variant="caption" fontWeight={700}>
                  {txn.transaction_id}
                </Typography>
              </TableCell>
              <TableCell>{formatDate(txn.date)}</TableCell>
              {showCustomer && <TableCell>{txn.customer_name || txn.account_number}</TableCell>}
              <TableCell sx={{ maxWidth: 260 }}>{txn.description}</TableCell>
              <TableCell>
                <Chip size="small" variant="outlined" label={txn.category} />
              </TableCell>
              <TableCell>
                <Chip
                  size="small"
                  label={txn.transaction_type === "CREDIT" ? "Credit" : "Debit"}
                  color={txn.transaction_type === "CREDIT" ? "success" : "default"}
                  variant={txn.transaction_type === "CREDIT" ? "filled" : "outlined"}
                />
              </TableCell>
              <TableCell align="right">
                <Typography
                  fontWeight={700}
                  color={txn.transaction_type === "CREDIT" ? "success.main" : "text.primary"}
                >
                  {txn.transaction_type === "CREDIT" ? "+" : "-"}
                  {formatCurrency(txn.amount)}
                </Typography>
              </TableCell>
              <TableCell>
                <StatusChip status={txn.status} />
              </TableCell>
              <TableCell align="right">
                {basePath !== "/admin/transactions" && (
                  <Tooltip title="Open transaction details">
                    <IconButton size="small" onClick={(e) => {
                      e.stopPropagation();
                      navigate(`${basePath}/${txn.id}`);
                    }}>
                      <VisibilityIcon fontSize="small" />
                    </IconButton>
                  </Tooltip>
                )}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
```

### frontend/src/components/LoanCard.jsx

```jsx
import {
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Divider,
  LinearProgress,
  Stack,
  Typography,
} from "@mui/material";
import HomeWorkIcon from "@mui/icons-material/HomeWork";
import SchoolIcon from "@mui/icons-material/School";
import DirectionsCarIcon from "@mui/icons-material/DirectionsCar";
import PaidIcon from "@mui/icons-material/Paid";
import { useNavigate } from "react-router-dom";

import { formatCurrency, formatDate } from "../utils/formatCurrency.js";
import { StatusChip } from "./Common.jsx";

const ICONS = {
  HOME: <HomeWorkIcon />,
  EDUCATION: <SchoolIcon />,
  VEHICLE: <DirectionsCarIcon />,
  PERSONAL: <PaidIcon />,
};

export default function LoanCard({ loan, detailPath = "/loans" }) {
  const navigate = useNavigate();

  return (
    <Card sx={{ height: "100%" }}>
      <CardContent>
        <Stack direction="row" justifyContent="space-between" alignItems="flex-start">
          <Stack direction="row" spacing={1.5} alignItems="center">
            <Box
              sx={{
                display: "grid",
                placeItems: "center",
                width: 44,
                height: 44,
                borderRadius: 2,
                backgroundColor: "#eef2fd",
                color: "primary.main",
              }}
            >
              {ICONS[loan.loan_type] || <PaidIcon />}
            </Box>
            <Box>
              <Typography variant="subtitle1" fontWeight={700}>
                {loan.loan_type_display}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                {loan.loan_id} • applied {formatDate(loan.applied_at)}
              </Typography>
            </Box>
          </Stack>
          <StatusChip status={loan.status} />
        </Stack>

        <Stack direction="row" spacing={3} sx={{ mt: 2.5 }}>
          <Box>
            <Typography variant="caption" color="text.secondary">
              Loan amount
            </Typography>
            <Typography variant="h6">{formatCurrency(loan.amount, { compact: true })}</Typography>
          </Box>
          <Box>
            <Typography variant="caption" color="text.secondary">
              EMI
            </Typography>
            <Typography variant="h6">{formatCurrency(loan.emi)}</Typography>
          </Box>
          <Box>
            <Typography variant="caption" color="text.secondary">
              Interest
            </Typography>
            <Typography variant="h6">{loan.interest_rate}%</Typography>
          </Box>
        </Stack>

        <Divider sx={{ my: 2 }} />

        <Stack direction="row" justifyContent="space-between" sx={{ mb: 0.5 }}>
          <Typography variant="caption" color="text.secondary">
            Repaid {formatCurrency(loan.paid_amount)}
          </Typography>
          <Typography variant="caption" fontWeight={700}>
            {loan.progress_percent}%
          </Typography>
        </Stack>
        <LinearProgress
          variant="determinate"
          value={Math.min(loan.progress_percent, 100)}
          sx={{ height: 8, borderRadius: 4 }}
        />

        <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mt: 2 }}>
          <Chip
            size="small"
            variant="outlined"
            label={`${loan.tenure_months} months`}
          />
          <Button size="small" onClick={() => navigate(`${detailPath}/${loan.id}`)}>
            View details
          </Button>
        </Stack>
      </CardContent>
    </Card>
  );
}
```

### frontend/src/components/ChatMessage.jsx

```jsx
import { Avatar, Box, Chip, Paper, Stack, Typography } from "@mui/material";
import SmartToyIcon from "@mui/icons-material/SmartToy";
import PersonIcon from "@mui/icons-material/Person";

import { initials, relativeTime } from "../utils/formatCurrency.js";

/**
 * A single chat bubble. Used for both live answers and saved chat history.
 */
export default function ChatMessage({ message, sender = "ai", userName = "You", meta }) {
  const isUser = sender === "user";

  return (
    <Stack
      direction="row"
      spacing={1.5}
      justifyContent={isUser ? "flex-end" : "flex-start"}
      sx={{ mb: 2 }}
      className="fade-in"
    >
      {!isUser && (
        <Avatar sx={{ bgcolor: "primary.main", width: 36, height: 36 }}>
          <SmartToyIcon fontSize="small" />
        </Avatar>
      )}
      <Box sx={{ maxWidth: { xs: "85%", md: "70%" } }}>
        <Paper
          elevation={0}
          sx={{
            p: 1.75,
            borderRadius: 3,
            borderTopLeftRadius: isUser ? 12 : 4,
            borderTopRightRadius: isUser ? 4 : 12,
            backgroundColor: isUser ? "primary.main" : "#ffffff",
            color: isUser ? "#ffffff" : "text.primary",
            border: isUser ? "none" : "1px solid #e6e9f2",
            whiteSpace: "pre-line",
          }}
        >
          <Typography variant="body2" sx={{ lineHeight: 1.7 }}>
            {message}
          </Typography>
        </Paper>
        <Stack direction="row" spacing={0.75} alignItems="center" sx={{ mt: 0.5, px: 0.5 }}>
          <Typography variant="caption" color="text.secondary">
            {isUser ? userName : "BankFlow AI"}
          </Typography>
          {meta?.type && !isUser && (
            <Chip size="small" variant="outlined" label={meta.type.replace(/_/g, " ")} />
          )}
          {meta?.created_at && (
            <Typography variant="caption" color="text.secondary">
              {relativeTime(meta.created_at)}
            </Typography>
          )}
        </Stack>
      </Box>
      {isUser && (
        <Avatar sx={{ bgcolor: "#111a2e", width: 36, height: 36 }}>
          {isUser && userName && userName !== "You" ? initials(userName) : <PersonIcon fontSize="small" />}
        </Avatar>
      )}
    </Stack>
  );
}
```

### frontend/src/components/ProtectedRoute.jsx

```jsx
import { Box, CircularProgress } from "@mui/material";
import { Navigate, Outlet, useLocation } from "react-router-dom";

import { useAuth } from "../context/AuthContext.jsx";

/**
 * Route guard.
 * <ProtectedRoute />                    -> any logged in customer
 * <ProtectedRoute role="ADMIN" />       -> bank employee area only
 */
export default function ProtectedRoute({ role }) {
  const { isAuthenticated, isAdmin, booting } = useAuth();
  const location = useLocation();

  if (booting) {
    return (
      <Box sx={{ display: "grid", placeItems: "center", minHeight: "60vh" }}>
        <CircularProgress />
      </Box>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace state={{ from: location.pathname }} />;
  }

  if (role === "ADMIN" && !isAdmin) {
    return <Navigate to="/dashboard" replace />;
  }

  return <Outlet />;
}
```

### frontend/src/components/Common.jsx

```jsx
import {
  Alert,
  Box,
  Chip,
  CircularProgress,
  Paper,
  Stack,
  Typography,
} from "@mui/material";

/** Small shared building blocks used by every page. */

export function PageHeader({ title, subtitle, action }) {
  return (
    <Stack
      direction={{ xs: "column", sm: "row" }}
      justifyContent="space-between"
      alignItems={{ xs: "flex-start", sm: "center" }}
      spacing={2}
      sx={{ mb: 3 }}
    >
      <Box>
        <Typography variant="h5">{title}</Typography>
        {subtitle && (
          <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
            {subtitle}
          </Typography>
        )}
      </Box>
      {action}
    </Stack>
  );
}

export function Loader({ label = "Loading demo data...", minHeight = 240 }) {
  return (
    <Box sx={{ display: "grid", placeItems: "center", minHeight, gap: 2 }}>
      <CircularProgress size={32} />
      <Typography variant="body2" color="text.secondary">
        {label}
      </Typography>
    </Box>
  );
}

export function ErrorAlert({ message, onRetry }) {
  if (!message) return null;
  return (
    <Alert
      severity="error"
      sx={{ mb: 2, borderRadius: 2 }}
      action={
        onRetry ? (
          <Typography
            variant="button"
            sx={{ cursor: "pointer", textDecoration: "underline" }}
            onClick={onRetry}
          >
            Retry
          </Typography>
        ) : null
      }
    >
      {message}
    </Alert>
  );
}

export function EmptyState({ title, description, icon, action }) {
  return (
    <Paper
      variant="outlined"
      sx={{
        p: 4,
        textAlign: "center",
        borderRadius: 3,
        borderStyle: "dashed",
        backgroundColor: "#fbfcff",
      }}
    >
      {icon && <Box sx={{ fontSize: 40, color: "text.secondary", mb: 1 }}>{icon}</Box>}
      <Typography variant="subtitle1" fontWeight={700}>
        {title}
      </Typography>
      {description && (
        <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
          {description}
        </Typography>
      )}
      {action && <Box sx={{ mt: 2 }}>{action}</Box>}
    </Paper>
  );
}

const STATUS_STYLES = {
  COMPLETED: { color: "success", label: "Completed" },
  PENDING: { color: "warning", label: "Pending" },
  FAILED: { color: "error", label: "Failed" },
  ACTIVE: { color: "success", label: "Active" },
  APPROVED: { color: "info", label: "Approved" },
  REJECTED: { color: "error", label: "Rejected" },
  DORMANT: { color: "warning", label: "Dormant" },
  CLOSED: { color: "default", label: "Closed" },
};

export function StatusChip({ status, size = "small" }) {
  const style = STATUS_STYLES[status] || { color: "default", label: status };
  return (
    <Chip
      size={size}
      color={style.color}
      variant={style.color === "default" ? "outlined" : "filled"}
      label={style.label}
      sx={{ fontWeight: 600 }}
    />
  );
}

export function SectionCard({ title, subtitle, action, children, sx }) {
  return (
    <Paper
      variant="outlined"
      sx={{ p: { xs: 2, md: 2.5 }, borderRadius: 3, height: "100%", ...sx }}
    >
      <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 2 }}>
        <Box>
          <Typography variant="h6">{title}</Typography>
          {subtitle && (
            <Typography variant="body2" color="text.secondary">
              {subtitle}
            </Typography>
          )}
        </Box>
        {action}
      </Stack>
      {children}
    </Paper>
  );
}
```

## 8. FRONTEND - CUSTOMER PAGES

### frontend/src/pages/Landing.jsx

```jsx
import {
  AppBar,
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Container,
  Divider,
  Grid,
  IconButton,
  Stack,
  Toolbar,
  Typography,
} from "@mui/material";
import {
  FiArrowRight,
  FiBarChart2,
  FiBell,
  FiCheckCircle,
  FiLock,
  FiPieChart,
  FiSmartphone,
  FiTrendingUp,
  FiUserCheck,
  FiZap,
} from "react-icons/fi";
import AccountBalanceWalletIcon from "@mui/icons-material/AccountBalanceWallet";
import SmartToyIcon from "@mui/icons-material/SmartToy";
import { Link as RouterLink, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext.jsx";

const NAV_LINKS = [
  { label: "Home", href: "#home" },
  { label: "Features", href: "#features" },
  { label: "AI Assistant", href: "#assistant" },
  { label: "Security", href: "#security" },
  { label: "About", href: "#about" },
];

const FEATURES = [
  {
    icon: <FiZap size={22} />,
    title: "Smart Dashboard",
    text: "Balances, income, expenses and loans in one clean, glanceable view.",
  },
  {
    icon: <SmartToyIcon sx={{ fontSize: 22 }} />,
    title: "AI Banking Assistant",
    text: "Ask natural questions about your money and get grounded answers instantly.",
  },
  {
    icon: <FiBarChart2 size={22} />,
    title: "Transaction Analytics",
    text: "Monthly trends, category splits and income vs expense charts.",
  },
  {
    icon: <FiTrendingUp size={22} />,
    title: "Loan Management",
    text: "Apply for demo loans, track EMI, outstanding amount and status.",
  },
  {
    icon: <FiLock size={22} />,
    title: "Secure Authentication",
    text: "JWT login, protected APIs and role based access for bank staff.",
  },
  {
    icon: <FiPieChart size={22} />,
    title: "Financial Insights",
    text: "Understand spending patterns with AI generated summaries.",
  },
];

const DEMO_CHAT = [
  { role: "user", text: "What is my current balance?" },
  { role: "ai", text: "Your current available balance is ₹85,450." },
  { role: "user", text: "How much did I spend this month?" },
  { role: "ai", text: "You spent ₹18,450 this month." },
  { role: "user", text: "What was my biggest expense?" },
  { role: "ai", text: "Your largest expense this month was Shopping at ₹7,200." },
];

export default function Landing() {
  const navigate = useNavigate();
  const { isAuthenticated, isAdmin } = useAuth();

  const goToApp = () => navigate(isAuthenticated ? (isAdmin ? "/admin" : "/dashboard") : "/login");

  return (
    <Box id="home" sx={{ backgroundColor: "#ffffff" }}>
      {/* ------------------------------------------------------------ navbar */}
      <AppBar
        position="sticky"
        sx={{
          backgroundColor: "rgba(255,255,255,.94)",
          backdropFilter: "blur(10px)",
          borderBottom: "1px solid #e6e9f2",
        }}
      >
        <Container maxWidth="lg">
          <Toolbar disableGutters sx={{ gap: 2 }}>
            <Stack direction="row" spacing={1.25} alignItems="center" sx={{ flexGrow: 1 }}>
              <Box
                sx={{
                  display: "grid",
                  placeItems: "center",
                  width: 38,
                  height: 38,
                  borderRadius: 2,
                  backgroundColor: "primary.main",
                  color: "#fff",
                }}
              >
                <AccountBalanceWalletIcon fontSize="small" />
              </Box>
              <Box>
                <Typography variant="subtitle1" fontWeight={800} lineHeight={1.1}>
                  BankFlow
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  AI Banking Assistant
                </Typography>
              </Box>
            </Stack>

            <Stack direction="row" spacing={3} sx={{ display: { xs: "none", md: "flex" } }}>
              {NAV_LINKS.map((link) => (
                <Typography
                  key={link.label}
                  component="a"
                  href={link.href}
                  variant="body2"
                  sx={{
                    color: "text.secondary",
                    fontWeight: 600,
                    "&:hover": { color: "primary.main" },
                  }}
                >
                  {link.label}
                </Typography>
              ))}
            </Stack>

            <Button component={RouterLink} to="/login" sx={{ display: { xs: "none", sm: "flex" } }}>
              Login
            </Button>
            <Button variant="contained" onClick={() => (isAuthenticated ? goToApp() : navigate("/register"))}>
              {isAuthenticated ? "Open App" : "Register"}
            </Button>
          </Toolbar>
        </Container>
      </AppBar>

      {/* -------------------------------------------------------------- hero */}
      <Box
        sx={{
          background:
            "radial-gradient(1200px 520px at 15% 0%, #e8eefc 0%, #ffffff 60%), linear-gradient(180deg, #fbfcff 0%, #ffffff 100%)",
          py: { xs: 6, md: 10 },
        }}
      >
        <Container maxWidth="lg">
          <Grid container spacing={6} alignItems="center">
            <Grid item xs={12} md={6}>
              <Chip
                label="Demo application • simulated data only"
                color="primary"
                variant="outlined"
                sx={{ mb: 2 }}
              />
              <Typography variant="h2" sx={{ fontSize: { xs: 32, md: 46 }, lineHeight: 1.15 }}>
                Your Smarter Digital Banking Experience
              </Typography>
              <Typography variant="h6" color="text.secondary" sx={{ mt: 2, fontWeight: 400 }}>
                Manage your finances, understand your spending and get instant assistance with our
                AI-powered banking assistant.
              </Typography>
              <Stack direction={{ xs: "column", sm: "row" }} spacing={2} sx={{ mt: 4 }}>
                <Button
                  variant="contained"
                  size="large"
                  endIcon={<FiArrowRight />}
                  onClick={goToApp}
                >
                  Get Started
                </Button>
                <Button
                  size="large"
                  variant="outlined"
                  component="a"
                  href="#features"
                >
                  Explore Features
                </Button>
              </Stack>
              <Stack direction="row" spacing={3} sx={{ mt: 4, flexWrap: "wrap", gap: 1 }}>
                {["JWT secured", "Role based access", "Works offline"].map((item) => (
                  <Stack key={item} direction="row" spacing={0.75} alignItems="center">
                    <FiCheckCircle color="#16a34a" />
                    <Typography variant="body2" color="text.secondary">
                      {item}
                    </Typography>
                  </Stack>
                ))}
              </Stack>
            </Grid>

            <Grid item xs={12} md={6}>
              <Card sx={{ borderRadius: 4 }}>
                <CardContent sx={{ p: 3 }}>
                  <Stack direction="row" justifyContent="space-between" alignItems="center">
                    <Stack direction="row" spacing={1.5} alignItems="center">
                      <Box
                        sx={{
                          display: "grid",
                          placeItems: "center",
                          width: 40,
                          height: 40,
                          borderRadius: 2,
                          backgroundColor: "#eef2fd",
                          color: "primary.main",
                        }}
                      >
                        <SmartToyIcon fontSize="small" />
                      </Box>
                      <Box>
                        <Typography variant="subtitle1" fontWeight={700}>
                          BankFlow AI
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          Always-on demo assistant
                        </Typography>
                      </Box>
                    </Stack>
                    <Chip size="small" color="success" label="online" />
                  </Stack>

                  <Divider sx={{ my: 2 }} />

                  {DEMO_CHAT.map((line) => (
                    <Box
                      key={line.text}
                      sx={{
                        display: "flex",
                        justifyContent: line.role === "user" ? "flex-end" : "flex-start",
                        mb: 1.25,
                      }}
                    >
                      <Box
                        sx={{
                          px: 1.75,
                          py: 1,
                          borderRadius: 3,
                          maxWidth: "85%",
                          fontSize: 14,
                          backgroundColor: line.role === "user" ? "primary.main" : "#f4f6fb",
                          color: line.role === "user" ? "#fff" : "text.primary",
                        }}
                      >
                        {line.text}
                      </Box>
                    </Box>
                  ))}

                  <Button fullWidth variant="contained" sx={{ mt: 2 }} onClick={goToApp}>
                    Try the assistant
                  </Button>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Container>
      </Box>

      {/* ---------------------------------------------------------- features */}
      <Container maxWidth="lg" id="features" sx={{ py: { xs: 6, md: 9 } }}>
        <Stack alignItems="center" sx={{ textAlign: "center", mb: 5 }}>
          <Typography variant="h3" sx={{ fontSize: { xs: 26, md: 34 } }}>
            Everything a modern banking demo needs
          </Typography>
          <Typography color="text.secondary" sx={{ mt: 1.5, maxWidth: 620 }}>
            BankFlow demonstrates React, Django REST Framework, JWT, charts and an AI assistant
            working together on completely fictional data.
          </Typography>
        </Stack>

        <Grid container spacing={3}>
          {FEATURES.map((feature) => (
            <Grid item xs={12} sm={6} md={4} key={feature.title}>
              <Card sx={{ height: "100%", transition: "transform .18s ease", "&:hover": { transform: "translateY(-4px)" } }}>
                <CardContent>
                  <Box
                    sx={{
                      display: "grid",
                      placeItems: "center",
                      width: 46,
                      height: 46,
                      borderRadius: 2,
                      color: "primary.main",
                      backgroundColor: "#eef2fd",
                      mb: 2,
                    }}
                  >
                    {feature.icon}
                  </Box>
                  <Typography variant="h6" sx={{ mb: 0.5 }}>
                    {feature.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {feature.text}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Container>

      {/* --------------------------------------------------------- assistant */}
      <Box id="assistant" sx={{ backgroundColor: "#f7f9ff", py: { xs: 6, md: 9 } }}>
        <Container maxWidth="lg">
          <Grid container spacing={5} alignItems="center">
            <Grid item xs={12} md={6}>
              <Typography variant="h3" sx={{ fontSize: { xs: 26, md: 32 } }}>
                An assistant that actually understands your data
              </Typography>
              <Typography color="text.secondary" sx={{ mt: 2 }}>
                Questions are mapped to an intent, the relevant demo banking data is retrieved, and
                the answer is generated from that data — never invented. If no external AI key is
                configured, the built-in rule based engine answers anyway.
              </Typography>
              <Stack spacing={1.5} sx={{ mt: 3 }}>
                {[
                  "What is my balance?",
                  "How much did I spend on food?",
                  "What loans do I have?",
                  "Explain EMI / KYC / credit score",
                ].map((q) => (
                  <Stack key={q} direction="row" spacing={1.25} alignItems="center">
                    <FiCheckCircle color="#1b3a8f" />
                    <Typography variant="body2">{q}</Typography>
                  </Stack>
                ))}
              </Stack>
            </Grid>
            <Grid item xs={12} md={6}>
              <Card sx={{ backgroundColor: "#0f1d3d", color: "#fff", borderRadius: 4 }}>
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h6" sx={{ mb: 2 }}>
                    Example AI session
                  </Typography>
                  {[
                    ["You", "What was my biggest expense?"],
                    ["BankFlow AI", "Your largest expense this month was Shopping at ₹7,200."],
                    ["You", "What loans do I have?"],
                    ["BankFlow AI", "You currently have 2 active demo loans: Home Loan and Vehicle Loan."],
                  ].map(([who, text]) => (
                    <Box key={text} sx={{ mb: 1.5 }}>
                      <Typography variant="caption" sx={{ color: "rgba(255,255,255,.6)" }}>
                        {who}
                      </Typography>
                      <Typography variant="body2">{text}</Typography>
                    </Box>
                  ))}
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Container>
      </Box>

      {/* ---------------------------------------------------------- security */}
      <Container maxWidth="lg" id="security" sx={{ py: { xs: 6, md: 9 } }}>
        <Grid container spacing={4}>
          <Grid item xs={12} md={4}>
            <Typography variant="h4" sx={{ fontSize: { xs: 24, md: 30 } }}>
              Built with security basics from day one
            </Typography>
            <Typography color="text.secondary" sx={{ mt: 1.5 }}>
              This is a demonstration project, but it still shows the patterns a real banking
              application would follow.
            </Typography>
          </Grid>
          <Grid item xs={12} md={8}>
            <Grid container spacing={2}>
              {[
                { icon: <FiLock />, title: "JWT authentication", text: "Access + refresh tokens with automatic refresh on 401." },
                { icon: <FiUserCheck />, title: "Role based access", text: "Customer routes and bank employee routes are separated." },
                { icon: <FiSmartphone />, title: "Responsive by default", text: "Desktop, laptop, tablet and mobile layouts." },
                { icon: <FiBell />, title: "Simulated notifications", text: "Salary, security and loan updates with read state." },
              ].map((item) => (
                <Grid item xs={12} sm={6} key={item.title}>
                  <Box sx={{ p: 2.5, borderRadius: 3, border: "1px solid #e6e9f2", height: "100%" }}>
                    <Stack direction="row" spacing={1.5} alignItems="center" sx={{ mb: 1 }}>
                      <Box sx={{ color: "primary.main" }}>{item.icon}</Box>
                      <Typography variant="subtitle2">{item.title}</Typography>
                    </Stack>
                    <Typography variant="body2" color="text.secondary">
                      {item.text}
                    </Typography>
                  </Box>
                </Grid>
              ))}
            </Grid>
          </Grid>
        </Grid>
      </Container>

      {/* ------------------------------------------------------------- about */}
      <Box id="about" sx={{ backgroundColor: "#f7f9ff", py: { xs: 6, md: 8 } }}>
        <Container maxWidth="lg">
          <Grid container spacing={4} alignItems="center">
            <Grid item xs={12} md={7}>
              <Typography variant="h4" sx={{ fontSize: { xs: 24, md: 30 } }}>
                BankFlow - AI Banking Assistant
              </Typography>
              <Typography color="text.secondary" sx={{ mt: 1.5 }}>
                A full-stack reference project: React + Vite + Material UI on the frontend,
                Django REST Framework with JWT on the backend, Recharts for analytics and a modular
                AI service that can run rule based or be pointed at an LLM.
              </Typography>
              <Typography color="text.secondary" sx={{ mt: 1.5 }}>
                <strong>Important:</strong> every account, transaction and loan in this application
                is fictional. No real money movement, payments or banking operations are performed.
              </Typography>
            </Grid>
            <Grid item xs={12} md={5}>
              <Card>
                <CardContent>
                  <Typography variant="subtitle1" fontWeight={700} sx={{ mb: 1.5 }}>
                    Demo logins
                  </Typography>
                  {[
                    ["Customer", "mohammed@bankflow.com", "Demo@12345"],
                    ["Bank employee", "admin@bankflow.com", "Admin@12345"],
                  ].map(([role, email, password]) => (
                    <Box key={email} sx={{ mb: 1.5 }}>
                      <Typography variant="caption" color="text.secondary">
                        {role}
                      </Typography>
                      <Stack direction="row" spacing={1} alignItems="center" sx={{ flexWrap: "wrap" }}>
                        <Chip size="small" label={email} variant="outlined" />
                        <Chip size="small" label={password} variant="outlined" />
                      </Stack>
                    </Box>
                  ))}
                  <Button fullWidth variant="contained" sx={{ mt: 1 }} onClick={() => navigate("/login")}>
                    Login to the demo
                  </Button>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Container>
      </Box>

      {/* ------------------------------------------------------------ footer */}
      <Box sx={{ backgroundColor: "#0f1d3d", color: "#fff", py: 4 }}>
        <Container maxWidth="lg">
          <Stack direction={{ xs: "column", md: "row" }} justifyContent="space-between" spacing={2}>
            <Stack direction="row" spacing={1.25} alignItems="center">
              <IconButton size="small" sx={{ color: "#fff" }}>
                <AccountBalanceWalletIcon fontSize="small" />
              </IconButton>
              <Typography variant="subtitle2">BankFlow - AI Banking Assistant (demo)</Typography>
            </Stack>
            <Stack direction="row" spacing={3} sx={{ flexWrap: "wrap" }}>
              {NAV_LINKS.map((link) => (
                <Typography
                  key={link.label}
                  component="a"
                  href={link.href}
                  variant="body2"
                  sx={{ color: "rgba(255,255,255,.75)", "&:hover": { color: "#fff" } }}
                >
                  {link.label}
                </Typography>
              ))}
            </Stack>
          </Stack>
          <Divider sx={{ my: 2, borderColor: "rgba(255,255,255,.15)" }} />
          <Typography variant="caption" sx={{ color: "rgba(255,255,255,.6)" }}>
            © {new Date().getFullYear()} BankFlow demo. All data is simulated and fictional. Built
            with React and Django REST Framework.
          </Typography>
        </Container>
      </Box>
    </Box>
  );
}
```

### frontend/src/pages/Login.jsx

```jsx
import { useEffect, useState } from "react";
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  IconButton,
  InputAdornment,
  Link,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import AccountBalanceWalletIcon from "@mui/icons-material/AccountBalanceWallet";
import VisibilityIcon from "@mui/icons-material/Visibility";
import VisibilityOffIcon from "@mui/icons-material/VisibilityOff";
import { Link as RouterLink, useLocation, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext.jsx";
import { getErrorMessage } from "../services/api";

const DEMO_ACCOUNTS = [
  { label: "Customer", email: "mohammed@bankflow.com", password: "Demo@12345" },
  { label: "Bank employee", email: "admin@bankflow.com", password: "Admin@12345" },
];

export default function Login() {
  const { login, isAuthenticated, isAdmin } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [form, setForm] = useState({ email: "", password: "" });
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const sessionExpired = new URLSearchParams(location.search).get("session") === "expired";

  useEffect(() => {
    if (isAuthenticated) {
      navigate(isAdmin ? "/admin" : "/dashboard", { replace: true });
    }
  }, [isAuthenticated, isAdmin, navigate]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");

    if (!form.email || !form.password) {
      setError("Please enter both your email and password.");
      return;
    }

    setLoading(true);
    try {
      const profile = await login(form);
      const target =
        profile?.user?.role === "ADMIN"
          ? "/admin"
          : location.state?.from && location.state.from !== "/login"
            ? location.state.from
            : "/dashboard";
      navigate(target, { replace: true });
    } catch (err) {
      setError(
        err?.response?.status === 401
          ? "Invalid email or password. Use one of the demo logins below."
          : getErrorMessage(err)
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box
      sx={{
        minHeight: "100vh",
        display: "grid",
        placeItems: "center",
        p: 2,
        background:
          "radial-gradient(900px 420px at 20% 10%, #e8eefc 0%, #ffffff 55%), #f4f6fb",
      }}
    >
      <Card sx={{ width: "100%", maxWidth: 440, borderRadius: 4 }}>
        <CardContent sx={{ p: { xs: 3, md: 4 } }}>
          <Stack direction="row" spacing={1.25} alignItems="center" sx={{ mb: 3 }}>
            <Box
              sx={{
                display: "grid",
                placeItems: "center",
                width: 40,
                height: 40,
                borderRadius: 2,
                backgroundColor: "primary.main",
                color: "#fff",
              }}
            >
              <AccountBalanceWalletIcon fontSize="small" />
            </Box>
            <Box>
              <Typography variant="subtitle1" fontWeight={800} lineHeight={1.1}>
                BankFlow
              </Typography>
              <Typography variant="caption" color="text.secondary">
                AI Banking Assistant
              </Typography>
            </Box>
          </Stack>

          <Typography variant="h5" sx={{ mb: 0.5 }}>
            Welcome back
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
            Login with a demo account to explore the dashboard.
          </Typography>

          {sessionExpired && (
            <Alert severity="warning" sx={{ mb: 2 }}>
              Your session expired. Please login again.
            </Alert>
          )}
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          <form onSubmit={handleSubmit} noValidate>
            <TextField
              fullWidth
              label="Email"
              type="email"
              autoComplete="email"
              value={form.email}
              onChange={(event) => setForm({ ...form, email: event.target.value })}
              sx={{ mb: 2 }}
            />
            <TextField
              fullWidth
              label="Password"
              type={showPassword ? "text" : "password"}
              autoComplete="current-password"
              value={form.password}
              onChange={(event) => setForm({ ...form, password: event.target.value })}
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton onClick={() => setShowPassword((prev) => !prev)} edge="end">
                      {showPassword ? <VisibilityOffIcon /> : <VisibilityIcon />}
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />

            <Button
              type="submit"
              fullWidth
              variant="contained"
              size="large"
              disabled={loading}
              sx={{ mt: 3 }}
              startIcon={loading ? <CircularProgress size={18} color="inherit" /> : null}
            >
              {loading ? "Signing in..." : "Login"}
            </Button>
          </form>

          <Typography variant="body2" color="text.secondary" sx={{ mt: 2, textAlign: "center" }}>
            New to BankFlow?{" "}
            <Link component={RouterLink} to="/register" fontWeight={700}>
              Create an account
            </Link>
          </Typography>

          <Box sx={{ mt: 3, p: 2, borderRadius: 3, backgroundColor: "#f8f9fd" }}>
            <Typography variant="caption" color="text.secondary" fontWeight={700}>
              DEMO LOGINS (click to autofill)
            </Typography>
            <Stack spacing={1} sx={{ mt: 1 }}>
              {DEMO_ACCOUNTS.map((account) => (
                <Stack
                  key={account.email}
                  direction="row"
                  spacing={1}
                  alignItems="center"
                  onClick={() => setForm({ email: account.email, password: account.password })}
                  sx={{ cursor: "pointer", flexWrap: "wrap" }}
                >
                  <Chip size="small" label={account.label} color="primary" variant="outlined" />
                  <Typography variant="caption">{account.email}</Typography>
                  <Typography variant="caption" color="text.secondary">
                    {account.password}
                  </Typography>
                </Stack>
              ))}
            </Stack>
          </Box>

          <Typography variant="caption" color="text.secondary" sx={{ display: "block", mt: 2 }}>
            This is a demo application with fictional data. Never enter real banking credentials.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
}
```

### frontend/src/pages/Register.jsx

```jsx
import { useState } from "react";
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  CircularProgress,
  Grid,
  Link,
  MenuItem,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import AccountBalanceWalletIcon from "@mui/icons-material/AccountBalanceWallet";
import CheckCircleOutlineIcon from "@mui/icons-material/CheckCircleOutline";
import { Link as RouterLink, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext.jsx";
import { getErrorMessage } from "../services/api";

const EMPLOYMENT_TYPES = [
  { value: "SALARIED", label: "Salaried" },
  { value: "SELF_EMPLOYED", label: "Self Employed" },
  { value: "STUDENT", label: "Student" },
  { value: "RETIRED", label: "Retired" },
  { value: "OTHER", label: "Other" },
];

const EMPTY_FORM = {
  name: "",
  email: "",
  phone: "",
  employment_type: "SALARIED",
  password: "",
  confirm_password: "",
};

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState(EMPTY_FORM);
  const [errors, setErrors] = useState({});
  const [apiError, setApiError] = useState("");
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);

  const update = (field) => (event) => setForm({ ...form, [field]: event.target.value });

  const validate = () => {
    const next = {};
    if (!form.name.trim()) next.name = "Full name is required.";
    if (!form.email.trim()) next.email = "Email is required.";
    else if (!/^\S+@\S+\.\S+$/.test(form.email)) next.email = "Enter a valid email address.";
    if (form.phone && !/^[+0-9\s-]{8,20}$/.test(form.phone)) {
      next.phone = "Enter a valid phone number.";
    }
    if (!form.password) next.password = "Password is required.";
    else if (form.password.length < 8) next.password = "Use at least 8 characters.";
    else if (/^\d+$/.test(form.password)) next.password = "Password cannot be only numbers.";
    if (form.confirm_password !== form.password) {
      next.confirm_password = "Passwords do not match.";
    }
    setErrors(next);
    return Object.keys(next).length === 0;
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setApiError("");
    if (!validate()) return;

    setLoading(true);
    try {
      await register(form);
      setSuccess(true);
      setForm(EMPTY_FORM);
      setTimeout(() => navigate("/login"), 1800);
    } catch (error) {
      setApiError(getErrorMessage(error));
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box
      sx={{
        minHeight: "100vh",
        display: "grid",
        placeItems: "center",
        p: 2,
        background:
          "radial-gradient(900px 420px at 80% 5%, #e8eefc 0%, #ffffff 55%), #f4f6fb",
      }}
    >
      <Card sx={{ width: "100%", maxWidth: 720, borderRadius: 4 }}>
        <CardContent sx={{ p: { xs: 3, md: 4 } }}>
          <Stack direction="row" spacing={1.25} alignItems="center" sx={{ mb: 3 }}>
            <Box
              sx={{
                display: "grid",
                placeItems: "center",
                width: 40,
                height: 40,
                borderRadius: 2,
                backgroundColor: "primary.main",
                color: "#fff",
              }}
            >
              <AccountBalanceWalletIcon fontSize="small" />
            </Box>
            <Box>
              <Typography variant="subtitle1" fontWeight={800} lineHeight={1.1}>
                BankFlow
              </Typography>
              <Typography variant="caption" color="text.secondary">
                Create your demo customer profile
              </Typography>
            </Box>
          </Stack>

          {success && (
            <Alert
              severity="success"
              icon={<CheckCircleOutlineIcon />}
              sx={{ mb: 2 }}
            >
              Registration successful. Redirecting you to the login page...
            </Alert>
          )}
          {apiError && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {apiError}
            </Alert>
          )}

          <form onSubmit={handleSubmit} noValidate>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  required
                  label="Full name"
                  value={form.name}
                  onChange={update("name")}
                  error={Boolean(errors.name)}
                  helperText={errors.name}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  required
                  label="Email"
                  type="email"
                  value={form.email}
                  onChange={update("email")}
                  error={Boolean(errors.email)}
                  helperText={errors.email}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Phone"
                  placeholder="+91 98765 43210"
                  value={form.phone}
                  onChange={update("phone")}
                  error={Boolean(errors.phone)}
                  helperText={errors.phone}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  select
                  label="Employment type"
                  value={form.employment_type}
                  onChange={update("employment_type")}
                >
                  {EMPLOYMENT_TYPES.map((option) => (
                    <MenuItem key={option.value} value={option.value}>
                      {option.label}
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  required
                  label="Password"
                  type="password"
                  value={form.password}
                  onChange={update("password")}
                  error={Boolean(errors.password)}
                  helperText={errors.password || "Minimum 8 characters."}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  required
                  label="Confirm password"
                  type="password"
                  value={form.confirm_password}
                  onChange={update("confirm_password")}
                  error={Boolean(errors.confirm_password)}
                  helperText={errors.confirm_password}
                />
              </Grid>
            </Grid>

            <Button
              type="submit"
              fullWidth
              variant="contained"
              size="large"
              disabled={loading}
              sx={{ mt: 3 }}
              startIcon={loading ? <CircularProgress size={18} color="inherit" /> : null}
            >
              {loading ? "Creating account..." : "Create demo account"}
            </Button>
          </form>

          <Typography variant="body2" color="text.secondary" sx={{ mt: 2, textAlign: "center" }}>
            Already registered?{" "}
            <Link component={RouterLink} to="/login" fontWeight={700}>
              Login instead
            </Link>
          </Typography>
          <Typography variant="caption" color="text.secondary" sx={{ display: "block", mt: 2 }}>
            New demo customers automatically get a simulated savings account and welcome
            notification. No real banking data is used or stored.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
}
```

### frontend/src/pages/Dashboard.jsx

```jsx
import { useCallback, useEffect, useState } from "react";
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Divider,
  Grid,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  Skeleton,
  Stack,
  Tab,
  Tabs,
  Typography,
} from "@mui/material";
import AccountBalanceWalletIcon from "@mui/icons-material/AccountBalanceWallet";
import TrendingUpIcon from "@mui/icons-material/TrendingUp";
import TrendingDownIcon from "@mui/icons-material/TrendingDown";
import RequestQuoteIcon from "@mui/icons-material/RequestQuote";
import ReceiptLongIcon from "@mui/icons-material/ReceiptLong";
import CalculateIcon from "@mui/icons-material/Calculate";
import SmartToyIcon from "@mui/icons-material/SmartToy";
import NotificationsActiveIcon from "@mui/icons-material/NotificationsActive";
import ArrowForwardIcon from "@mui/icons-material/ArrowForward";
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip as ChartTooltip,
  XAxis,
  YAxis,
} from "recharts";
import { useNavigate } from "react-router-dom";

import DashboardCard from "../components/DashboardCard.jsx";
import { EmptyState, ErrorAlert, Loader, PageHeader, SectionCard, StatusChip } from "../components/Common.jsx";
import { useAuth } from "../context/AuthContext.jsx";
import bankingService from "../services/bankingService";
import { getErrorMessage } from "../services/api";
import {
  CATEGORY_COLORS,
  formatCurrency,
  formatDate,
  greeting,
} from "../utils/formatCurrency.js";

const QUICK_ACTIONS = [
  { label: "View Transactions", icon: <ReceiptLongIcon />, to: "/transactions" },
  { label: "Apply for Loan", icon: <RequestQuoteIcon />, to: "/loans" },
  { label: "Ask AI Assistant", icon: <SmartToyIcon />, to: "/assistant" },
  { label: "EMI Calculator", icon: <CalculateIcon />, to: "/emi-calculator" },
];

export default function Dashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [trendTab, setTrendTab] = useState("both");

  const load = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const [dashboard, notif] = await Promise.all([
        bankingService.getDashboard(),
        bankingService.getNotifications(),
      ]);
      setData(dashboard);
      setNotifications(notif.slice(0, 4));
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  if (loading) return <Loader label="Loading your banking dashboard..." minHeight="60vh" />;

  if (error) {
    return (
      <>
        <PageHeader title="Dashboard" />
        <ErrorAlert message={error} onRetry={load} />
      </>
    );
  }

  const firstName = (user?.name || "Customer").split(" ")[0];
  const categories = data.spending_categories || [];
  const trend = data.monthly_trend || [];

  return (
    <Box>
      <PageHeader
        title={`${greeting()}, ${firstName}`}
        subtitle={`Here is your financial snapshot for ${new Date().toLocaleDateString("en-IN", {
          month: "long",
          year: "numeric",
        })}. All figures are simulated demo data.`}
        action={
          <Chip
            color="primary"
            variant="outlined"
            icon={<AccountBalanceWalletIcon />}
            label="Demo account"
          />
        }
      />

      {/* -------------------------------------------------------------- cards */}
      <Grid container spacing={2.5}>
        <Grid item xs={12} sm={6} lg={3}>
          <DashboardCard
            title="Available Balance"
            value={formatCurrency(data.balance)}
            icon={<AccountBalanceWalletIcon />}
            caption="Across all active demo accounts"
            gradient="linear-gradient(135deg, #1b3a8f 0%, #4361ee 100%)"
          />
        </Grid>
        <Grid item xs={12} sm={6} lg={3}>
          <DashboardCard
            title="Monthly Income"
            value={formatCurrency(data.monthly_income)}
            icon={<TrendingUpIcon />}
            caption="Salary and other credits"
            color="#16a34a"
          />
        </Grid>
        <Grid item xs={12} sm={6} lg={3}>
          <DashboardCard
            title="Monthly Expenses"
            value={formatCurrency(data.monthly_expenses)}
            icon={<TrendingDownIcon />}
            caption="vs last month"
            trend={data.expense_change_percent}
            color="#e11d48"
          />
        </Grid>
        <Grid item xs={12} sm={6} lg={3}>
          <DashboardCard
            title="Active Loans"
            value={data.active_loans}
            icon={<RequestQuoteIcon />}
            caption={`${formatCurrency(data.monthly_emi_total)} monthly EMI`}
            color="#f59e0b"
          />
        </Grid>
      </Grid>

      {/* ----------------------------------------------------- quick actions */}
      <SectionCard
        title="Quick actions"
        subtitle="Jump straight into the most used demo features"
        sx={{ mt: 2.5 }}
      >
        <Grid container spacing={2}>
          {QUICK_ACTIONS.map((action) => (
            <Grid item xs={12} sm={6} md={3} key={action.label}>
              <Button
                fullWidth
                variant="outlined"
                startIcon={action.icon}
                onClick={() => navigate(action.to)}
                sx={{ justifyContent: "flex-start", py: 1.4 }}
              >
                {action.label}
              </Button>
            </Grid>
          ))}
        </Grid>
      </SectionCard>

      {/* ------------------------------------------------------------ charts */}
      <Grid container spacing={2.5} sx={{ mt: 0.5 }}>
        <Grid item xs={12} lg={8}>
          <SectionCard
            title="Income vs Expenses"
            subtitle="Last 6 months (demo data)"
            action={
              <Tabs
                value={trendTab}
                onChange={(_, value) => setTrendTab(value)}
                sx={{ minHeight: 34 }}
              >
                <Tab value="both" label="Both" sx={{ minHeight: 34, fontSize: 12 }} />
                <Tab value="income" label="Income" sx={{ minHeight: 34, fontSize: 12 }} />
                <Tab value="expense" label="Expense" sx={{ minHeight: 34, fontSize: 12 }} />
              </Tabs>
            }
          >
            <Box sx={{ height: 300 }}>
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={trend}>
                  <defs>
                    <linearGradient id="incomeFill" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#16a34a" stopOpacity={0.35} />
                      <stop offset="95%" stopColor="#16a34a" stopOpacity={0} />
                    </linearGradient>
                    <linearGradient id="expenseFill" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#e11d48" stopOpacity={0.35} />
                      <stop offset="95%" stopColor="#e11d48" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#eef1f8" />
                  <XAxis dataKey="short_month" tick={{ fontSize: 12 }} />
                  <YAxis tick={{ fontSize: 12 }} tickFormatter={(value) => `${value / 1000}k`} />
                  <ChartTooltip formatter={(value) => formatCurrency(value)} />
                  <Legend />
                  {trendTab !== "expense" && (
                    <Area
                      type="monotone"
                      dataKey="income"
                      name="Income"
                      stroke="#16a34a"
                      fill="url(#incomeFill)"
                      strokeWidth={2}
                    />
                  )}
                  {trendTab !== "income" && (
                    <Area
                      type="monotone"
                      dataKey="expense"
                      name="Expense"
                      stroke="#e11d48"
                      fill="url(#expenseFill)"
                      strokeWidth={2}
                    />
                  )}
                </AreaChart>
              </ResponsiveContainer>
            </Box>
          </SectionCard>
        </Grid>

        <Grid item xs={12} lg={4}>
          <SectionCard title="Spending by category" subtitle="This month">
            {categories.length === 0 ? (
              <EmptyState title="No spending yet" description="Debit transactions will appear here." />
            ) : (
              <>
                <Box sx={{ height: 210 }}>
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={categories}
                        dataKey="amount"
                        nameKey="category"
                        innerRadius={52}
                        outerRadius={82}
                        paddingAngle={3}
                      >
                        {categories.map((entry) => (
                          <Cell
                            key={entry.category}
                            fill={entry.color || CATEGORY_COLORS[entry.category] || "#94a3b8"}
                          />
                        ))}
                      </Pie>
                      <ChartTooltip formatter={(value) => formatCurrency(value)} />
                    </PieChart>
                  </ResponsiveContainer>
                </Box>
                <Stack spacing={1} sx={{ mt: 1 }}>
                  {categories.slice(0, 5).map((item) => (
                    <Stack key={item.category} direction="row" justifyContent="space-between">
                      <Stack direction="row" spacing={1} alignItems="center">
                        <Box
                          sx={{
                            width: 10,
                            height: 10,
                            borderRadius: "50%",
                            backgroundColor: item.color || CATEGORY_COLORS[item.category],
                          }}
                        />
                        <Typography variant="body2">{item.category}</Typography>
                      </Stack>
                      <Typography variant="body2" fontWeight={700}>
                        {formatCurrency(item.amount)}
                      </Typography>
                    </Stack>
                  ))}
                </Stack>
              </>
            )}
          </SectionCard>
        </Grid>

        <Grid item xs={12} md={7}>
          <SectionCard title="Monthly spending trend" subtitle="Number of transactions per month">
            <Box sx={{ height: 260 }}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={trend}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#eef1f8" />
                  <XAxis dataKey="short_month" tick={{ fontSize: 12 }} />
                  <YAxis tick={{ fontSize: 12 }} allowDecimals={false} />
                  <ChartTooltip />
                  <Legend />
                  <Bar
                    dataKey="transactions"
                    name="Transactions"
                    fill="#4361ee"
                    radius={[6, 6, 0, 0]}
                    maxBarSize={44}
                  />
                </BarChart>
              </ResponsiveContainer>
            </Box>
          </SectionCard>
        </Grid>

        <Grid item xs={12} md={5}>
          <SectionCard title="Loan status" subtitle="Demo loan applications">
            <Stack spacing={1.5}>
              {(data.loan_status_breakdown || []).map((item) => (
                <Stack key={item.status} direction="row" justifyContent="space-between" alignItems="center">
                  <Stack direction="row" spacing={1.25} alignItems="center">
                    <StatusChip status={item.status} />
                    <Typography variant="body2" color="text.secondary">
                      {item.label}
                    </Typography>
                  </Stack>
                  <Typography variant="h6">{item.count}</Typography>
                </Stack>
              ))}
              <Divider sx={{ my: 0.5 }} />
              <Stack direction="row" justifyContent="space-between">
                <Typography variant="body2" color="text.secondary">
                  Total outstanding
                </Typography>
                <Typography variant="body2" fontWeight={700}>
                  {formatCurrency(data.total_outstanding)}
                </Typography>
              </Stack>
              <Stack direction="row" justifyContent="space-between">
                <Typography variant="body2" color="text.secondary">
                  Monthly EMI total
                </Typography>
                <Typography variant="body2" fontWeight={700}>
                  {formatCurrency(data.monthly_emi_total)}
                </Typography>
              </Stack>
              <Button endIcon={<ArrowForwardIcon />} onClick={() => navigate("/loans")}>
                Manage loans
              </Button>
            </Stack>
          </SectionCard>
        </Grid>
      </Grid>

      {/* --------------------------------------------- transactions + alerts */}
      <Grid container spacing={2.5} sx={{ mt: 0.5 }}>
        <Grid item xs={12} md={8}>
          <SectionCard
            title="Recent transactions"
            subtitle="Latest 5 movements in your demo account"
            action={
              <Button size="small" endIcon={<ArrowForwardIcon />} onClick={() => navigate("/transactions")}>
                View all
              </Button>
            }
          >
            <List disablePadding>
              {(data.recent_transactions || []).map((txn, index) => (
                <Box key={txn.id}>
                  <ListItem
                    disableGutters
                    sx={{ cursor: "pointer" }}
                    onClick={() => navigate(`/transactions/${txn.id}`)}
                    secondaryAction={
                      <Typography
                        fontWeight={700}
                        color={txn.transaction_type === "CREDIT" ? "success.main" : "text.primary"}
                      >
                        {txn.transaction_type === "CREDIT" ? "+" : "-"}
                        {formatCurrency(txn.amount)}
                      </Typography>
                    }
                  >
                    <ListItemAvatar>
                      <Box
                        sx={{
                          display: "grid",
                          placeItems: "center",
                          width: 40,
                          height: 40,
                          borderRadius: 2,
                          backgroundColor: "#f2f5fd",
                          color: "primary.main",
                        }}
                      >
                        {txn.transaction_type === "CREDIT" ? (
                          <TrendingUpIcon fontSize="small" />
                        ) : (
                          <TrendingDownIcon fontSize="small" />
                        )}
                      </Box>
                    </ListItemAvatar>
                    <ListItemText
                      primary={txn.description}
                      secondary={`${formatDate(txn.date)} • ${txn.category} • ${txn.transaction_id}`}
                      primaryTypographyProps={{ fontWeight: 600, fontSize: 14 }}
                    />
                  </ListItem>
                  {index < data.recent_transactions.length - 1 && <Divider component="li" />}
                </Box>
              ))}
            </List>
          </SectionCard>
        </Grid>

        <Grid item xs={12} md={4}>
          <SectionCard
            title="Notifications"
            subtitle={`${data.unread_notifications} unread`}
            action={
              <Button size="small" onClick={() => navigate("/notifications")}>
                See all
              </Button>
            }
          >
            {notifications.length === 0 ? (
              <EmptyState title="No notifications" description="Simulated alerts will appear here." />
            ) : (
              <Stack spacing={1.5}>
                {notifications.map((item) => (
                  <Stack
                    key={item.id}
                    direction="row"
                    spacing={1.5}
                    alignItems="flex-start"
                    sx={{ p: 1.25, borderRadius: 2, backgroundColor: item.is_read ? "#fbfcff" : "#eef2fd" }}
                  >
                    <NotificationsActiveIcon fontSize="small" color="primary" />
                    <Box>
                      <Typography variant="subtitle2" fontSize={13}>
                        {item.title}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        {item.message.length > 90 ? `${item.message.slice(0, 90)}...` : item.message}
                      </Typography>
                    </Box>
                  </Stack>
                ))}
              </Stack>
            )}
          </SectionCard>
        </Grid>
      </Grid>

      <Alert severity="info" sx={{ mt: 3, borderRadius: 3 }}>
        BankFlow is a demonstration application. Balances, transactions, loans and notifications are
        fictional and no real money movement takes place.
      </Alert>
    </Box>
  );
}
```

### frontend/src/pages/Account.jsx

```jsx
import { useCallback, useEffect, useState } from "react";
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Divider,
  Grid,
  Stack,
  Typography,
} from "@mui/material";
import ContentCopyIcon from "@mui/icons-material/ContentCopy";
import AccountBalanceIcon from "@mui/icons-material/AccountBalance";
import ReceiptLongIcon from "@mui/icons-material/ReceiptLong";
import CalculateIcon from "@mui/icons-material/Calculate";
import { useNavigate } from "react-router-dom";

import { ErrorAlert, Loader, PageHeader, SectionCard, StatusChip } from "../components/Common.jsx";
import bankingService from "../services/bankingService";
import { getErrorMessage } from "../services/api";
import { formatCurrency, formatDate } from "../utils/formatCurrency.js";

function DetailRow({ label, value, copyable }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(String(value));
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch {
      setCopied(false);
    }
  };

  return (
    <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ py: 1.25 }}>
      <Typography variant="body2" color="text.secondary">
        {label}
      </Typography>
      <Stack direction="row" spacing={1} alignItems="center">
        <Typography variant="body2" fontWeight={700}>
          {value}
        </Typography>
        {copyable && (
          <Button size="small" onClick={handleCopy} startIcon={<ContentCopyIcon fontSize="small" />}>
            {copied ? "Copied" : "Copy"}
          </Button>
        )}
      </Stack>
    </Stack>
  );
}

export default function Account() {
  const navigate = useNavigate();
  const [account, setAccount] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      setAccount(await bankingService.getAccount());
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  if (loading) return <Loader label="Loading account details..." />;

  return (
    <Box>
      <PageHeader
        title="My Account"
        subtitle="A simulated savings account with masked identifiers for the demo."
      />
      <ErrorAlert message={error} onRetry={load} />

      {account && (
        <Grid container spacing={2.5}>
          <Grid item xs={12} md={5}>
            <Card
              sx={{
                color: "#fff",
                background: "linear-gradient(135deg, #12295e 0%, #1b3a8f 55%, #4361ee 100%)",
                borderRadius: 4,
              }}
            >
              <CardContent sx={{ p: 3 }}>
                <Stack direction="row" justifyContent="space-between" alignItems="flex-start">
                  <Box>
                    <Typography variant="caption" sx={{ color: "rgba(255,255,255,.75)" }}>
                      Available balance
                    </Typography>
                    <Typography variant="h4" sx={{ fontWeight: 800, mt: 0.5 }}>
                      {formatCurrency(account.balance)}
                    </Typography>
                  </Box>
                  <AccountBalanceIcon sx={{ fontSize: 34, opacity: 0.9 }} />
                </Stack>

                <Typography variant="body1" sx={{ letterSpacing: 3, mt: 4, fontSize: 18 }}>
                  {account.masked_account_number}
                </Typography>
                <Stack direction="row" justifyContent="space-between" sx={{ mt: 3 }}>
                  <Box>
                    <Typography variant="caption" sx={{ color: "rgba(255,255,255,.7)" }}>
                      Account holder
                    </Typography>
                    <Typography variant="body2" fontWeight={700}>
                      {account.customer_name}
                    </Typography>
                  </Box>
                  <Box>
                    <Typography variant="caption" sx={{ color: "rgba(255,255,255,.7)" }}>
                      IFSC (demo)
                    </Typography>
                    <Typography variant="body2" fontWeight={700}>
                      {account.ifsc_code}
                    </Typography>
                  </Box>
                </Stack>
              </CardContent>
            </Card>

            <Stack direction="row" spacing={1.5} sx={{ mt: 2 }}>
              <Button
                fullWidth
                variant="contained"
                startIcon={<ReceiptLongIcon />}
                onClick={() => navigate("/transactions")}
              >
                Transactions
              </Button>
              <Button
                fullWidth
                variant="outlined"
                startIcon={<CalculateIcon />}
                onClick={() => navigate("/emi-calculator")}
              >
                EMI calculator
              </Button>
            </Stack>
          </Grid>

          <Grid item xs={12} md={7}>
            <SectionCard title="Account information" subtitle="Simulated details - safe to share">
              <DetailRow label="Customer name" value={account.customer_name} />
              <Divider />
              <DetailRow label="Email" value={account.customer_email} />
              <Divider />
              <DetailRow label="Account number (masked)" value={account.masked_account_number} />
              <Divider />
              <DetailRow label="Account type" value={account.account_type_display} />
              <Divider />
              <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ py: 1.25 }}>
                <Typography variant="body2" color="text.secondary">
                  Account status
                </Typography>
                <StatusChip status={account.status} />
              </Stack>
              <Divider />
              <DetailRow label="Available balance" value={formatCurrency(account.balance)} />
              <Divider />
              <DetailRow label="IFSC-like demo identifier" value={account.ifsc_code} copyable />
              <Divider />
              <DetailRow label="Branch" value={account.branch} />
              <Divider />
              <DetailRow label="Date created" value={formatDate(account.created_at)} />
            </SectionCard>

            <Alert severity="info" sx={{ mt: 2.5, borderRadius: 3 }}>
              For privacy, the full account number is never displayed or exposed by the API. All
              identifiers and balances in BankFlow are fictional demo values.
            </Alert>
          </Grid>
        </Grid>
      )}
    </Box>
  );
}
```

### frontend/src/pages/Transactions.jsx

```jsx
import { useCallback, useEffect, useMemo, useState } from "react";
import {
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Grid,
  InputAdornment,
  MenuItem,
  Paper,
  Stack,
  TablePagination,
  TextField,
  Typography,
} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import FilterAltOffIcon from "@mui/icons-material/FilterAltOff";

import TransactionTable from "../components/TransactionTable.jsx";
import { ErrorAlert, PageHeader } from "../components/Common.jsx";
import bankingService from "../services/bankingService";
import { getErrorMessage } from "../services/api";
import { TRANSACTION_CATEGORIES, formatCurrency } from "../utils/formatCurrency.js";

const EMPTY_FILTERS = {
  search: "",
  category: "ALL",
  type: "ALL",
  status: "ALL",
  start_date: "",
  end_date: "",
  ordering: "-date",
};

export default function Transactions() {
  const [filters, setFilters] = useState(EMPTY_FILTERS);
  const [debouncedSearch, setDebouncedSearch] = useState("");
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [data, setData] = useState({ results: [], count: 0, summary: null });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Debounce the search box so we do not fire a request on every keystroke.
  useEffect(() => {
    const timer = setTimeout(() => setDebouncedSearch(filters.search), 400);
    return () => clearTimeout(timer);
  }, [filters.search]);

  const query = useMemo(
    () => ({
      page: page + 1,
      page_size: rowsPerPage,
      search: debouncedSearch || undefined,
      category: filters.category,
      type: filters.type,
      status: filters.status,
      start_date: filters.start_date || undefined,
      end_date: filters.end_date || undefined,
      ordering: filters.ordering,
    }),
    [page, rowsPerPage, debouncedSearch, filters.category, filters.type, filters.status,
     filters.start_date, filters.end_date, filters.ordering]
  );

  const load = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const response = await bankingService.getTransactions(query);
      setData({
        results: response.results,
        count: response.count,
        summary: response.summary,
      });
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, [query]);

  useEffect(() => {
    load();
  }, [load]);

  const updateFilter = (field) => (event) => {
    setPage(0);
    setFilters((prev) => ({ ...prev, [field]: event.target.value }));
  };

  const resetFilters = () => {
    setFilters(EMPTY_FILTERS);
    setPage(0);
  };

  const activeFilterCount = Object.entries(filters).filter(
    ([key, value]) => value && value !== "ALL" && key !== "ordering" && key !== "search"
  ).length;

  return (
    <Box>
      <PageHeader
        title="Transactions"
        subtitle="Search, filter and inspect every simulated movement in your demo account."
        action={
          <Button
            variant="outlined"
            startIcon={<FilterAltOffIcon />}
            onClick={resetFilters}
            disabled={activeFilterCount === 0 && !filters.search}
          >
            Reset filters{activeFilterCount ? ` (${activeFilterCount})` : ""}
          </Button>
        }
      />

      <ErrorAlert message={error} onRetry={load} />

      <Grid container spacing={2.5} sx={{ mb: 2.5 }}>
        <Grid item xs={12} sm={4}>
          <Card>
            <CardContent>
              <Typography variant="caption" color="text.secondary">
                Total credit (filtered)
              </Typography>
              <Typography variant="h6" color="success.main">
                {formatCurrency(data.summary?.total_credit || 0)}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={4}>
          <Card>
            <CardContent>
              <Typography variant="caption" color="text.secondary">
                Total debit (filtered)
              </Typography>
              <Typography variant="h6" color="error.main">
                {formatCurrency(data.summary?.total_debit || 0)}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={4}>
          <Card>
            <CardContent>
              <Typography variant="caption" color="text.secondary">
                Net movement
              </Typography>
              <Typography variant="h6">{formatCurrency(data.summary?.net || 0)}</Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Paper variant="outlined" sx={{ p: 2.5, borderRadius: 3 }}>
        <Grid container spacing={2} sx={{ mb: 2 }}>
          <Grid item xs={12} md={4}>
            <TextField
              fullWidth
              size="small"
              placeholder="Search description, ID or category"
              value={filters.search}
              onChange={updateFilter("search")}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <SearchIcon fontSize="small" />
                  </InputAdornment>
                ),
              }}
            />
          </Grid>
          <Grid item xs={6} md={2}>
            <TextField
              fullWidth
              select
              size="small"
              label="Category"
              value={filters.category}
              onChange={updateFilter("category")}
            >
              <MenuItem value="ALL">All categories</MenuItem>
              {TRANSACTION_CATEGORIES.map((category) => (
                <MenuItem key={category} value={category}>
                  {category}
                </MenuItem>
              ))}
            </TextField>
          </Grid>
          <Grid item xs={6} md={2}>
            <TextField
              fullWidth
              select
              size="small"
              label="Type"
              value={filters.type}
              onChange={updateFilter("type")}
            >
              <MenuItem value="ALL">All types</MenuItem>
              <MenuItem value="CREDIT">Credit</MenuItem>
              <MenuItem value="DEBIT">Debit</MenuItem>
            </TextField>
          </Grid>
          <Grid item xs={6} md={2}>
            <TextField
              fullWidth
              size="small"
              type="date"
              label="From"
              InputLabelProps={{ shrink: true }}
              value={filters.start_date}
              onChange={updateFilter("start_date")}
            />
          </Grid>
          <Grid item xs={6} md={2}>
            <TextField
              fullWidth
              size="small"
              type="date"
              label="To"
              InputLabelProps={{ shrink: true }}
              value={filters.end_date}
              onChange={updateFilter("end_date")}
            />
          </Grid>
        </Grid>

        <Stack direction="row" spacing={1} sx={{ mb: 1.5, flexWrap: "wrap", gap: 1 }}>
          <Typography variant="caption" color="text.secondary" sx={{ alignSelf: "center" }}>
            Sort by:
          </Typography>
          {[
            { value: "-date", label: "Newest" },
            { value: "date", label: "Oldest" },
            { value: "-amount", label: "Highest amount" },
            { value: "amount", label: "Lowest amount" },
          ].map((option) => (
            <Chip
              key={option.value}
              size="small"
              label={option.label}
              color={filters.ordering === option.value ? "primary" : "default"}
              variant={filters.ordering === option.value ? "filled" : "outlined"}
              onClick={() => {
                setPage(0);
                setFilters((prev) => ({ ...prev, ordering: option.value }));
              }}
            />
          ))}
        </Stack>

        <TransactionTable transactions={data.results} loading={loading} />

        {!loading && data.count > 0 && (
          <TablePagination
            component="div"
            count={data.count}
            page={page}
            onPageChange={(_, newPage) => setPage(newPage)}
            rowsPerPage={rowsPerPage}
            onRowsPerPageChange={(event) => {
              setRowsPerPage(parseInt(event.target.value, 10));
              setPage(0);
            }}
            rowsPerPageOptions={[5, 10, 25]}
          />
        )}
      </Paper>
    </Box>
  );
}
```

### frontend/src/pages/TransactionDetails.jsx

```jsx
import { useCallback, useEffect, useState } from "react";
import {
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Divider,
  Grid,
  Stack,
  Typography,
} from "@mui/material";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import { useNavigate, useParams } from "react-router-dom";

import { ErrorAlert, Loader, PageHeader, SectionCard, StatusChip } from "../components/Common.jsx";
import bankingService from "../services/bankingService";
import { getErrorMessage } from "../services/api";
import { formatCurrency, formatDate } from "../utils/formatCurrency.js";

export default function TransactionDetails() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [transaction, setTransaction] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      setTransaction(await bankingService.getTransaction(id));
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    load();
  }, [load]);

  if (loading) return <Loader label="Loading transaction..." />;

  if (error) {
    return (
      <>
        <PageHeader title="Transaction details" />
        <ErrorAlert message={error} onRetry={load} />
        <Button startIcon={<ArrowBackIcon />} onClick={() => navigate("/transactions")}>
          Back to transactions
        </Button>
      </>
    );
  }

  const isCredit = transaction.transaction_type === "CREDIT";

  return (
    <Box>
      <PageHeader
        title="Transaction details"
        subtitle={transaction.transaction_id}
        action={
          <Button startIcon={<ArrowBackIcon />} onClick={() => navigate("/transactions")}>
            Back
          </Button>
        }
      />

      <Grid container spacing={2.5}>
        <Grid item xs={12} md={5}>
          <Card
            sx={{
              borderRadius: 4,
              background: isCredit
                ? "linear-gradient(135deg, #0f5132 0%, #16a34a 100%)"
                : "linear-gradient(135deg, #12295e 0%, #1b3a8f 100%)",
              color: "#fff",
            }}
          >
            <CardContent sx={{ p: 3 }}>
              <Typography variant="caption" sx={{ color: "rgba(255,255,255,.8)" }}>
                {isCredit ? "Amount credited" : "Amount debited"}
              </Typography>
              <Typography variant="h3" sx={{ fontWeight: 800, mt: 1 }}>
                {isCredit ? "+" : "-"}
                {formatCurrency(transaction.amount)}
              </Typography>
              <Typography variant="body2" sx={{ mt: 1, color: "rgba(255,255,255,.85)" }}>
                {transaction.description}
              </Typography>
              <Stack direction="row" spacing={1} sx={{ mt: 3 }}>
                <Chip size="small" label={transaction.category} sx={{ bgcolor: "rgba(255,255,255,.22)", color: "#fff" }} />
                <Chip size="small" label={transaction.type_display} sx={{ bgcolor: "rgba(255,255,255,.22)", color: "#fff" }} />
              </Stack>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={7}>
          <SectionCard title="Transaction information">
            {[
              ["Transaction ID", transaction.transaction_id],
              ["Date & time", formatDate(transaction.date, { withTime: true })],
              ["Category", transaction.category_display || transaction.category],
              ["Type", transaction.type_display],
              ["Amount", formatCurrency(transaction.amount)],
              ["Balance after transaction", formatCurrency(transaction.balance_after)],
              ["Account number", transaction.account_number],
            ].map(([label, value]) => (
              <Box key={label}>
                <Stack direction="row" justifyContent="space-between" sx={{ py: 1.25 }}>
                  <Typography variant="body2" color="text.secondary">
                    {label}
                  </Typography>
                  <Typography variant="body2" fontWeight={700}>
                    {value}
                  </Typography>
                </Stack>
                <Divider />
              </Box>
            ))}
            <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ pt: 1.5 }}>
              <Typography variant="body2" color="text.secondary">
                Status
              </Typography>
              <StatusChip status={transaction.status} />
            </Stack>
          </SectionCard>
        </Grid>
      </Grid>
    </Box>
  );
}
```

### frontend/src/pages/Loans.jsx

```jsx
import { useCallback, useEffect, useMemo, useState } from "react";
import {
  Alert,
  Box,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Grid,
  MenuItem,
  Snackbar,
  Stack,
  Tab,
  Tabs,
  TextField,
  Typography,
} from "@mui/material";
import AddCircleOutlineIcon from "@mui/icons-material/AddCircleOutline";

import LoanCard from "../components/LoanCard.jsx";
import { EmptyState, ErrorAlert, Loader, PageHeader, SectionCard } from "../components/Common.jsx";
import bankingService from "../services/bankingService";
import { getErrorMessage } from "../services/api";
import { LOAN_TYPES, formatCurrency } from "../utils/formatCurrency.js";
import { calculateEmi, tenureLabel } from "../utils/calculations.js";

const STATUS_TABS = ["ALL", "PENDING", "APPROVED", "ACTIVE", "REJECTED", "COMPLETED"];

const EMPTY_APPLICATION = {
  loan_type: "PERSONAL",
  amount: 200000,
  interest_rate: 12.5,
  tenure_months: 24,
  monthly_income: 60000,
  employment_type: "SALARIED",
  purpose: "",
};

export default function Loans() {
  const [loans, setLoans] = useState([]);
  const [status, setStatus] = useState("ALL");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [dialogOpen, setDialogOpen] = useState(false);
  const [application, setApplication] = useState(EMPTY_APPLICATION);
  const [formError, setFormError] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [snack, setSnack] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      setLoans(await bankingService.getLoans());
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  const filtered = useMemo(
    () => (status === "ALL" ? loans : loans.filter((loan) => loan.status === status)),
    [loans, status]
  );

  const totals = useMemo(() => {
    const active = loans.filter((loan) => ["ACTIVE", "APPROVED"].includes(loan.status));
    return {
      outstanding: active.reduce((sum, loan) => sum + Number(loan.remaining_amount || 0), 0),
      emi: active.reduce((sum, loan) => sum + Number(loan.emi || 0), 0),
      count: active.length,
    };
  }, [loans]);

  const preview = calculateEmi(
    application.amount,
    application.interest_rate,
    application.tenure_months
  );

  const openDialog = () => {
    setApplication(EMPTY_APPLICATION);
    setFormError("");
    setDialogOpen(true);
  };

  const handleTypeChange = (event) => {
    const selected = LOAN_TYPES.find((type) => type.value === event.target.value);
    setApplication((prev) => ({
      ...prev,
      loan_type: event.target.value,
      interest_rate: selected?.defaultRate ?? prev.interest_rate,
    }));
  };

  const submitApplication = async () => {
    setFormError("");
    if (!application.purpose.trim()) {
      setFormError("Please add a short purpose for the demo loan.");
      return;
    }
    if (application.amount < 10000) {
      setFormError("The minimum demo loan amount is Rs 10,000.");
      return;
    }

    setSubmitting(true);
    try {
      await bankingService.applyLoan(application);
      setDialogOpen(false);
      setSnack("Demo loan application submitted and marked as pending review.");
      await load();
    } catch (err) {
      setFormError(getErrorMessage(err));
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <Loader label="Loading your demo loans..." />;

  return (
    <Box>
      <PageHeader
        title="Loans"
        subtitle="Apply for a simulated loan and monitor EMI, tenure and outstanding amount."
        action={
          <Button variant="contained" startIcon={<AddCircleOutlineIcon />} onClick={openDialog}>
            Apply for a demo loan
          </Button>
        }
      />

      <ErrorAlert message={error} onRetry={load} />

      <Grid container spacing={2.5} sx={{ mb: 2.5 }}>
        <Grid item xs={12} sm={4}>
          <SectionCard title="Active loans">
            <Typography variant="h4">{totals.count}</Typography>
            <Typography variant="caption" color="text.secondary">
              Approved or running demo loans
            </Typography>
          </SectionCard>
        </Grid>
        <Grid item xs={12} sm={4}>
          <SectionCard title="Monthly EMI total">
            <Typography variant="h4">{formatCurrency(totals.emi)}</Typography>
            <Typography variant="caption" color="text.secondary">
              Sum of every active EMI
            </Typography>
          </SectionCard>
        </Grid>
        <Grid item xs={12} sm={4}>
          <SectionCard title="Outstanding amount">
            <Typography variant="h4">{formatCurrency(totals.outstanding)}</Typography>
            <Typography variant="caption" color="text.secondary">
              Remaining demo balance to repay
            </Typography>
          </SectionCard>
        </Grid>
      </Grid>

      <Tabs
        value={status}
        onChange={(_, value) => setStatus(value)}
        variant="scrollable"
        scrollButtons="auto"
        sx={{ mb: 2, borderBottom: "1px solid #e6e9f2" }}
      >
        {STATUS_TABS.map((tab) => (
          <Tab key={tab} value={tab} label={tab === "ALL" ? "All loans" : tab.toLowerCase()} />
        ))}
      </Tabs>

      {filtered.length === 0 ? (
        <EmptyState
          title="No loans in this view"
          description="Submit a demo loan application to see it appear here with a pending status."
          action={
            <Button variant="contained" onClick={openDialog}>
              Apply for a demo loan
            </Button>
          }
        />
      ) : (
        <Grid container spacing={2.5}>
          {filtered.map((loan) => (
            <Grid item xs={12} md={6} xl={4} key={loan.id}>
              <LoanCard loan={loan} />
            </Grid>
          ))}
        </Grid>
      )}

      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Apply for a demo loan</DialogTitle>
        <DialogContent dividers>
          {formError && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {formError}
            </Alert>
          )}
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                select
                label="Loan type"
                value={application.loan_type}
                onChange={handleTypeChange}
              >
                {LOAN_TYPES.map((type) => (
                  <MenuItem key={type.value} value={type.value}>
                    {type.label} ({type.defaultRate}%)
                  </MenuItem>
                ))}
              </TextField>
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                type="number"
                label="Loan amount"
                value={application.amount}
                onChange={(event) =>
                  setApplication({ ...application, amount: Number(event.target.value) })
                }
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                type="number"
                label="Interest rate (% p.a.)"
                value={application.interest_rate}
                onChange={(event) =>
                  setApplication({ ...application, interest_rate: Number(event.target.value) })
                }
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                type="number"
                label="Tenure (months)"
                value={application.tenure_months}
                onChange={(event) =>
                  setApplication({ ...application, tenure_months: Number(event.target.value) })
                }
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                type="number"
                label="Monthly income"
                value={application.monthly_income}
                onChange={(event) =>
                  setApplication({ ...application, monthly_income: Number(event.target.value) })
                }
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                select
                label="Employment type"
                value={application.employment_type}
                onChange={(event) =>
                  setApplication({ ...application, employment_type: event.target.value })
                }
              >
                {[
                  ["SALARIED", "Salaried"],
                  ["SELF_EMPLOYED", "Self Employed"],
                  ["STUDENT", "Student"],
                  ["RETIRED", "Retired"],
                  ["OTHER", "Other"],
                ].map(([value, label]) => (
                  <MenuItem key={value} value={value}>
                    {label}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Purpose"
                placeholder="e.g. Home renovation"
                value={application.purpose}
                onChange={(event) =>
                  setApplication({ ...application, purpose: event.target.value })
                }
              />
            </Grid>
          </Grid>

          <Box sx={{ mt: 3, p: 2, borderRadius: 3, backgroundColor: "#f8f9fd" }}>
            <Typography variant="subtitle2" sx={{ mb: 1 }}>
              Estimated EMI (live preview)
            </Typography>
            <Stack direction="row" spacing={3} sx={{ flexWrap: "wrap", gap: 1 }}>
              <Box>
                <Typography variant="caption" color="text.secondary">
                  Monthly EMI
                </Typography>
                <Typography variant="h6">{formatCurrency(preview.monthly_emi)}</Typography>
              </Box>
              <Box>
                <Typography variant="caption" color="text.secondary">
                  Total interest
                </Typography>
                <Typography variant="h6">{formatCurrency(preview.total_interest)}</Typography>
              </Box>
              <Box>
                <Typography variant="caption" color="text.secondary">
                  Total repayment
                </Typography>
                <Typography variant="h6">{formatCurrency(preview.total_payment)}</Typography>
              </Box>
              <Box>
                <Typography variant="caption" color="text.secondary">
                  Tenure
                </Typography>
                <Typography variant="h6">{tenureLabel(application.tenure_months)}</Typography>
              </Box>
            </Stack>
          </Box>
        </DialogContent>
        <DialogActions sx={{ p: 2 }}>
          <Button onClick={() => setDialogOpen(false)}>Cancel</Button>
          <Button variant="contained" onClick={submitApplication} disabled={submitting}>
            {submitting ? "Submitting..." : "Submit application"}
          </Button>
        </DialogActions>
      </Dialog>

      <Snackbar
        open={Boolean(snack)}
        autoHideDuration={4000}
        onClose={() => setSnack("")}
        message={snack}
      />
    </Box>
  );
}
```

### frontend/src/pages/LoanDetails.jsx

```jsx
import { useCallback, useEffect, useState } from "react";
import {
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Divider,
  Grid,
  LinearProgress,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import { useNavigate, useParams } from "react-router-dom";

import { ErrorAlert, Loader, PageHeader, SectionCard, StatusChip } from "../components/Common.jsx";
import bankingService from "../services/bankingService";
import { getErrorMessage } from "../services/api";
import { formatCurrency, formatDate } from "../utils/formatCurrency.js";
import { amortisationSchedule, tenureLabel } from "../utils/calculations.js";

export default function LoanDetails() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [loan, setLoan] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      setLoan(await bankingService.getLoan(id));
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    load();
  }, [load]);

  if (loading) return <Loader label="Loading loan details..." />;

  if (error) {
    return (
      <>
        <PageHeader title="Loan details" />
        <ErrorAlert message={error} onRetry={load} />
        <Button startIcon={<ArrowBackIcon />} onClick={() => navigate("/loans")}>
          Back to loans
        </Button>
      </>
    );
  }

  const schedule = amortisationSchedule(loan.amount, loan.interest_rate, loan.tenure_months, 12);

  return (
    <Box>
      <PageHeader
        title={loan.loan_type_display}
        subtitle={`Loan ID ${loan.loan_id} - applied ${formatDate(loan.applied_at)}`}
        action={
          <Button startIcon={<ArrowBackIcon />} onClick={() => navigate("/loans")}>
            Back to loans
          </Button>
        }
      />

      <Grid container spacing={2.5}>
        <Grid item xs={12} md={4}>
          <Card
            sx={{
              color: "#fff",
              background: "linear-gradient(135deg, #12295e 0%, #1b3a8f 60%, #4361ee 100%)",
              borderRadius: 4,
            }}
          >
            <CardContent sx={{ p: 3 }}>
              <Stack direction="row" justifyContent="space-between" alignItems="center">
                <Typography variant="caption" sx={{ color: "rgba(255,255,255,.8)" }}>
                  Outstanding amount
                </Typography>
                <Chip
                  size="small"
                  label={loan.status_display}
                  sx={{ bgcolor: "rgba(255,255,255,.2)", color: "#fff" }}
                />
              </Stack>
              <Typography variant="h4" sx={{ fontWeight: 800, mt: 1 }}>
                {formatCurrency(loan.remaining_amount)}
              </Typography>
              <Typography variant="body2" sx={{ mt: 1, color: "rgba(255,255,255,.85)" }}>
                of {formatCurrency(loan.amount)} sanctioned
              </Typography>

              <Box sx={{ mt: 3 }}>
                <Stack direction="row" justifyContent="space-between">
                  <Typography variant="caption" sx={{ color: "rgba(255,255,255,.8)" }}>
                    Repaid {formatCurrency(loan.paid_amount)}
                  </Typography>
                  <Typography variant="caption" fontWeight={700}>
                    {loan.progress_percent}%
                  </Typography>
                </Stack>
                <LinearProgress
                  variant="determinate"
                  value={Math.min(loan.progress_percent, 100)}
                  sx={{
                    mt: 0.75,
                    height: 8,
                    borderRadius: 4,
                    backgroundColor: "rgba(255,255,255,.25)",
                    "& .MuiLinearProgress-bar": { backgroundColor: "#4fc3f7" },
                  }}
                />
              </Box>

              <Stack direction="row" spacing={3} sx={{ mt: 3, flexWrap: "wrap", gap: 1 }}>
                <Box>
                  <Typography variant="caption" sx={{ color: "rgba(255,255,255,.7)" }}>
                    Monthly EMI
                  </Typography>
                  <Typography variant="h6">{formatCurrency(loan.emi)}</Typography>
                </Box>
                <Box>
                  <Typography variant="caption" sx={{ color: "rgba(255,255,255,.7)" }}>
                    Interest
                  </Typography>
                  <Typography variant="h6">{loan.interest_rate}%</Typography>
                </Box>
                <Box>
                  <Typography variant="caption" sx={{ color: "rgba(255,255,255,.7)" }}>
                    Tenure
                  </Typography>
                  <Typography variant="h6">{tenureLabel(loan.tenure_months)}</Typography>
                </Box>
              </Stack>
            </CardContent>
          </Card>

          <SectionCard title="Application summary" sx={{ mt: 2.5 }}>
            {[
              ["Loan ID", loan.loan_id],
              ["Loan type", loan.loan_type_display],
              ["Purpose", loan.purpose || "-"],
              ["Monthly income", formatCurrency(loan.monthly_income)],
              ["Employment", loan.employment_type_display],
              ["Applied on", formatDate(loan.applied_at)],
            ].map(([label, value]) => (
              <Box key={label}>
                <Stack direction="row" justifyContent="space-between" sx={{ py: 1.1 }}>
                  <Typography variant="body2" color="text.secondary">
                    {label}
                  </Typography>
                  <Typography variant="body2" fontWeight={700} textAlign="right">
                    {value}
                  </Typography>
                </Stack>
                <Divider />
              </Box>
            ))}
            <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ pt: 1.5 }}>
              <Typography variant="body2" color="text.secondary">
                Status
              </Typography>
              <StatusChip status={loan.status} />
            </Stack>
          </SectionCard>
        </Grid>

        <Grid item xs={12} md={8}>
          <SectionCard
            title="Repayment schedule (first 12 instalments)"
            subtitle="Calculated on a reducing balance basis for this demo loan"
          >
            <TableContainer>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>Month</TableCell>
                    <TableCell align="right">EMI</TableCell>
                    <TableCell align="right">Principal</TableCell>
                    <TableCell align="right">Interest</TableCell>
                    <TableCell align="right">Balance</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {schedule.map((row) => (
                    <TableRow key={row.month} hover>
                      <TableCell>{row.month}</TableCell>
                      <TableCell align="right">{formatCurrency(row.emi)}</TableCell>
                      <TableCell align="right">{formatCurrency(row.principal)}</TableCell>
                      <TableCell align="right">{formatCurrency(row.interest)}</TableCell>
                      <TableCell align="right">{formatCurrency(row.balance)}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </SectionCard>
        </Grid>
      </Grid>
    </Box>
  );
}
```

### frontend/src/pages/EMICalculator.jsx

```jsx
import { useEffect, useMemo, useState } from "react";
import {
  Alert,
  Box,
  Card,
  CardContent,
  Divider,
  Grid,
  MenuItem,
  Slider,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from "@mui/material";
import CalculateIcon from "@mui/icons-material/Calculate";
import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip as ChartTooltip } from "recharts";

import { PageHeader, SectionCard } from "../components/Common.jsx";
import bankingService from "../services/bankingService";
import { LOAN_TYPES, formatCurrency } from "../utils/formatCurrency.js";
import { amortisationSchedule, calculateEmi, tenureLabel } from "../utils/calculations.js";

export default function EMICalculator() {
  const [loanAmount, setLoanAmount] = useState(500000);
  const [interestRate, setInterestRate] = useState(9.5);
  const [tenureMonths, setTenureMonths] = useState(60);
  const [loanType, setLoanType] = useState("PERSONAL");
  const [serverResult, setServerResult] = useState(null);
  const [serverError, setServerError] = useState("");

  const result = useMemo(
    () => calculateEmi(loanAmount, interestRate, tenureMonths),
    [loanAmount, interestRate, tenureMonths]
  );

  const schedule = useMemo(
    () => amortisationSchedule(loanAmount, interestRate, tenureMonths, 12),
    [loanAmount, interestRate, tenureMonths]
  );

  const donutData = [
    { name: "Principal", value: result.principal, color: "#1b3a8f" },
    { name: "Total interest", value: result.total_interest, color: "#0ea5e9" },
  ];

  // Confirm the client side maths with the Django endpoint (also demonstrates the API).
  useEffect(() => {
    let cancelled = false;
    const timer = setTimeout(async () => {
      try {
        const data = await bankingService.calculateEmi({
          loan_amount: loanAmount,
          interest_rate: interestRate,
          tenure_months: tenureMonths,
        });
        if (!cancelled) {
          setServerResult(data);
          setServerError("");
        }
      } catch {
        if (!cancelled) {
          setServerResult(null);
          setServerError("Server verification unavailable - showing locally calculated values.");
        }
      }
    }, 450);
    return () => {
      cancelled = true;
      clearTimeout(timer);
    };
  }, [loanAmount, interestRate, tenureMonths]);

  const applyLoanType = (event) => {
    const selected = LOAN_TYPES.find((type) => type.value === event.target.value);
    setLoanType(event.target.value);
    if (selected) setInterestRate(selected.defaultRate);
  };

  return (
    <Box>
      <PageHeader
        title="EMI Calculator"
        subtitle="Adjust the amount, rate and tenure to see the EMI update instantly."
      />

      <Grid container spacing={2.5}>
        <Grid item xs={12} md={7}>
          <SectionCard title="Loan inputs" subtitle="Values are not saved - this is a calculator">
            <Grid container spacing={3}>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  select
                  label="Loan type preset"
                  value={loanType}
                  onChange={applyLoanType}
                >
                  {LOAN_TYPES.map((type) => (
                    <MenuItem key={type.value} value={type.value}>
                      {type.label} - {type.defaultRate}%
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  type="number"
                  label="Loan amount"
                  value={loanAmount}
                  onChange={(event) =>
                    setLoanAmount(Math.max(Number(event.target.value) || 0, 1000))
                  }
                />
              </Grid>

              <Grid item xs={12}>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Loan amount: <strong>{formatCurrency(loanAmount)}</strong>
                </Typography>
                <Slider
                  value={loanAmount}
                  min={50000}
                  max={10000000}
                  step={25000}
                  onChange={(_, value) => setLoanAmount(value)}
                  valueLabelDisplay="auto"
                  valueLabelFormat={(value) => formatCurrency(value, { compact: true })}
                />
              </Grid>

              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  type="number"
                  label="Interest rate (% p.a.)"
                  value={interestRate}
                  onChange={(event) => setInterestRate(Number(event.target.value) || 0)}
                />
                <Slider
                  value={interestRate}
                  min={4}
                  max={20}
                  step={0.25}
                  onChange={(_, value) => setInterestRate(value)}
                  valueLabelDisplay="auto"
                  valueLabelFormat={(value) => `${value}%`}
                  sx={{ mt: 1 }}
                />
              </Grid>

              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  type="number"
                  label="Tenure (months)"
                  value={tenureMonths}
                  onChange={(event) =>
                    setTenureMonths(Math.min(Math.max(Number(event.target.value) || 1, 1), 360))
                  }
                  helperText={tenureLabel(tenureMonths)}
                />
                <Slider
                  value={tenureMonths}
                  min={6}
                  max={360}
                  step={6}
                  onChange={(_, value) => setTenureMonths(value)}
                  valueLabelDisplay="auto"
                  sx={{ mt: 1 }}
                />
              </Grid>
            </Grid>

            {serverError && (
              <Alert severity="warning" sx={{ mt: 2 }}>
                {serverError}
              </Alert>
            )}
            {serverResult && (
              <Alert severity="success" sx={{ mt: 2 }}>
                Verified by the Django API: {formatCurrency(serverResult.monthly_emi)} monthly EMI,
                total repayment {formatCurrency(serverResult.total_payment)}.
              </Alert>
            )}
          </SectionCard>

          <SectionCard
            title="Amortisation preview"
            subtitle="How the first 12 instalments split between principal and interest"
            sx={{ mt: 2.5 }}
          >
            <TableContainer>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>Month</TableCell>
                    <TableCell align="right">EMI</TableCell>
                    <TableCell align="right">Principal</TableCell>
                    <TableCell align="right">Interest</TableCell>
                    <TableCell align="right">Balance</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {schedule.map((row) => (
                    <TableRow key={row.month} hover>
                      <TableCell>{row.month}</TableCell>
                      <TableCell align="right">{formatCurrency(row.emi)}</TableCell>
                      <TableCell align="right">{formatCurrency(row.principal)}</TableCell>
                      <TableCell align="right">{formatCurrency(row.interest)}</TableCell>
                      <TableCell align="right">{formatCurrency(row.balance)}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </SectionCard>
        </Grid>

        <Grid item xs={12} md={5}>
          <Card
            sx={{
              borderRadius: 4,
              background: "linear-gradient(135deg, #1b3a8f 0%, #4361ee 100%)",
              color: "#fff",
            }}
          >
            <CardContent sx={{ p: 3 }}>
              <Stack direction="row" spacing={1.5} alignItems="center">
                <CalculateIcon />
                <Typography variant="subtitle1">Your monthly EMI</Typography>
              </Stack>
              <Typography variant="h3" sx={{ fontWeight: 800, mt: 2 }}>
                {formatCurrency(result.monthly_emi)}
              </Typography>
              <Typography variant="body2" sx={{ color: "rgba(255,255,255,.85)", mt: 0.5 }}>
                {formatCurrency(loanAmount)} at {interestRate}% for {tenureLabel(tenureMonths)}
              </Typography>

              <Divider sx={{ my: 3, borderColor: "rgba(255,255,255,.2)" }} />

              <Stack spacing={1.5}>
                <Stack direction="row" justifyContent="space-between">
                  <Typography variant="body2" sx={{ color: "rgba(255,255,255,.85)" }}>
                    Principal amount
                  </Typography>
                  <Typography variant="body2" fontWeight={700}>
                    {formatCurrency(result.principal)}
                  </Typography>
                </Stack>
                <Stack direction="row" justifyContent="space-between">
                  <Typography variant="body2" sx={{ color: "rgba(255,255,255,.85)" }}>
                    Total interest
                  </Typography>
                  <Typography variant="body2" fontWeight={700}>
                    {formatCurrency(result.total_interest)}
                  </Typography>
                </Stack>
                <Stack direction="row" justifyContent="space-between">
                  <Typography variant="body2" sx={{ color: "rgba(255,255,255,.85)" }}>
                    Total repayment
                  </Typography>
                  <Typography variant="body2" fontWeight={700}>
                    {formatCurrency(result.total_payment)}
                  </Typography>
                </Stack>
              </Stack>
            </CardContent>
          </Card>

          <SectionCard title="Principal vs interest" sx={{ mt: 2.5 }}>
            <Box sx={{ height: 240 }}>
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={donutData}
                    dataKey="value"
                    nameKey="name"
                    innerRadius={58}
                    outerRadius={90}
                    paddingAngle={3}
                  >
                    {donutData.map((entry) => (
                      <Cell key={entry.name} fill={entry.color} />
                    ))}
                  </Pie>
                  <ChartTooltip formatter={(value) => formatCurrency(value)} />
                </PieChart>
              </ResponsiveContainer>
            </Box>
            <Stack spacing={1} sx={{ mt: 1 }}>
              {donutData.map((item) => (
                <Stack key={item.name} direction="row" justifyContent="space-between">
                  <Stack direction="row" spacing={1} alignItems="center">
                    <Box
                      sx={{
                        width: 10,
                        height: 10,
                        borderRadius: "50%",
                        backgroundColor: item.color,
                      }}
                    />
                    <Typography variant="body2">{item.name}</Typography>
                  </Stack>
                  <Typography variant="body2" fontWeight={700}>
                    {formatCurrency(item.value)}
                  </Typography>
                </Stack>
              ))}
            </Stack>
          </SectionCard>

          <Alert severity="info" sx={{ mt: 2.5, borderRadius: 3 }}>
            EMI uses the reducing balance formula: EMI = P x r x (1 + r)^n / ((1 + r)^n - 1), where
            r is the monthly interest rate and n is the number of instalments.
          </Alert>
        </Grid>
      </Grid>
    </Box>
  );
}
```

### frontend/src/pages/AIAssistant.jsx

```jsx
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  Alert,
  Avatar,
  Box,
  Button,
  Chip,
  CircularProgress,
  Divider,
  Drawer,
  IconButton,
  List,
  ListItemButton,
  ListItemText,
  Paper,
  Stack,
  TextField,
  Tooltip,
  Typography,
  useMediaQuery,
  useTheme,
} from "@mui/material";
import SmartToyIcon from "@mui/icons-material/SmartToy";
import SendIcon from "@mui/icons-material/Send";
import AddCommentIcon from "@mui/icons-material/AddComment";
import DeleteSweepIcon from "@mui/icons-material/DeleteSweep";
import HistoryIcon from "@mui/icons-material/History";
import MenuOpenIcon from "@mui/icons-material/MenuOpen";
import { useNavigate } from "react-router-dom";

import ChatMessage from "../components/ChatMessage.jsx";
import { useAuth } from "../context/AuthContext.jsx";
import aiService from "../services/aiService";
import { getErrorMessage } from "../services/api";
import { relativeTime } from "../utils/formatCurrency.js";

const WELCOME = {
  role: "ai",
  text:
    "Hi! I am BankFlow AI, your demo banking assistant.\n\nAsk me things like:\n" +
    "- What is my current balance?\n" +
    "- How much did I spend this month?\n" +
    "- What was my biggest expense?\n" +
    "- What loans do I have?\n" +
    "- Explain EMI",
  meta: { type: "greeting" },
};

export default function AIAssistant() {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("md"));
  const { user } = useAuth();
  const navigate = useNavigate();

  const [messages, setMessages] = useState([WELCOME]);
  const [history, setHistory] = useState([]);
  const [suggestions, setSuggestions] = useState([]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const [error, setError] = useState("");
  const [historyOpen, setHistoryOpen] = useState(false);
  const bottomRef = useRef(null);

  const loadHistory = useCallback(async () => {
    try {
      const data = await aiService.history();
      setHistory(data.results.slice().reverse());
      setSuggestions(data.suggestions || []);
    } catch (err) {
      setError(getErrorMessage(err));
    }
  }, []);

  useEffect(() => {
    loadHistory();
  }, [loadHistory]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, sending]);

  const send = async (question) => {
    const text = (question ?? input).trim();
    if (!text || sending) return;

    setError("");
    setInput("");
    setMessages((prev) => [...prev, { role: "user", text }]);
    setSending(true);

    try {
      const data = await aiService.chat(text);
      setMessages((prev) => [
        ...prev,
        { role: "ai", text: data.response, meta: { type: data.type, provider: data.provider } },
      ]);
      await loadHistory();
    } catch (err) {
      setError(getErrorMessage(err));
      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          text: "I could not reach the banking service just now. Please try again in a moment.",
          meta: { type: "error" },
        },
      ]);
    } finally {
      setSending(false);
    }
  };

  const clearHistory = async () => {
    try {
      await aiService.clearHistory();
      setHistory([]);
      setMessages([WELCOME]);
    } catch (err) {
      setError(getErrorMessage(err));
    }
  };

  const startNewChat = () => {
    setMessages([WELCOME]);
    setHistoryOpen(false);
  };

  const historyPanel = useMemo(
    () => (
      <Box sx={{ display: "flex", flexDirection: "column", height: "100%" }}>
        <Stack direction="row" alignItems="center" spacing={1} sx={{ p: 2 }}>
          <HistoryIcon fontSize="small" color="primary" />
          <Typography variant="subtitle2" sx={{ flexGrow: 1 }}>
            Chat history
          </Typography>
          <Tooltip title="Clear saved history">
            <IconButton size="small" onClick={clearHistory}>
              <DeleteSweepIcon fontSize="small" />
            </IconButton>
          </Tooltip>
        </Stack>
        <Divider />
        <Box sx={{ p: 1.5 }}>
          <Button
            fullWidth
            variant="outlined"
            startIcon={<AddCommentIcon />}
            onClick={startNewChat}
          >
            New chat
          </Button>
        </Box>
        <Divider />
        <List sx={{ px: 1, overflowY: "auto", flexGrow: 1 }}>
          {history.length === 0 && (
            <Typography variant="caption" color="text.secondary" sx={{ p: 2, display: "block" }}>
              No saved conversations yet. Your questions are stored in the demo database so you can
              revisit them.
            </Typography>
          )}
          {history.map((item) => (
            <ListItemButton
              key={item.id}
              sx={{ borderRadius: 2, mb: 0.5, alignItems: "flex-start" }}
              onClick={() => {
                setMessages((prev) => [
                  ...prev,
                  { role: "user", text: item.message },
                  {
                    role: "ai",
                    text: item.response,
                    meta: { type: item.response_type, created_at: item.created_at },
                  },
                ]);
                setHistoryOpen(false);
              }}
            >
              <ListItemText
                primary={item.message}
                secondary={`${item.response_type.replace(/_/g, " ")} - ${relativeTime(item.created_at)}`}
                primaryTypographyProps={{ fontSize: 13, fontWeight: 600, noWrap: false }}
                secondaryTypographyProps={{ fontSize: 11 }}
              />
            </ListItemButton>
          ))}
        </List>
      </Box>
    ),
    [history]
  );

  return (
    <Box sx={{ display: "flex", gap: 2.5, height: { xs: "calc(100vh - 150px)", md: "calc(100vh - 150px)" } }}>
      {/* -------------------------------------------------- history sidebar */}
      {!isMobile && (
        <Paper
          variant="outlined"
          sx={{ width: 280, flexShrink: 0, borderRadius: 3, overflow: "hidden" }}
        >
          {historyPanel}
        </Paper>
      )}

      <Drawer
        anchor="left"
        open={historyOpen}
        onClose={() => setHistoryOpen(false)}
        sx={{ display: { md: "none" } }}
      >
        <Box sx={{ width: 290 }}>{historyPanel}</Box>
      </Drawer>

      {/* ----------------------------------------------------------- chat */}
      <Paper
        variant="outlined"
        sx={{ flexGrow: 1, borderRadius: 3, display: "flex", flexDirection: "column", overflow: "hidden" }}
      >
        <Stack
          direction="row"
          spacing={1.5}
          alignItems="center"
          sx={{ p: 2, borderBottom: "1px solid #e6e9f2" }}
        >
          {isMobile && (
            <IconButton size="small" onClick={() => setHistoryOpen(true)}>
              <MenuOpenIcon />
            </IconButton>
          )}
          <Avatar sx={{ bgcolor: "primary.main" }}>
            <SmartToyIcon fontSize="small" />
          </Avatar>
          <Box sx={{ flexGrow: 1 }}>
            <Typography variant="subtitle1" fontWeight={700} lineHeight={1.2}>
              BankFlow AI
            </Typography>
            <Typography variant="caption" color="text.secondary">
              Grounded in your simulated banking data
            </Typography>
          </Box>
          <Chip size="small" color="success" label="online" />
        </Stack>

        <Box sx={{ flexGrow: 1, overflowY: "auto", p: { xs: 2, md: 3 }, backgroundColor: "#fbfcff" }}>
          {error && (
            <Alert severity="warning" sx={{ mb: 2 }} onClose={() => setError("")}>
              {error}
            </Alert>
          )}

          {messages.map((message, index) => (
            <ChatMessage
              key={`${message.role}-${index}`}
              sender={message.role}
              message={message.text}
              meta={message.meta}
              userName={user?.name}
            />
          ))}

          {sending && (
            <Stack direction="row" spacing={1.5} alignItems="center" sx={{ pl: 1 }}>
              <Avatar sx={{ bgcolor: "primary.main", width: 36, height: 36 }}>
                <SmartToyIcon fontSize="small" />
              </Avatar>
              <Stack direction="row" spacing={1} alignItems="center">
                <CircularProgress size={16} />
                <Typography variant="caption" color="text.secondary">
                  BankFlow AI is checking your demo data...
                </Typography>
              </Stack>
            </Stack>
          )}
          <div ref={bottomRef} />
        </Box>

        {/* ------------------------------------------- suggestions + input */}
        <Box sx={{ p: 2, borderTop: "1px solid #e6e9f2" }}>
          <Stack
            direction="row"
            spacing={1}
            sx={{ mb: 1.5, overflowX: "auto", pb: 0.5 }}
          >
            {suggestions.slice(0, 8).map((suggestion) => (
              <Chip
                key={suggestion}
                label={suggestion}
                size="small"
                variant="outlined"
                onClick={() => send(suggestion)}
                sx={{ whiteSpace: "nowrap" }}
              />
            ))}
          </Stack>

          <Stack direction="row" spacing={1.5} alignItems="flex-end">
            <TextField
              fullWidth
              multiline
              maxRows={4}
              size="small"
              placeholder="Ask about your balance, spending, loans or a banking term..."
              value={input}
              onChange={(event) => setInput(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === "Enter" && !event.shiftKey) {
                  event.preventDefault();
                  send();
                }
              }}
            />
            <Button
              variant="contained"
              onClick={() => send()}
              disabled={sending || !input.trim()}
              endIcon={<SendIcon />}
              sx={{ height: 42 }}
            >
              Send
            </Button>
          </Stack>
          <Typography variant="caption" color="text.secondary" sx={{ display: "block", mt: 1 }}>
            Answers use only your simulated demo data. BankFlow AI cannot move money or access real
            accounts.{" "}
            <Box
              component="span"
              sx={{ color: "primary.main", cursor: "pointer", fontWeight: 600 }}
              onClick={() => navigate("/emi-calculator")}
            >
              Try the EMI calculator
            </Box>
          </Typography>
        </Box>
      </Paper>
    </Box>
  );
}
```

### frontend/src/pages/Notifications.jsx

```jsx
import { useCallback, useEffect, useMemo, useState } from "react";
import {
  Box,
  Button,
  Chip,
  Divider,
  Grid,
  IconButton,
  Paper,
  Stack,
  Tab,
  Tabs,
  Tooltip,
  Typography,
} from "@mui/material";
import NotificationsActiveIcon from "@mui/icons-material/NotificationsActive";
import PaymentsIcon from "@mui/icons-material/Payments";
import SecurityIcon from "@mui/icons-material/Security";
import RequestQuoteIcon from "@mui/icons-material/RequestQuote";
import InsightsIcon from "@mui/icons-material/Insights";
import DoneAllIcon from "@mui/icons-material/DoneAll";
import MarkEmailReadIcon from "@mui/icons-material/MarkEmailRead";

import { EmptyState, ErrorAlert, Loader, PageHeader } from "../components/Common.jsx";
import bankingService from "../services/bankingService";
import { getErrorMessage } from "../services/api";
import { relativeTime } from "../utils/formatCurrency.js";

const ICONS = {
  TRANSACTION: <PaymentsIcon />,
  SECURITY: <SecurityIcon />,
  LOAN: <RequestQuoteIcon />,
  SUMMARY: <InsightsIcon />,
  SYSTEM: <NotificationsActiveIcon />,
};

export default function Notifications() {
  const [notifications, setNotifications] = useState([]);
  const [tab, setTab] = useState("all");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      setNotifications(await bankingService.getNotifications());
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  const toggleRead = async (notification) => {
    try {
      const updated = await bankingService.markNotificationRead(
        notification.id,
        !notification.is_read
      );
      setNotifications((prev) =>
        prev.map((item) => (item.id === updated.id ? { ...item, is_read: updated.is_read } : item))
      );
    } catch (err) {
      setError(getErrorMessage(err));
    }
  };

  const markAll = async () => {
    try {
      await bankingService.markAllNotificationsRead();
      setNotifications((prev) => prev.map((item) => ({ ...item, is_read: true })));
    } catch (err) {
      setError(getErrorMessage(err));
    }
  };

  const filtered = useMemo(() => {
    if (tab === "unread") return notifications.filter((item) => !item.is_read);
    if (tab === "read") return notifications.filter((item) => item.is_read);
    return notifications;
  }, [notifications, tab]);

  const unread = notifications.filter((item) => !item.is_read).length;

  if (loading) return <Loader label="Loading notifications..." />;

  return (
    <Box>
      <PageHeader
        title="Notifications"
        subtitle={`${unread} unread simulated alert${unread === 1 ? "" : "s"}`}
        action={
          <Button startIcon={<DoneAllIcon />} onClick={markAll} disabled={unread === 0}>
            Mark all as read
          </Button>
        }
      />

      <ErrorAlert message={error} onRetry={load} />

      <Tabs
        value={tab}
        onChange={(_, value) => setTab(value)}
        sx={{ mb: 2, borderBottom: "1px solid #e6e9f2" }}
      >
        <Tab value="all" label={`All (${notifications.length})`} />
        <Tab value="unread" label={`Unread (${unread})`} />
        <Tab value="read" label={`Read (${notifications.length - unread})`} />
      </Tabs>

      {filtered.length === 0 ? (
        <EmptyState
          title="Nothing here"
          description="Simulated banking alerts will show up in this list."
        />
      ) : (
        <Grid container spacing={2}>
          {filtered.map((item) => (
            <Grid item xs={12} key={item.id}>
              <Paper
                variant="outlined"
                sx={{
                  p: 2,
                  borderRadius: 3,
                  borderLeft: item.is_read ? "4px solid #e6e9f2" : "4px solid #1b3a8f",
                  backgroundColor: item.is_read ? "#ffffff" : "#f8faff",
                }}
              >
                <Stack direction="row" spacing={2} alignItems="flex-start">
                  <Box
                    sx={{
                      display: "grid",
                      placeItems: "center",
                      width: 42,
                      height: 42,
                      borderRadius: 2,
                      backgroundColor: "#eef2fd",
                      color: "primary.main",
                      flexShrink: 0,
                    }}
                  >
                    {ICONS[item.notification_type] || ICONS.SYSTEM}
                  </Box>
                  <Box sx={{ flexGrow: 1 }}>
                    <Stack direction="row" spacing={1} alignItems="center" sx={{ flexWrap: "wrap" }}>
                      <Typography variant="subtitle1" fontWeight={700}>
                        {item.title}
                      </Typography>
                      {!item.is_read && <Chip size="small" color="primary" label="new" />}
                      <Chip
                        size="small"
                        variant="outlined"
                        label={item.notification_type.toLowerCase()}
                      />
                    </Stack>
                    <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
                      {item.message}
                    </Typography>
                    <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: "block" }}>
                      {relativeTime(item.created_at)}
                    </Typography>
                  </Box>
                  <Tooltip title={item.is_read ? "Mark as unread" : "Mark as read"}>
                    <IconButton onClick={() => toggleRead(item)}>
                      {item.is_read ? <MarkEmailReadIcon color="disabled" /> : <MarkEmailReadIcon color="primary" />}
                    </IconButton>
                  </Tooltip>
                </Stack>
              </Paper>
            </Grid>
          ))}
        </Grid>
      )}

      <Divider sx={{ my: 3 }} />
      <Typography variant="caption" color="text.secondary">
        These alerts are generated by the demo seed data. No real banking notifications are sent.
      </Typography>
    </Box>
  );
}
```

### frontend/src/pages/Profile.jsx

```jsx
import { useEffect, useState } from "react";
import {
  Alert,
  Avatar,
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Divider,
  Grid,
  Snackbar,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import SaveIcon from "@mui/icons-material/Save";

import { ErrorAlert, Loader, PageHeader, SectionCard } from "../components/Common.jsx";
import { useAuth } from "../context/AuthContext.jsx";
import authService from "../services/authService";
import { getErrorMessage } from "../services/api";
import { formatCurrency, formatDate, initials } from "../utils/formatCurrency.js";

export default function Profile() {
  const { reloadProfile, user } = useAuth();
  const [profile, setProfile] = useState(null);
  const [form, setForm] = useState({ name: "", phone: "", address: "", occupation: "", monthly_income: 0 });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [errors, setErrors] = useState({});
  const [snack, setSnack] = useState("");

  useEffect(() => {
    (async () => {
      try {
        const data = await authService.profile();
        setProfile(data);
        setForm({
          name: data.user.name || "",
          phone: data.phone || "",
          address: data.address || "",
          occupation: data.occupation || "",
          monthly_income: data.monthly_income || 0,
        });
      } catch (err) {
        setError(getErrorMessage(err));
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const handleSave = async (event) => {
    event.preventDefault();
    const nextErrors = {};
    if (!form.name.trim()) nextErrors.name = "Name cannot be empty.";
    if (form.phone && !/^[+0-9\s-]{8,20}$/.test(form.phone)) {
      nextErrors.phone = "Enter a valid phone number.";
    }
    setErrors(nextErrors);
    if (Object.keys(nextErrors).length) return;

    setSaving(true);
    setError("");
    try {
      const updated = await authService.updateProfile(form);
      setProfile(updated);
      await reloadProfile();
      setSnack("Profile updated successfully.");
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <Loader label="Loading your demo profile..." />;

  return (
    <Box>
      <PageHeader title="Profile" subtitle="Update your demo contact details and review your account." />
      <ErrorAlert message={error} />

      <Grid container spacing={2.5}>
        <Grid item xs={12} md={4}>
          <Card sx={{ borderRadius: 4 }}>
            <CardContent sx={{ textAlign: "center", py: 4 }}>
              <Avatar
                sx={{
                  width: 88,
                  height: 88,
                  mx: "auto",
                  bgcolor: "primary.main",
                  fontSize: 30,
                  fontWeight: 700,
                }}
              >
                {initials(form.name || user?.name || "BF")}
              </Avatar>
              <Typography variant="h6" sx={{ mt: 2 }}>
                {form.name || user?.name}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                {user?.email}
              </Typography>
              <Stack direction="row" spacing={1} justifyContent="center" sx={{ mt: 2 }}>
                <Chip size="small" color="primary" label={user?.role === "ADMIN" ? "Bank Employee" : "Customer"} />
                <Chip size="small" variant="outlined" label="Demo profile" />
              </Stack>
              <Divider sx={{ my: 3 }} />
              <Stack spacing={1} sx={{ textAlign: "left", px: 1 }}>
                <Stack direction="row" justifyContent="space-between">
                  <Typography variant="body2" color="text.secondary">
                    Member since
                  </Typography>
                  <Typography variant="body2" fontWeight={700}>
                    {formatDate(profile?.user?.date_joined || profile?.created_at)}
                  </Typography>
                </Stack>
                <Stack direction="row" justifyContent="space-between">
                  <Typography variant="body2" color="text.secondary">
                    Employment
                  </Typography>
                  <Typography variant="body2" fontWeight={700}>
                    {profile?.employment_type?.replace("_", " ").toLowerCase()}
                  </Typography>
                </Stack>
                <Stack direction="row" justifyContent="space-between">
                  <Typography variant="body2" color="text.secondary">
                    Monthly income
                  </Typography>
                  <Typography variant="body2" fontWeight={700}>
                    {formatCurrency(profile?.monthly_income || 0)}
                  </Typography>
                </Stack>
              </Stack>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={8}>
          <SectionCard title="Personal details" subtitle="Name and phone are editable in this demo">
            <form onSubmit={handleSave}>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Full name"
                    value={form.name}
                    onChange={(event) => setForm({ ...form, name: event.target.value })}
                    error={Boolean(errors.name)}
                    helperText={errors.name}
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Email (read only)"
                    value={user?.email || ""}
                    disabled
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Phone"
                    value={form.phone}
                    onChange={(event) => setForm({ ...form, phone: event.target.value })}
                    error={Boolean(errors.phone)}
                    helperText={errors.phone}
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Occupation"
                    value={form.occupation}
                    onChange={(event) => setForm({ ...form, occupation: event.target.value })}
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    label="Address"
                    value={form.address}
                    onChange={(event) => setForm({ ...form, address: event.target.value })}
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    type="number"
                    label="Monthly income"
                    value={form.monthly_income}
                    onChange={(event) =>
                      setForm({ ...form, monthly_income: Number(event.target.value) })
                    }
                  />
                </Grid>
              </Grid>

              <Stack direction="row" spacing={2} sx={{ mt: 3 }}>
                <Button
                  type="submit"
                  variant="contained"
                  startIcon={<SaveIcon />}
                  disabled={saving}
                >
                  {saving ? "Saving..." : "Save changes"}
                </Button>
                <Button
                  onClick={() =>
                    setForm({
                      name: profile?.user?.name || "",
                      phone: profile?.phone || "",
                      address: profile?.address || "",
                      occupation: profile?.occupation || "",
                      monthly_income: profile?.monthly_income || 0,
                    })
                  }
                >
                  Reset
                </Button>
              </Stack>
            </form>
          </SectionCard>

          <Alert severity="info" sx={{ mt: 2.5, borderRadius: 3 }}>
            Profile pictures are shown as initials in this demo. Email addresses cannot be changed
            because they identify the login.
          </Alert>
        </Grid>
      </Grid>

      <Snackbar
        open={Boolean(snack)}
        autoHideDuration={3000}
        onClose={() => setSnack("")}
        message={snack}
      />
    </Box>
  );
}
```

### frontend/src/pages/NotFound.jsx

```jsx
import { Box, Button, Container, Stack, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext.jsx";

export default function NotFound() {
  const navigate = useNavigate();
  const { isAuthenticated, isAdmin } = useAuth();

  return (
    <Container maxWidth="sm">
      <Box sx={{ minHeight: "100vh", display: "grid", placeItems: "center", textAlign: "center" }}>
        <Stack spacing={2} alignItems="center">
          <Typography variant="h1" sx={{ fontSize: 84, color: "primary.main", fontWeight: 800 }}>
            404
          </Typography>
          <Typography variant="h5">This page is not part of the demo</Typography>
          <Typography color="text.secondary">
            The link you followed may be broken, or the page may have moved. Everything else in
            BankFlow is still working fine.
          </Typography>
          <Stack direction={{ xs: "column", sm: "row" }} spacing={2} sx={{ pt: 1 }}>
            <Button variant="contained" onClick={() => navigate(isAuthenticated ? (isAdmin ? "/admin" : "/dashboard") : "/")}>
              {isAuthenticated ? "Back to dashboard" : "Back to home"}
            </Button>
            <Button variant="outlined" onClick={() => navigate("/assistant")}>
              Ask BankFlow AI
            </Button>
          </Stack>
        </Stack>
      </Box>
    </Container>
  );
}
```

## 9. FRONTEND - BANK EMPLOYEE (ADMIN) PAGES

### frontend/src/pages/admin/AdminDashboard.jsx

```jsx
import { useCallback, useEffect, useState } from "react";
import {
  Box,
  Button,
  Divider,
  Grid,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material";
import GroupIcon from "@mui/icons-material/Group";
import AccountBalanceIcon from "@mui/icons-material/AccountBalance";
import ReceiptLongIcon from "@mui/icons-material/ReceiptLong";
import RequestQuoteIcon from "@mui/icons-material/RequestQuote";
import HourglassBottomIcon from "@mui/icons-material/HourglassBottom";
import PaymentsIcon from "@mui/icons-material/Payments";
import ArrowForwardIcon from "@mui/icons-material/ArrowForward";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip as ChartTooltip,
  XAxis,
  YAxis,
} from "recharts";
import { useNavigate } from "react-router-dom";

import DashboardCard from "../../components/DashboardCard.jsx";
import { ErrorAlert, Loader, PageHeader, SectionCard, StatusChip } from "../../components/Common.jsx";
import adminService from "../../services/adminService";
import { getErrorMessage } from "../../services/api";
import { CATEGORY_COLORS, formatCurrency } from "../../utils/formatCurrency.js";

export default function AdminDashboard() {
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      setData(await adminService.analytics());
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  if (loading) return <Loader label="Loading bank employee dashboard..." minHeight="60vh" />;

  if (error) {
    return (
      <>
        <PageHeader title="Admin Dashboard" />
        <ErrorAlert message={error} onRetry={load} />
      </>
    );
  }

  const { totals, monthly_trend: trend, category_breakdown: categories } = data;

  return (
    <Box>
      <PageHeader
        title="Bank employee dashboard"
        subtitle="Demo portfolio overview across every fictional customer."
        action={
          <Button endIcon={<ArrowForwardIcon />} onClick={() => navigate("/admin/analytics")}>
            Open analytics
          </Button>
        }
      />

      <Grid container spacing={2.5}>
        <Grid item xs={12} sm={6} lg={4} xl={2}>
          <DashboardCard
            title="Total Customers"
            value={totals.customers}
            icon={<GroupIcon />}
            caption="Fictional demo customers"
            gradient="linear-gradient(135deg, #1b3a8f 0%, #4361ee 100%)"
          />
        </Grid>
        <Grid item xs={12} sm={6} lg={4} xl={2}>
          <DashboardCard
            title="Total Accounts"
            value={totals.accounts}
            icon={<AccountBalanceIcon />}
            caption={`Deposits ${formatCurrency(totals.total_deposits, { compact: true })}`}
          />
        </Grid>
        <Grid item xs={12} sm={6} lg={4} xl={2}>
          <DashboardCard
            title="Total Transactions"
            value={totals.transactions}
            icon={<ReceiptLongIcon />}
            caption="Across all demo accounts"
          />
        </Grid>
        <Grid item xs={12} sm={6} lg={4} xl={2}>
          <DashboardCard
            title="Total Loans"
            value={totals.loans}
            icon={<RequestQuoteIcon />}
            caption={`Outstanding ${formatCurrency(totals.outstanding, { compact: true })}`}
          />
        </Grid>
        <Grid item xs={12} sm={6} lg={4} xl={2}>
          <DashboardCard
            title="Pending Loans"
            value={totals.pending_loans}
            icon={<HourglassBottomIcon />}
            caption="Awaiting employee review"
            color="#f59e0b"
          />
        </Grid>
        <Grid item xs={12} sm={6} lg={4} xl={2}>
          <DashboardCard
            title="Demo Volume"
            value={formatCurrency(totals.demo_volume, { compact: true })}
            icon={<PaymentsIcon />}
            caption="Simulated transaction volume"
            color="#16a34a"
          />
        </Grid>
      </Grid>

      <Grid container spacing={2.5} sx={{ mt: 0.5 }}>
        <Grid item xs={12} lg={7}>
          <SectionCard title="Portfolio income vs expenses" subtitle="Last 6 months">
            <Box sx={{ height: 300 }}>
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={trend}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#eef1f8" />
                  <XAxis dataKey="short_month" tick={{ fontSize: 12 }} />
                  <YAxis tick={{ fontSize: 12 }} tickFormatter={(v) => `${v / 1000}k`} />
                  <ChartTooltip formatter={(value) => formatCurrency(value)} />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="income"
                    name="Income"
                    stroke="#16a34a"
                    strokeWidth={2.5}
                    dot={{ r: 3 }}
                  />
                  <Line
                    type="monotone"
                    dataKey="expense"
                    name="Expense"
                    stroke="#e11d48"
                    strokeWidth={2.5}
                    dot={{ r: 3 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </Box>
          </SectionCard>
        </Grid>

        <Grid item xs={12} lg={5}>
          <SectionCard title="Demo transaction volume by category" subtitle="All customers">
            <Box sx={{ height: 300 }}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={categories}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#eef1f8" />
                  <XAxis dataKey="category" tick={{ fontSize: 11 }} interval={0} angle={-20} dy={10} height={50} />
                  <YAxis tick={{ fontSize: 12 }} tickFormatter={(v) => `${v / 1000}k`} />
                  <ChartTooltip formatter={(value) => formatCurrency(value)} />
                  <Bar dataKey="amount" name="Amount" radius={[6, 6, 0, 0]} maxBarSize={38}>
                    {categories.map((entry) => (
                      <Cell key={entry.category} fill={entry.color || CATEGORY_COLORS[entry.category]} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </Box>
          </SectionCard>
        </Grid>

        <Grid item xs={12} md={5}>
          <SectionCard title="Loan status mix" subtitle="Every demo loan application">
            <Box sx={{ height: 240 }}>
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={data.loan_status_breakdown.filter((item) => item.count > 0)}
                    dataKey="count"
                    nameKey="label"
                    innerRadius={50}
                    outerRadius={82}
                    paddingAngle={3}
                  >
                    {data.loan_status_breakdown.map((entry, index) => (
                      <Cell
                        key={entry.status}
                        fill={["#f59e0b", "#0ea5e9", "#e11d48", "#16a34a", "#64748b"][index % 5]}
                      />
                    ))}
                  </Pie>
                  <ChartTooltip />
                </PieChart>
              </ResponsiveContainer>
            </Box>
            <Stack spacing={1} sx={{ mt: 1 }}>
              {data.loan_status_breakdown.map((item) => (
                <Stack key={item.status} direction="row" justifyContent="space-between">
                  <StatusChip status={item.status} />
                  <Typography variant="body2" fontWeight={700}>
                    {item.count}
                  </Typography>
                </Stack>
              ))}
            </Stack>
          </SectionCard>
        </Grid>

        <Grid item xs={12} md={7}>
          <SectionCard
            title="Top customers by balance"
            subtitle="Fictional demo customers only"
            action={
              <Button size="small" onClick={() => navigate("/admin/customers")}>
                Manage customers
              </Button>
            }
          >
            <TableContainer>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>Customer</TableCell>
                    <TableCell align="right">Balance</TableCell>
                    <TableCell align="right">Transactions</TableCell>
                    <TableCell align="right">Loans</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {data.top_customers.map((customer) => (
                    <TableRow key={customer.id} hover>
                      <TableCell>
                        <Typography variant="body2" fontWeight={600}>
                          {customer.name}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          {customer.email}
                        </Typography>
                      </TableCell>
                      <TableCell align="right">{formatCurrency(customer.balance)}</TableCell>
                      <TableCell align="right">{customer.transactions}</TableCell>
                      <TableCell align="right">{customer.loans}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
            <Divider sx={{ my: 2 }} />
            <Stack direction="row" spacing={2} sx={{ flexWrap: "wrap", gap: 2 }}>
              {data.transaction_type_split.map((item) => (
                <Box key={item.type}>
                  <Typography variant="caption" color="text.secondary">
                    {item.label}
                  </Typography>
                  <Typography variant="h6">{item.count}</Typography>
                </Box>
              ))}
            </Stack>
          </SectionCard>
        </Grid>
      </Grid>
    </Box>
  );
}
```

### frontend/src/pages/admin/CustomerManagement.jsx

```jsx
import { useCallback, useEffect, useState } from "react";
import {
  Box,
  Button,
  Chip,
  Dialog,
  DialogContent,
  DialogTitle,
  Divider,
  Grid,
  InputAdornment,
  Paper,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import VisibilityIcon from "@mui/icons-material/Visibility";

import { ErrorAlert, Loader, PageHeader, SectionCard, StatusChip } from "../../components/Common.jsx";
import adminService from "../../services/adminService";
import { getErrorMessage } from "../../services/api";
import { formatCurrency, formatDate } from "../../utils/formatCurrency.js";

export default function CustomerManagement() {
  const [customers, setCustomers] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [detail, setDetail] = useState(null);
  const [detailLoading, setDetailLoading] = useState(false);

  const load = useCallback(async (term = "") => {
    setLoading(true);
    setError("");
    try {
      const data = await adminService.customers(term ? { search: term } : {});
      setCustomers(data.results);
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  const openDetail = async (id) => {
    setDetailLoading(true);
    setDetail({});
    try {
      setDetail(await adminService.customer(id));
    } catch (err) {
      setError(getErrorMessage(err));
      setDetail(null);
    } finally {
      setDetailLoading(false);
    }
  };

  return (
    <Box>
      <PageHeader
        title="Customer Management"
        subtitle={`${customers.length} fictional demo customer${customers.length === 1 ? "" : "s"} in the portfolio.`}
      />

      <ErrorAlert message={error} onRetry={() => load(search)} />

      <Paper variant="outlined" sx={{ p: 2.5, borderRadius: 3 }}>
        <Stack direction={{ xs: "column", sm: "row" }} spacing={2} sx={{ mb: 2 }}>
          <TextField
            size="small"
            placeholder="Search by name or email"
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            onKeyDown={(event) => event.key === "Enter" && load(search)}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon fontSize="small" />
                </InputAdornment>
              ),
            }}
            sx={{ flexGrow: 1 }}
          />
          <Button variant="contained" onClick={() => load(search)}>
            Search
          </Button>
          <Button
            onClick={() => {
              setSearch("");
              load("");
            }}
          >
            Clear
          </Button>
        </Stack>

        {loading ? (
          <Loader label="Loading customers..." minHeight={200} />
        ) : (
          <TableContainer>
            <Table size="small" sx={{ minWidth: 860 }}>
              <TableHead>
                <TableRow>
                  <TableCell>Customer</TableCell>
                  <TableCell>Phone</TableCell>
                  <TableCell>Account</TableCell>
                  <TableCell align="right">Balance</TableCell>
                  <TableCell align="right">Txns</TableCell>
                  <TableCell align="right">Loans</TableCell>
                  <TableCell>Joined</TableCell>
                  <TableCell align="right">Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {customers.map((customer) => (
                  <TableRow key={customer.id} hover>
                    <TableCell>
                      <Typography variant="body2" fontWeight={600}>
                        {customer.name}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        {customer.email}
                      </Typography>
                    </TableCell>
                    <TableCell>{customer.phone || "-"}</TableCell>
                    <TableCell>
                      <Typography variant="caption">{customer.masked_account_number || "-"}</Typography>
                      <Typography variant="caption" color="text.secondary" display="block">
                        {customer.account_type || ""}
                      </Typography>
                    </TableCell>
                    <TableCell align="right">{formatCurrency(customer.balance)}</TableCell>
                    <TableCell align="right">{customer.transaction_count}</TableCell>
                    <TableCell align="right">{customer.loan_count}</TableCell>
                    <TableCell>{formatDate(customer.joined)}</TableCell>
                    <TableCell align="right">
                      <Button
                        size="small"
                        startIcon={<VisibilityIcon fontSize="small" />}
                        onClick={() => openDetail(customer.id)}
                      >
                        View
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </Paper>

      <Dialog open={Boolean(detail)} onClose={() => setDetail(null)} maxWidth="md" fullWidth>
        <DialogTitle>Customer 360 view</DialogTitle>
        <DialogContent dividers>
          {detailLoading ? (
            <Loader label="Loading customer profile..." minHeight={200} />
          ) : (
            detail?.customer && (
              <Box>
                <Stack
                  direction={{ xs: "column", sm: "row" }}
                  spacing={2}
                  alignItems={{ xs: "flex-start", sm: "center" }}
                  sx={{ mb: 2 }}
                >
                  <Box sx={{ flexGrow: 1 }}>
                    <Typography variant="h6">{detail.customer.name}</Typography>
                    <Typography variant="body2" color="text.secondary">
                      {detail.customer.email} • joined {formatDate(detail.customer.joined)}
                    </Typography>
                  </Box>
                  <Chip
                    label={detail.customer.is_active ? "Active login" : "Disabled"}
                    color={detail.customer.is_active ? "success" : "default"}
                  />
                  <Chip label={detail.customer.role} color="primary" variant="outlined" />
                </Stack>

                <Grid container spacing={2}>
                  {detail.accounts.map((account) => (
                    <Grid item xs={12} sm={6} key={account.id}>
                      <SectionCard title={account.account_type_display} subtitle={account.masked_account_number}>
                        <Typography variant="h6">{formatCurrency(account.balance)}</Typography>
                        <Stack direction="row" spacing={1} sx={{ mt: 1 }}>
                          <StatusChip status={account.status} />
                          <Chip size="small" variant="outlined" label={account.ifsc_code} />
                        </Stack>
                      </SectionCard>
                    </Grid>
                  ))}
                  <Grid item xs={12} sm={6}>
                    <SectionCard title="Profile details">
                      {[
                        ["Phone", detail.customer.profile?.phone || "-"],
                        ["Occupation", detail.customer.profile?.occupation || "-"],
                        [
                          "Employment",
                          detail.customer.profile?.employment_type?.replace("_", " ").toLowerCase() || "-",
                        ],
                        ["Monthly income", formatCurrency(detail.customer.profile?.monthly_income || 0)],
                      ].map(([label, value]) => (
                        <Stack key={label} direction="row" justifyContent="space-between" sx={{ py: 0.75 }}>
                          <Typography variant="body2" color="text.secondary">
                            {label}
                          </Typography>
                          <Typography variant="body2" fontWeight={600}>
                            {value}
                          </Typography>
                        </Stack>
                      ))}
                    </SectionCard>
                  </Grid>
                </Grid>

                <Typography variant="subtitle1" sx={{ mt: 3, mb: 1 }}>
                  Demo loans
                </Typography>
                {detail.loans.length === 0 ? (
                  <Typography variant="body2" color="text.secondary">
                    No loans on record for this customer.
                  </Typography>
                ) : (
                  <TableContainer>
                    <Table size="small">
                      <TableHead>
                        <TableRow>
                          <TableCell>Loan</TableCell>
                          <TableCell align="right">Amount</TableCell>
                          <TableCell align="right">EMI</TableCell>
                          <TableCell align="right">Outstanding</TableCell>
                          <TableCell>Status</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {detail.loans.map((loan) => (
                          <TableRow key={loan.id}>
                            <TableCell>
                              {loan.loan_type_display}
                              <Typography variant="caption" color="text.secondary" display="block">
                                {loan.loan_id}
                              </Typography>
                            </TableCell>
                            <TableCell align="right">{formatCurrency(loan.amount)}</TableCell>
                            <TableCell align="right">{formatCurrency(loan.emi)}</TableCell>
                            <TableCell align="right">
                              {formatCurrency(loan.remaining_amount)}
                            </TableCell>
                            <TableCell>
                              <StatusChip status={loan.status} />
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                )}

                <Divider sx={{ my: 3 }} />
                <Typography variant="caption" color="text.secondary">
                  This dialog only exposes simulated demo data. No real customer information is
                  stored in BankFlow.
                </Typography>
              </Box>
            )
          )}
        </DialogContent>
      </Dialog>
    </Box>
  );
}
```

### frontend/src/pages/admin/TransactionManagement.jsx

```jsx
import { useCallback, useEffect, useMemo, useState } from "react";
import {
  Box,
  Card,
  CardContent,
  Grid,
  InputAdornment,
  MenuItem,
  Paper,
  Stack,
  TablePagination,
  TextField,
  Typography,
} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";

import TransactionTable from "../../components/TransactionTable.jsx";
import { ErrorAlert, PageHeader } from "../../components/Common.jsx";
import adminService from "../../services/adminService";
import { getErrorMessage } from "../../services/api";
import { TRANSACTION_CATEGORIES, formatCurrency } from "../../utils/formatCurrency.js";

export default function TransactionManagement() {
  const [filters, setFilters] = useState({
    search: "",
    category: "ALL",
    type: "ALL",
    start_date: "",
    end_date: "",
  });
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [data, setData] = useState({ results: [], count: 0, summary: null });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const timer = setTimeout(() => setSearch(filters.search), 400);
    return () => clearTimeout(timer);
  }, [filters.search]);

  const query = useMemo(
    () => ({
      page: page + 1,
      page_size: rowsPerPage,
      search: search || undefined,
      category: filters.category,
      type: filters.type,
      start_date: filters.start_date || undefined,
      end_date: filters.end_date || undefined,
    }),
    [page, rowsPerPage, search, filters.category, filters.type, filters.start_date, filters.end_date]
  );

  const load = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const response = await adminService.transactions(query);
      setData({ results: response.results, count: response.count, summary: response.summary });
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, [query]);

  useEffect(() => {
    load();
  }, [load]);

  return (
    <Box>
      <PageHeader
        title="Transaction Management"
        subtitle="Every simulated transaction across all demo customers."
      />

      <ErrorAlert message={error} onRetry={load} />

      <Grid container spacing={2.5} sx={{ mb: 2.5 }}>
        <Grid item xs={12} sm={6}>
          <Card>
            <CardContent>
              <Typography variant="caption" color="text.secondary">
                Filtered transactions
              </Typography>
              <Typography variant="h6">{data.summary?.count ?? data.count}</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6}>
          <Card>
            <CardContent>
              <Typography variant="caption" color="text.secondary">
                Filtered demo volume
              </Typography>
              <Typography variant="h6">{formatCurrency(data.summary?.volume || 0)}</Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Paper variant="outlined" sx={{ p: 2.5, borderRadius: 3 }}>
        <Grid container spacing={2} sx={{ mb: 2 }}>
          <Grid item xs={12} md={4}>
            <TextField
              fullWidth
              size="small"
              placeholder="Search customer, description or ID"
              value={filters.search}
              onChange={(event) => {
                setPage(0);
                setFilters({ ...filters, search: event.target.value });
              }}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <SearchIcon fontSize="small" />
                  </InputAdornment>
                ),
              }}
            />
          </Grid>
          <Grid item xs={6} md={2}>
            <TextField
              fullWidth
              select
              size="small"
              label="Category"
              value={filters.category}
              onChange={(event) => {
                setPage(0);
                setFilters({ ...filters, category: event.target.value });
              }}
            >
              <MenuItem value="ALL">All categories</MenuItem>
              {TRANSACTION_CATEGORIES.map((category) => (
                <MenuItem key={category} value={category}>
                  {category}
                </MenuItem>
              ))}
            </TextField>
          </Grid>
          <Grid item xs={6} md={2}>
            <TextField
              fullWidth
              select
              size="small"
              label="Type"
              value={filters.type}
              onChange={(event) => {
                setPage(0);
                setFilters({ ...filters, type: event.target.value });
              }}
            >
              <MenuItem value="ALL">All types</MenuItem>
              <MenuItem value="CREDIT">Credit</MenuItem>
              <MenuItem value="DEBIT">Debit</MenuItem>
            </TextField>
          </Grid>
          <Grid item xs={6} md={2}>
            <TextField
              fullWidth
              size="small"
              type="date"
              label="From"
              InputLabelProps={{ shrink: true }}
              value={filters.start_date}
              onChange={(event) => {
                setPage(0);
                setFilters({ ...filters, start_date: event.target.value });
              }}
            />
          </Grid>
          <Grid item xs={6} md={2}>
            <TextField
              fullWidth
              size="small"
              type="date"
              label="To"
              InputLabelProps={{ shrink: true }}
              value={filters.end_date}
              onChange={(event) => {
                setPage(0);
                setFilters({ ...filters, end_date: event.target.value });
              }}
            />
          </Grid>
        </Grid>

        <TransactionTable
          transactions={data.results}
          loading={loading}
          showCustomer
          basePath="/admin/transactions"
          emptyTitle="No transactions match these filters"
        />

        {!loading && data.count > 0 && (
          <TablePagination
            component="div"
            count={data.count}
            page={page}
            onPageChange={(_, newPage) => setPage(newPage)}
            rowsPerPage={rowsPerPage}
            onRowsPerPageChange={(event) => {
              setRowsPerPage(parseInt(event.target.value, 10));
              setPage(0);
            }}
            rowsPerPageOptions={[5, 10, 25]}
          />
        )}
      </Paper>

      <Stack sx={{ mt: 2 }}>
        <Typography variant="caption" color="text.secondary">
          Transactions are read-only in the bank employee area - this demo never moves real money.
        </Typography>
      </Stack>
    </Box>
  );
}
```

### frontend/src/pages/admin/LoanManagement.jsx

```jsx
import { useCallback, useEffect, useState } from "react";
import {
  Box,
  Button,
  Chip,
  InputAdornment,
  MenuItem,
  Paper,
  Snackbar,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import CheckCircleOutlineIcon from "@mui/icons-material/CheckCircleOutline";
import HighlightOffIcon from "@mui/icons-material/HighlightOff";
import PlayCircleOutlineIcon from "@mui/icons-material/PlayCircleOutline";

import { EmptyState, ErrorAlert, Loader, PageHeader, StatusChip } from "../../components/Common.jsx";
import adminService from "../../services/adminService";
import { getErrorMessage } from "../../services/api";
import { LOAN_TYPES, formatCurrency, formatDate } from "../../utils/formatCurrency.js";

const STATUS_OPTIONS = ["ALL", "PENDING", "APPROVED", "ACTIVE", "REJECTED", "COMPLETED"];

export default function LoanManagement() {
  const [loans, setLoans] = useState([]);
  const [filters, setFilters] = useState({ search: "", status: "ALL", type: "ALL" });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [snack, setSnack] = useState("");
  const [updatingId, setUpdatingId] = useState(null);

  const load = useCallback(async (currentFilters = filters) => {
    setLoading(true);
    setError("");
    try {
      const data = await adminService.loans({
        search: currentFilters.search || undefined,
        status: currentFilters.status,
        type: currentFilters.type,
      });
      setLoans(data.results);
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, [filters]);

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filters.status, filters.type]);

  const changeStatus = async (loan, status) => {
    setUpdatingId(loan.id);
    try {
      const updated = await adminService.updateLoanStatus(loan.id, status);
      setLoans((prev) => prev.map((item) => (item.id === updated.id ? updated : item)));
      setSnack(
        `${updated.loan_id} marked as ${updated.status_display}. The customer received a demo notification.`
      );
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setUpdatingId(null);
    }
  };

  const pending = loans.filter((loan) => loan.status === "PENDING").length;

  return (
    <Box>
      <PageHeader
        title="Loan Management"
        subtitle={`${loans.length} demo loan applications in view • ${pending} awaiting a decision`}
      />

      <ErrorAlert message={error} onRetry={() => load()} />

      <Paper variant="outlined" sx={{ p: 2.5, borderRadius: 3 }}>
        <Stack direction={{ xs: "column", md: "row" }} spacing={2} sx={{ mb: 2 }}>
          <TextField
            size="small"
            placeholder="Search by loan ID, customer name or email"
            value={filters.search}
            onChange={(event) => setFilters({ ...filters, search: event.target.value })}
            onKeyDown={(event) => event.key === "Enter" && load(filters)}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon fontSize="small" />
                </InputAdornment>
              ),
            }}
            sx={{ flexGrow: 1 }}
          />
          <TextField
            select
            size="small"
            label="Status"
            value={filters.status}
            onChange={(event) => setFilters({ ...filters, status: event.target.value })}
            sx={{ minWidth: 160 }}
          >
            {STATUS_OPTIONS.map((status) => (
              <MenuItem key={status} value={status}>
                {status === "ALL" ? "All statuses" : status.toLowerCase()}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            select
            size="small"
            label="Loan type"
            value={filters.type}
            onChange={(event) => setFilters({ ...filters, type: event.target.value })}
            sx={{ minWidth: 170 }}
          >
            <MenuItem value="ALL">All loan types</MenuItem>
            {LOAN_TYPES.map((type) => (
              <MenuItem key={type.value} value={type.value}>
                {type.label}
              </MenuItem>
            ))}
          </TextField>
          <Button variant="contained" onClick={() => load(filters)}>
            Apply
          </Button>
        </Stack>

        {loading ? (
          <Loader label="Loading demo loans..." minHeight={200} />
        ) : loans.length === 0 ? (
          <EmptyState title="No loans match these filters" description="Try another status or loan type." />
        ) : (
          <TableContainer>
            <Table size="small" sx={{ minWidth: 980 }}>
              <TableHead>
                <TableRow>
                  <TableCell>Loan ID</TableCell>
                  <TableCell>Customer</TableCell>
                  <TableCell>Type</TableCell>
                  <TableCell align="right">Amount</TableCell>
                  <TableCell align="right">Interest</TableCell>
                  <TableCell align="right">Tenure</TableCell>
                  <TableCell align="right">EMI</TableCell>
                  <TableCell align="right">Outstanding</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell align="right">Decision</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {loans.map((loan) => (
                  <TableRow key={loan.id} hover>
                    <TableCell>
                      <Typography variant="caption" fontWeight={700}>
                        {loan.loan_id}
                      </Typography>
                      <Typography variant="caption" color="text.secondary" display="block">
                        {formatDate(loan.applied_at)}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <Typography variant="body2" fontWeight={600}>
                        {loan.customer_name}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        {loan.customer_email}
                      </Typography>
                    </TableCell>
                    <TableCell>{loan.loan_type_display}</TableCell>
                    <TableCell align="right">{formatCurrency(loan.amount)}</TableCell>
                    <TableCell align="right">{loan.interest_rate}%</TableCell>
                    <TableCell align="right">{loan.tenure_months} mo</TableCell>
                    <TableCell align="right">{formatCurrency(loan.emi)}</TableCell>
                    <TableCell align="right">{formatCurrency(loan.remaining_amount)}</TableCell>
                    <TableCell>
                      <StatusChip status={loan.status} />
                    </TableCell>
                    <TableCell align="right">
                      <Stack direction="row" spacing={0.5} justifyContent="flex-end">
                        <Button
                          size="small"
                          color="success"
                          disabled={updatingId === loan.id || loan.status === "APPROVED"}
                          startIcon={<CheckCircleOutlineIcon fontSize="small" />}
                          onClick={() => changeStatus(loan, "APPROVED")}
                        >
                          Approve
                        </Button>
                        <Button
                          size="small"
                          color="primary"
                          disabled={updatingId === loan.id || loan.status === "ACTIVE"}
                          startIcon={<PlayCircleOutlineIcon fontSize="small" />}
                          onClick={() => changeStatus(loan, "ACTIVE")}
                        >
                          Activate
                        </Button>
                        <Button
                          size="small"
                          color="error"
                          disabled={updatingId === loan.id || loan.status === "REJECTED"}
                          startIcon={<HighlightOffIcon fontSize="small" />}
                          onClick={() => changeStatus(loan, "REJECTED")}
                        >
                          Reject
                        </Button>
                      </Stack>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </Paper>

      <Stack direction="row" spacing={1} sx={{ mt: 2, flexWrap: "wrap", gap: 1 }}>
        <Chip label="Approve / reject creates a customer notification" variant="outlined" />
        <Chip label="All loan decisions are simulated" variant="outlined" />
      </Stack>

      <Snackbar
        open={Boolean(snack)}
        autoHideDuration={4000}
        onClose={() => setSnack("")}
        message={snack}
      />
    </Box>
  );
}
```

### frontend/src/pages/admin/AdminAnalytics.jsx

```jsx
import { useCallback, useEffect, useState } from "react";
import { Box, Chip, Grid, Stack, Typography } from "@mui/material";
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Pie,
  PieChart,
  RadialBar,
  RadialBarChart,
  ResponsiveContainer,
  Tooltip as ChartTooltip,
  XAxis,
  YAxis,
} from "recharts";

import { ErrorAlert, Loader, PageHeader, SectionCard } from "../../components/Common.jsx";
import adminService from "../../services/adminService";
import { getErrorMessage } from "../../services/api";
import { CATEGORY_COLORS, formatCurrency } from "../../utils/formatCurrency.js";

export default function AdminAnalytics() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      setData(await adminService.analytics());
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  if (loading) return <Loader label="Crunching demo analytics..." minHeight="60vh" />;
  if (error) {
    return (
      <>
        <PageHeader title="Analytics" />
        <ErrorAlert message={error} onRetry={load} />
      </>
    );
  }

  const { totals, monthly_trend: trend, category_breakdown: categories } = data;
  const radialData = [
    {
      name: "Loans",
      value: totals.loans ? Math.round((totals.active_loans / totals.loans) * 100) : 0,
      fill: "#4361ee",
    },
  ];

  return (
    <Box>
      <PageHeader
        title="Analytics Dashboard"
        subtitle="Aggregated charts for the fictional BankFlow demo portfolio."
        action={<Chip label="Demo data" color="primary" variant="outlined" />}
      />

      <Grid container spacing={2.5}>
        <Grid item xs={12}>
          <SectionCard title="Monthly income vs expense trend" subtitle="Last 6 months, all customers">
            <Box sx={{ height: 320 }}>
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={trend}>
                  <defs>
                    <linearGradient id="aIncome" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#16a34a" stopOpacity={0.35} />
                      <stop offset="95%" stopColor="#16a34a" stopOpacity={0} />
                    </linearGradient>
                    <linearGradient id="aExpense" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#e11d48" stopOpacity={0.35} />
                      <stop offset="95%" stopColor="#e11d48" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#eef1f8" />
                  <XAxis dataKey="month" tick={{ fontSize: 12 }} />
                  <YAxis tick={{ fontSize: 12 }} tickFormatter={(v) => `${v / 1000}k`} />
                  <ChartTooltip formatter={(value) => formatCurrency(value)} />
                  <Legend />
                  <Area
                    type="monotone"
                    dataKey="income"
                    name="Income"
                    stroke="#16a34a"
                    fill="url(#aIncome)"
                    strokeWidth={2}
                  />
                  <Area
                    type="monotone"
                    dataKey="expense"
                    name="Expense"
                    stroke="#e11d48"
                    fill="url(#aExpense)"
                    strokeWidth={2}
                  />
                </AreaChart>
              </ResponsiveContainer>
            </Box>
          </SectionCard>
        </Grid>

        <Grid item xs={12} lg={6}>
          <SectionCard title="Expense by category" subtitle="Portfolio-wide debit split">
            <Box sx={{ height: 300 }}>
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={categories}
                    dataKey="amount"
                    nameKey="category"
                    outerRadius={100}
                    label={(entry) => entry.category}
                  >
                    {categories.map((entry) => (
                      <Cell key={entry.category} fill={entry.color || CATEGORY_COLORS[entry.category]} />
                    ))}
                  </Pie>
                  <ChartTooltip formatter={(value) => formatCurrency(value)} />
                </PieChart>
              </ResponsiveContainer>
            </Box>
          </SectionCard>
        </Grid>

        <Grid item xs={12} lg={6}>
          <SectionCard title="Transaction count per month" subtitle="Activity volume">
            <Box sx={{ height: 300 }}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={trend}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#eef1f8" />
                  <XAxis dataKey="short_month" tick={{ fontSize: 12 }} />
                  <YAxis tick={{ fontSize: 12 }} allowDecimals={false} />
                  <ChartTooltip />
                  <Bar
                    dataKey="transactions"
                    name="Transactions"
                    fill="#0ea5e9"
                    radius={[6, 6, 0, 0]}
                    maxBarSize={42}
                  />
                </BarChart>
              </ResponsiveContainer>
            </Box>
          </SectionCard>
        </Grid>

        <Grid item xs={12} md={5}>
          <SectionCard title="Active loan ratio" subtitle="Share of loans currently running">
            <Box sx={{ height: 260 }}>
              <ResponsiveContainer width="100%" height="100%">
                <RadialBarChart
                  data={radialData}
                  innerRadius="62%"
                  outerRadius="100%"
                  startAngle={90}
                  endAngle={-270}
                >
                  <RadialBar dataKey="value" background cornerRadius={12} />
                </RadialBarChart>
              </ResponsiveContainer>
            </Box>
            <Stack alignItems="center" spacing={0.5}>
              <Typography variant="h4">{radialData[0].value}%</Typography>
              <Typography variant="caption" color="text.secondary">
                {totals.active_loans} of {totals.loans} demo loans are active
              </Typography>
            </Stack>
          </SectionCard>
        </Grid>

        <Grid item xs={12} md={7}>
          <SectionCard title="Portfolio summary" subtitle="Key demo numbers">
            <Grid container spacing={2}>
              {[
                ["Total customers", totals.customers],
                ["Total accounts", totals.accounts],
                ["Total transactions", totals.transactions],
                ["Total loans", totals.loans],
                ["Pending loans", totals.pending_loans],
                ["Unread notifications", totals.unread_notifications],
                ["Total deposits", formatCurrency(totals.total_deposits)],
                ["Outstanding loans", formatCurrency(totals.outstanding)],
                ["Demo transaction volume", formatCurrency(totals.demo_volume)],
              ].map(([label, value]) => (
                <Grid item xs={12} sm={6} md={4} key={label}>
                  <Box sx={{ p: 2, borderRadius: 2, backgroundColor: "#f8f9fd" }}>
                    <Typography variant="caption" color="text.secondary">
                      {label}
                    </Typography>
                    <Typography variant="h6">{value}</Typography>
                  </Box>
                </Grid>
              ))}
            </Grid>
          </SectionCard>
        </Grid>
      </Grid>
    </Box>
  );
}
```

### frontend/src/pages/admin/AIMonitor.jsx

```jsx
import { useCallback, useEffect, useState } from "react";
import {
  Box,
  Chip,
  Grid,
  InputAdornment,
  Paper,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import SmartToyIcon from "@mui/icons-material/SmartToy";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip as ChartTooltip, XAxis, YAxis } from "recharts";

import { EmptyState, ErrorAlert, Loader, PageHeader, SectionCard } from "../../components/Common.jsx";
import adminService from "../../services/adminService";
import { getErrorMessage } from "../../services/api";
import { relativeTime } from "../../utils/formatCurrency.js";

export default function AIMonitor() {
  const [data, setData] = useState(null);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = useCallback(async (term = "") => {
    setLoading(true);
    setError("");
    try {
      setData(await adminService.aiMonitor(term ? { search: term } : {}));
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  return (
    <Box>
      <PageHeader
        title="AI Assistant Monitoring"
        subtitle="What customers are asking BankFlow AI and how the intent engine answered."
      />

      <ErrorAlert message={error} onRetry={() => load(search)} />

      {loading ? (
        <Loader label="Loading assistant activity..." minHeight="50vh" />
      ) : (
        <>
          <Grid container spacing={2.5} sx={{ mb: 2.5 }}>
            <Grid item xs={12} sm={4}>
              <SectionCard title="Total messages">
                <Typography variant="h4">{data.total_messages}</Typography>
                <Typography variant="caption" color="text.secondary">
                  Saved demo conversations
                </Typography>
              </SectionCard>
            </Grid>
            <Grid item xs={12} sm={4}>
              <SectionCard title="Rule based answers">
                <Typography variant="h4">{data.providers.fallback}</Typography>
                <Typography variant="caption" color="text.secondary">
                  Works with no external API key
                </Typography>
              </SectionCard>
            </Grid>
            <Grid item xs={12} sm={4}>
              <SectionCard title="LLM answers">
                <Typography variant="h4">{data.providers.openai}</Typography>
                <Typography variant="caption" color="text.secondary">
                  Used when AI_PROVIDER=openai
                </Typography>
              </SectionCard>
            </Grid>

            {data.intent_breakdown.length > 0 && (
              <Grid item xs={12}>
                <SectionCard title="Intent breakdown" subtitle="Detected intent per question">
                  <Box sx={{ height: 260 }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={data.intent_breakdown}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#eef1f8" />
                        <XAxis
                          dataKey="type"
                          tick={{ fontSize: 11 }}
                          interval={0}
                          angle={-20}
                          dy={10}
                          height={60}
                        />
                        <YAxis tick={{ fontSize: 12 }} allowDecimals={false} />
                        <ChartTooltip />
                        <Bar dataKey="count" name="Questions" fill="#4361ee" radius={[6, 6, 0, 0]} maxBarSize={40} />
                      </BarChart>
                    </ResponsiveContainer>
                  </Box>
                </SectionCard>
              </Grid>
            )}
          </Grid>

          <Paper variant="outlined" sx={{ p: 2.5, borderRadius: 3 }}>
            <Stack direction={{ xs: "column", sm: "row" }} spacing={2} sx={{ mb: 2 }}>
              <TextField
                size="small"
                placeholder="Search question or customer"
                value={search}
                onChange={(event) => setSearch(event.target.value)}
                onKeyDown={(event) => event.key === "Enter" && load(search)}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <SearchIcon fontSize="small" />
                    </InputAdornment>
                  ),
                }}
                sx={{ flexGrow: 1 }}
              />
              <Box
                component="button"
                onClick={() => load(search)}
                sx={{
                  px: 2,
                  py: 1,
                  borderRadius: 2,
                  border: "none",
                  backgroundColor: "primary.main",
                  color: "#fff",
                  cursor: "pointer",
                  fontWeight: 600,
                }}
              >
                Search
              </Box>
            </Stack>

            {data.results.length === 0 ? (
              <EmptyState
                title="No assistant activity yet"
                description="Ask something in the AI Assistant page and it will appear here."
              />
            ) : (
              <TableContainer>
                <Table size="small" sx={{ minWidth: 900 }}>
                  <TableHead>
                    <TableRow>
                      <TableCell>Customer</TableCell>
                      <TableCell>Question</TableCell>
                      <TableCell>Answer preview</TableCell>
                      <TableCell>Intent</TableCell>
                      <TableCell>Provider</TableCell>
                      <TableCell>When</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {data.results.map((row) => (
                      <TableRow key={row.id} hover>
                        <TableCell>
                          <Stack direction="row" spacing={1} alignItems="center">
                            <SmartToyIcon fontSize="small" color="primary" />
                            <Box>
                              <Typography variant="body2" fontWeight={600}>
                                {row.customer}
                              </Typography>
                              <Typography variant="caption" color="text.secondary">
                                {row.email}
                              </Typography>
                            </Box>
                          </Stack>
                        </TableCell>
                        <TableCell sx={{ maxWidth: 240 }}>{row.message}</TableCell>
                        <TableCell sx={{ maxWidth: 320 }}>
                          <Typography variant="body2" color="text.secondary">
                            {row.response.length > 140 ? `${row.response.slice(0, 140)}...` : row.response}
                          </Typography>
                        </TableCell>
                        <TableCell>
                          <Chip size="small" variant="outlined" label={row.type.replace(/_/g, " ")} />
                        </TableCell>
                        <TableCell>
                          <Chip
                            size="small"
                            color={row.provider === "openai" ? "info" : "default"}
                            label={row.provider}
                          />
                        </TableCell>
                        <TableCell>{relativeTime(row.created_at)}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            )}
          </Paper>
        </>
      )}
    </Box>
  );
}
```

---

## 10. PROJECT README (full documentation)

````markdown
# BankFlow – AI Banking Assistant

A complete, runnable **full-stack demo banking application**: React + Vite + Material UI on the
front end, Django + Django REST Framework + JWT on the back end, Recharts for analytics and a
modular AI banking assistant service.

> **This is a demonstration project.** Every customer, account, transaction, loan and notification
> is fictional. The app never moves real money, never contacts a real bank and must never be used
> with real credentials or financial data.

---

## 1. Project overview

BankFlow lets a customer register, log in, see a banking dashboard, explore transactions, apply for
demo loans, calculate EMIs, read notifications and chat with an AI assistant that answers questions
using **their own simulated banking data**. A second role - bank employee / admin - can manage
customers, transactions, loans, view analytics and monitor what customers ask the AI.

Everything works offline: if no external AI key is configured, a rule based intent engine answers
the questions instead.

---

## 2. Features

**Customer**

- Register, login, logout with JWT (access + refresh, automatic refresh on 401)
- Protected routes and role based access (customer vs bank employee)
- Dashboard: available balance, monthly income, monthly expenses, active loans
- Charts: income vs expense (6 months), spending by category, monthly transaction count, loan status
- Account page with masked account number, type, status, IFSC-style demo identifier
- Transactions: search, category filter, credit/debit filter, date range filter, sorting, pagination,
  running balance and a transaction details page
- Loans: list, status tabs, demo application form with live EMI preview, loan details with a
  12-instalment amortisation schedule and repayment progress
- EMI calculator: sliders + inputs, EMI, total interest, total repayment, principal vs interest chart,
  server-side verification through the Django API
- AI Banking Assistant: chat UI, chat history sidebar, suggested questions, intent-aware answers
- Notifications with read / unread state and "mark all as read"
- Profile: view and update name, phone, address, occupation, monthly income

**Bank employee / admin**

- Admin dashboard: customers, accounts, transactions, loans, pending loans, demo transaction volume
- Customer management with search and a customer 360 dialog (accounts, profile, loans)
- Transaction management across every customer with filters and pagination
- Loan management: approve / activate / reject a demo loan (creates a customer notification)
- Analytics dashboard: portfolio trend, category split, transaction count, active loan ratio
- AI assistant monitoring: total questions, intent breakdown, provider split, full question log

---

## 3. Technology stack

| Layer | Technology |
| --- | --- |
| Frontend | React 18, Vite 5, React Router 6, Material UI 5, Recharts, Axios, React Icons |
| Backend | Python, Django 5, Django REST Framework, SimpleJWT, django-cors-headers, python-dotenv |
| Database | SQLite (default, zero setup) or PostgreSQL (switch with `DB_ENGINE=postgres`) |
| AI | Modular service (`assistant/ai_service.py`) with rule based fallback and an optional LLM hook |
| Auth | JWT access/refresh tokens, `Authorization: Bearer <access>` |

---

## 4. Architecture

```
React (Vite, port 5173)
  └── axios api.js  ── JWT header + auto refresh
        │
        ▼
Django REST Framework (port 8000)
  ├── users/       custom User (email login, roles) + CustomerProfile
  ├── banking/     Account → Transaction, Loan, Notification + dashboard/analytics services
  └── assistant/   ChatMessage + ai_service (intent detection → data retrieval → answer)
        │
        ▼
SQLite / PostgreSQL (fictional demo data)
```

Request flow of an AI question:

1. React posts `{ "message": "How much did I spend this month?" }` to `/api/assistant/chat/`.
2. `ai_service.detect_intent()` maps the sentence to an intent (`expense_summary`).
3. `build_context(user)` retrieves the structured demo banking snapshot from the database.
4. Either the LLM layer (if `AI_PROVIDER=openai` and a key exists) or the rule based engine writes
   the answer from that snapshot - numbers are never invented.
5. The question and answer are stored in `ChatMessage` and returned to React with
   `{ response, type, data, provider }`.

---

## 5. Folder structure

```
banking_app/
├── README.md
├── FULL_CODE.md               # every source file, headline-wise, copy-paste ready
│
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── config/                settings.py, urls.py, wsgi.py, asgi.py
│   ├── users/                 models, serializers, views, permissions, signals, urls/
│   ├── banking/               models, serializers, views, admin_views, services,
│   │                          urls/, management/commands/seed_demo.py
│   └── assistant/             models, serializers, views, ai_service, urls
│
└── frontend/
    ├── index.html, package.json, vite.config.js, .env.example
    └── src/
        ├── main.jsx, App.jsx, theme.js, index.css
        ├── components/        AppLayout, Navbar, Sidebar, DashboardCard, TransactionTable,
        │                      LoanCard, ChatMessage, ProtectedRoute, Common
        ├── context/           AuthContext.jsx
        ├── services/          api.js, authService.js, bankingService.js, aiService.js, adminService.js
        ├── utils/             formatCurrency.js, calculations.js
        └── pages/             Landing, Login, Register, Dashboard, Account, Transactions,
                               TransactionDetails, Loans, LoanDetails, EMICalculator,
                               AIAssistant, Notifications, Profile, NotFound
            └── admin/         AdminDashboard, CustomerManagement, TransactionManagement,
                               LoanManagement, AdminAnalytics, AIMonitor
```

---

## 6. Backend setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate            # Windows
# source venv/bin/activate       # macOS / Linux
pip install -r requirements.txt
copy .env.example .env           # Windows   (cp on macOS / Linux)
python manage.py makemigrations users banking assistant
python manage.py migrate
python manage.py seed_demo --flush
python manage.py runserver 127.0.0.1:8000
```

API root: <http://127.0.0.1:8000/api/> · Django admin: <http://127.0.0.1:8000/admin/>

Run the tests (25 tests: auth, profile, banking, EMI, admin permissions, AI intents):

```bash
python manage.py test
```

---

## 7. Frontend setup

```bash
cd frontend
npm install
copy .env.example .env           # cp on macOS / Linux
npm run dev                      # http://localhost:5173
npm run build                    # production bundle in dist/
npm run preview                  # serve the production build
```

`frontend/.env`

```
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

---

## 8. Database setup

**SQLite (default, recommended for the demo)** - nothing to install, the file `backend/db.sqlite3`
is created by `migrate`.

**PostgreSQL (optional)** - create the database, then in `backend/.env`:

```
DB_ENGINE=postgres
POSTGRES_DB=bankflow
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

Re-run `python manage.py migrate` and `python manage.py seed_demo --flush`.

---

## 9. Environment variables

`backend/.env`

| Variable | Purpose |
| --- | --- |
| `DJANGO_SECRET_KEY` | Django secret key (change in production) |
| `DJANGO_DEBUG` | `True` locally, `False` in production |
| `DJANGO_ALLOWED_HOSTS` | Comma separated host names |
| `CORS_ALLOWED_ORIGINS` | Allowed front-end origins (default `http://localhost:5173`) |
| `DB_ENGINE` | `sqlite` or `postgres` |
| `POSTGRES_*` | PostgreSQL connection details |
| `AI_PROVIDER` | `fallback` (rule based, default) or `openai` |
| `OPENAI_API_KEY` | Optional key - never hard-code it, never commit `.env` |
| `OPENAI_MODEL` | Model name used when `AI_PROVIDER=openai` |

`frontend/.env`

| Variable | Purpose |
| --- | --- |
| `VITE_API_BASE_URL` | Base URL of the Django API |

---

## 10. API endpoints

All customer endpoints require the header `Authorization: Bearer <access_token>`.

**Authentication**

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/api/auth/register/` | Register a demo customer (creates an account automatically) |
| POST | `/api/auth/login/` | Login, returns `access` + `refresh` |
| POST | `/api/auth/refresh/` | Exchange a refresh token for a new access token |

**Customer**

| Method | Endpoint | Description |
| --- | --- | --- |
| GET / PUT | `/api/profile/` | Read or update the customer profile (name, phone, address, occupation, income) |
| GET | `/api/dashboard/` | KPI cards + charts data in one call |
| GET | `/api/account/` | Masked account details |
| GET | `/api/transactions/` | List with `search`, `category`, `type`, `status`, `start_date`, `end_date`, `ordering`, `page` |
| GET | `/api/transactions/<id>/` | Single transaction detail |
| GET / POST | `/api/loans/` | List loans / submit a demo loan application |
| GET | `/api/loans/<id>/` | Loan detail |
| POST | `/api/emi/` | Server-side EMI calculation |
| GET | `/api/notifications/` | Notifications (`?unread=true` for unread only) |
| PUT | `/api/notifications/<id>/` | Mark read / unread |
| POST | `/api/notifications/read-all/` | Mark every notification as read |
| POST | `/api/assistant/chat/` | Ask BankFlow AI |
| GET / DELETE | `/api/assistant/history/` | Read or clear the saved chat history |
| GET | `/api/assistant/suggestions/` | Suggested question chips |

**Bank employee / admin (role `ADMIN` required)**

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api/admin/analytics/` | KPI totals + all admin charts |
| GET | `/api/admin/analytics/overview/` | The six KPI numbers only |
| GET | `/api/admin/customers/` | Customer table (`?search=`) |
| GET | `/api/admin/customers/<id>/` | Customer 360 view |
| GET | `/api/admin/transactions/` | All transactions with filters |
| GET | `/api/admin/loans/` | All loans with filters |
| PATCH | `/api/admin/loans/<id>/` | `{ "status": "APPROVED" }` etc. (notifies the customer) |
| GET | `/api/admin/users/` | User management table |
| GET | `/api/assistant/monitor/` | AI monitoring dashboard data |

**AI request / response example**

```json
POST /api/assistant/chat/
{ "message": "How much did I spend this month?" }

{
  "id": 12,
  "message": "How much did I spend this month?",
  "response": "You spent ₹18,450 this month. Your income for the month is ₹45,000, so your net savings are ₹26,550.",
  "type": "expense_summary",
  "intent": "expense_summary",
  "provider": "fallback",
  "data": { "amount": 18450.0, "income": 45000.0, "savings": 26550.0 }
}
```

---

## 11. How to run

Terminal 1

```bash
cd backend
venv\Scripts\activate
python manage.py runserver 127.0.0.1:8000
```

Terminal 2

```bash
cd frontend
npm run dev
```

Open <http://localhost:5173>.

### Demo logins

| Role | Email | Password |
| --- | --- | --- |
| Customer (Mohammed Adnan, balance ₹85,450) | `mohammed@bankflow.com` | `Demo@12345` |
| Customer (Aisha Khan) | `aisha@bankflow.com` | `Demo@12345` |
| Customer (Rahul Verma) | `rahul@bankflow.com` | `Demo@12345` |
| Bank employee / admin | `admin@bankflow.com` | `Admin@12345` |

### 5-10 minute demo flow

1. Landing page - hero, features, AI preview, security, demo logins.
2. Login as `mohammed@bankflow.com`.
3. Dashboard - balance ₹85,450, income ₹45,000, expenses ₹18,450, 2 active loans, four charts.
4. Account page - masked account number and account status.
5. Transactions - filter by category, type, date; open a transaction detail.
6. Loans - status tabs, apply for a new demo loan (live EMI preview).
7. EMI calculator - move the sliders, see the Django API verification message.
8. AI Assistant - ask: *What is my balance?*, *How much did I spend this month?*,
   *What was my biggest expense?*, *What loans do I have?*, *What is EMI?* - and show the history panel.
9. Analytics + notifications.
10. Log out, log in as `admin@bankflow.com` - admin dashboard, customer 360, approve a pending loan,
    analytics and AI monitoring.
11. Explain the flow: React → axios/JWT → DRF views → services → ORM → SQLite → AI service.

---

## 12. Future improvements

- Real LLM integration with streaming responses and function/tool calling
- Budgets, goals and spend alerts; recurring transaction detection
- Statement export (CSV/PDF) and downloadable receipts
- Refresh-token blacklisting, 2FA and device management
- Celery + Redis for background jobs (EMI reminders, monthly summaries)
- WebSocket notifications instead of polling
- Docker Compose for one-command startup, plus CI with GitHub Actions
- End-to-end tests with Playwright and API schema docs with drf-spectacular
````

## 11. GENERATED FILES (do not copy by hand)

These are produced automatically by the commands in section 0:

- `backend/db.sqlite3` - created by `python manage.py migrate`
- `backend/*/migrations/0001_initial.py` etc. - created by `python manage.py makemigrations`
- `frontend/node_modules/`, `frontend/package-lock.json` - created by `npm install`
- `frontend/dist/` - created by `npm run build`

- `backend/.env` and `frontend/.env` - copy them from the `.env.example` files in sections 1 and 5

