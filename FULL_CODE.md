# BANKFLOW - AI BANKING ASSISTANT

Complete source code of the project, headline-wise, in the order you create the files.
Generated from 106 tracked files by tools/generate_full_code.py.

> Demo application only. All banking data is fictional and no real money movement happens.

---

## Install and run

```bash
git clone https://github.com/Adnan8066/bankflow-ai-banking-assistant.git
cd bankflow-ai-banking-assistant

# backend
cd backend
python -m venv venv
venv\Scripts\activate            # source venv/bin/activate on macOS or Linux
pip install -r requirements.txt
copy .env.example .env           # cp on macOS or Linux
python manage.py migrate
python manage.py seed_demo --flush
python manage.py runserver 127.0.0.1:8000

# frontend, in a second terminal
cd frontend
npm install
copy .env.example .env           # cp on macOS or Linux
npm run dev
```

---

## Project files

### README.md

````markdown
# BankFlow – AI Banking Assistant

A complete, runnable **full-stack demo banking application**: React + Vite + Material UI on the
front end, Django + Django REST Framework + JWT on the back end, Recharts for analytics and a
modular AI banking assistant service.

> **This is a demonstration project.** Every customer, account, transaction, loan and notification
> is fictional. The app never moves real money, never contacts a real bank and must never be used
> with real credentials or financial data.

[![CI](https://github.com/Adnan8066/bankflow-ai-banking-assistant/actions/workflows/ci.yml/badge.svg)](https://github.com/Adnan8066/bankflow-ai-banking-assistant/actions/workflows/ci.yml)

A one page summary of the project, its features and the decisions behind it is in
[PROJECT_BRIEF.md](PROJECT_BRIEF.md).

---

## Get the code on your computer

```bash
git clone https://github.com/Adnan8066/bankflow-ai-banking-assistant.git
cd bankflow-ai-banking-assistant
```

Then follow [Backend setup](#6-backend-setup) and [Frontend setup](#7-frontend-setup), or read the
step by step walkthroughs in `FULL_CODE.md`.

The repository is public. Change that any time in the repository **Settings**, under **General**,
**Danger zone**, **Change repository visibility**.

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
- Dashboard: available balance, monthly income, monthly expenses, savings rate, active loans
- Charts: income vs expense (6 months), spending by category, transaction count, loan status, daily spending
- Account page with masked account number, type, status, IFSC-style demo identifier
- Transactions: search, category filter, credit/debit filter, date range filter, sorting, pagination,
  running balance, CSV export and a transaction details page
- Loans: list, status tabs, demo application form with live EMI preview, loan details with a
  12-instalment amortisation schedule and repayment progress
- EMI calculator: sliders + inputs, EMI, total interest, total repayment, principal vs interest chart,
  server-side verification through the Django API
- AI Banking Assistant: chat UI, chat history sidebar, suggested questions, intent-aware answers
- Notifications with read / unread state and "mark all as read"
- Profile: view and update name, phone, address, occupation, monthly income, and change the password
- Light and dark mode, remembered between visits

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
├── PROJECT_BRIEF.md           # one page summary for a portfolio or a team
├── .github/workflows/ci.yml   # runs the Django tests and the frontend build
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
| POST | `/api/auth/change-password/` | Change the password after confirming the current one |

**Customer**

| Method | Endpoint | Description |
| --- | --- | --- |
| GET / PUT | `/api/profile/` | Read or update the customer profile (name, phone, address, occupation, income) |
| GET | `/api/dashboard/` | KPI cards + charts data in one call |
| GET | `/api/account/` | Masked account details |
| GET | `/api/transactions/` | List with `search`, `category`, `type`, `status`, `start_date`, `end_date`, `ordering`, `page` |
| GET | `/api/transactions/<id>/` | Single transaction detail |
| GET | `/api/transactions/export/` | Download the filtered transactions as a CSV file |
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

## Backend (Django REST Framework)

### backend/requirements.txt

```text
Django==5.2.6
djangorestframework==3.16.1
djangorestframework-simplejwt==5.5.1
django-cors-headers==4.9.0
python-dotenv==1.1.1
psycopg[binary]==3.2.10
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


class ChangePasswordSerializer(serializers.Serializer):
    """POST /api/auth/change-password/ - the customer proves the old password first."""

    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    def validate_current_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Your current password is not correct.")
        return value

    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "The two new passwords do not match."}
            )
        if attrs["new_password"] == attrs["current_password"]:
            raise serializers.ValidationError(
                {"new_password": "Choose a password different from the current one."}
            )
        return attrs

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save(update_fields=["password"])
        return user
```

### backend/users/views.py

```python
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

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
```

### backend/users/urls/auth_urls.py

```python
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import ChangePasswordView, RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
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


class ChangePasswordTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="password@bankflow.com", password="Demo@12345", name="Password User"
        )
        self.client.force_authenticate(self.user)

    def test_change_password_success(self):
        response = self.client.post("/api/auth/change-password/", {
            "current_password": "Demo@12345",
            "new_password": "NewDemo@2026",
            "confirm_password": "NewDemo@2026",
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("NewDemo@2026"))

    def test_change_password_rejects_wrong_current_password(self):
        response = self.client.post("/api/auth/change-password/", {
            "current_password": "WrongPassword1",
            "new_password": "NewDemo@2026",
            "confirm_password": "NewDemo@2026",
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("Demo@12345"))

    def test_change_password_rejects_mismatch_and_weak_password(self):
        mismatch = self.client.post("/api/auth/change-password/", {
            "current_password": "Demo@12345",
            "new_password": "NewDemo@2026",
            "confirm_password": "Different@2026",
        })
        self.assertEqual(mismatch.status_code, status.HTTP_400_BAD_REQUEST)

        weak = self.client.post("/api/auth/change-password/", {
            "current_password": "Demo@12345",
            "new_password": "123",
            "confirm_password": "123",
        })
        self.assertEqual(weak.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_requires_login(self):
        self.client.force_authenticate(None)
        response = self.client.post("/api/auth/change-password/", {
            "current_password": "Demo@12345",
            "new_password": "NewDemo@2026",
            "confirm_password": "NewDemo@2026",
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
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
        "savings_rate": savings_rate(current["income"], current["expense"]),
        "daily_spending": daily_spending(user, 14),
        "average_daily_spend": round(
            sum(item["amount"] for item in daily_spending(user, 14)) / 14, 2
        ),
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


def savings_rate(income, expense):
    """Share of this month's income that was not spent, as a percentage."""
    income = float(income or 0)
    expense = float(expense or 0)
    if income <= 0:
        return 0.0
    return round((income - expense) / income * 100, 1)


def daily_spending(user, days=14):
    """Debit totals for the last `days` days, with quiet days filled in as zero."""
    today = timezone.localdate()
    start = today - timedelta(days=days - 1)
    qs = customer_transactions(user).filter(
        transaction_type=Transaction.Type.DEBIT,
        status=Transaction.Status.COMPLETED,
        date__gte=aware(start),
    )
    totals = {}
    for txn in qs:
        key = timezone.localtime(txn.date).date().isoformat()
        totals[key] = totals.get(key, 0) + to_float(txn.amount)

    series = []
    for offset in range(days):
        day = start + timedelta(days=offset)
        series.append({
            "date": day.isoformat(),
            "label": day.strftime("%d %b"),
            "weekday": day.strftime("%a"),
            "amount": round(totals.get(day.isoformat(), 0), 2),
        })
    return series


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
    """A safe date inside a month (never in the future, never past month end).

    A negative `day` counts backwards from today, which keeps the newest demo
    transactions recent enough for the daily spending chart to look alive.
    """
    start = month_start_offset(month_offset)
    next_month = (start + timedelta(days=32)).replace(day=1)
    last_day = (next_month - timedelta(days=1)).day

    if month_offset == 0 and day < 0:
        target = timezone.localdate() + timedelta(days=day)
        if target < start:
            target = start
        return timezone.make_aware(
            datetime.combine(target, datetime.min.time())
        ) + timedelta(hours=hour, minutes=minute)

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
    (0, -1, 2450, "Amazon - electronics order", "Shopping", "DEBIT"),
    (0, -2, 1200, "Zomato - dinner order", "Food", "DEBIT"),
    (0, -3, 1500, "Electricity bill - BESCOM", "Bills", "DEBIT"),
    (0, -4, 2000, "IRCTC train tickets", "Travel", "DEBIT"),
    (0, -5, 800, "PVR Cinemas - movie tickets", "Entertainment", "DEBIT"),
    (0, -6, 4750, "Croma - new laptop accessories", "Shopping", "DEBIT"),
    (0, -8, 950, "Swiggy - lunch order", "Food", "DEBIT"),
    (0, -9, 1800, "UPI transfer to friend", "Transfer", "DEBIT"),
    (0, -11, 3000, "Insurance premium - demo policy", "Other", "DEBIT"),
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
import csv

from django.http import HttpResponse
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


def filter_transactions(queryset, params):
    """Apply the transaction filters in one place so the list and the CSV export agree."""
    search = params.get("search")
    if search:
        queryset = queryset.filter(
            Q(description__icontains=search)
            | Q(transaction_id__icontains=search)
            | Q(category__icontains=search)
        )
    if params.get("category") and params["category"] != "ALL":
        queryset = queryset.filter(category=params["category"])
    if params.get("type") and params["type"] != "ALL":
        queryset = queryset.filter(transaction_type=params["type"].upper())
    if params.get("status") and params["status"] != "ALL":
        queryset = queryset.filter(status=params["status"].upper())

    start = parse_date(params.get("start_date") or "")
    end = parse_date(params.get("end_date") or "")
    if start:
        queryset = queryset.filter(date__date__gte=start)
    if end:
        queryset = queryset.filter(date__date__lte=end)

    ordering = params.get("ordering") or "-date"
    allowed = {"date", "-date", "amount", "-amount", "category", "-category"}
    return queryset.order_by(ordering if ordering in allowed else "-date")


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
        return filter_transactions(
            customer_transactions(self.request.user).select_related("account"),
            self.request.query_params,
        )

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


class TransactionExportView(APIView):
    """GET /api/transactions/export/ - the filtered transactions as a CSV download."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = filter_transactions(
            customer_transactions(request.user).select_related("account"),
            request.query_params,
        )
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="bankflow-transactions.csv"'
        writer = csv.writer(response)
        writer.writerow([
            "Transaction ID", "Date", "Description", "Category", "Type",
            "Amount", "Status", "Balance after",
        ])
        for txn in queryset:
            writer.writerow([
                txn.transaction_id,
                txn.date.strftime("%Y-%m-%d %H:%M"),
                txn.description,
                txn.category,
                txn.transaction_type,
                f"{float(txn.amount):.2f}",
                txn.status,
                f"{float(txn.balance_after):.2f}",
            ])
        return response


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
    TransactionExportView,
    TransactionListView,
)

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("account/", AccountView.as_view(), name="account"),
    path("transactions/", TransactionListView.as_view(), name="transaction-list"),
    path("transactions/export/", TransactionExportView.as_view(), name="transaction-export"),
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

    def test_dashboard_insights(self):
        response = self.client.get("/api/dashboard/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["daily_spending"]), 14)
        self.assertAlmostEqual(response.data["savings_rate"], 81.3, places=1)
        self.assertGreater(response.data["average_daily_spend"], 0)
        self.assertEqual(set(response.data["daily_spending"][0]),
                         {"date", "label", "weekday", "amount"})

    def test_transactions_csv_export(self):
        response = self.client.get("/api/transactions/export/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("text/csv", response["Content-Type"])
        self.assertIn("attachment", response["Content-Disposition"])
        body = response.content.decode()
        header = body.splitlines()[0]
        self.assertIn("Transaction ID", header)
        self.assertIn("Balance after", header)
        self.assertEqual(len(body.strip().splitlines()), 4)  # header + 3 transactions

    def test_transactions_csv_export_respects_filters(self):
        response = self.client.get("/api/transactions/export/", {"category": "Food"})
        body = response.content.decode().strip().splitlines()
        self.assertEqual(len(body), 2)  # header + one food transaction
        self.assertIn("Zomato", body[1])


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

### backend/assistant/migrations/0001_initial.py

```python
# Generated by Django 5.2.6 on 2026-09-21 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('response', models.TextField()),
                ('response_type', models.CharField(default='general', max_length=40)),
                ('provider', models.CharField(default='fallback', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
    ]
```

### backend/assistant/migrations/0002_initial.py

```python
# Generated by Django 5.2.6 on 2026-09-21 17:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('assistant', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_messages', to=settings.AUTH_USER_MODEL),
        ),
    ]
```

### backend/assistant/migrations/__init__.py

```python

```

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

### backend/banking/management/__init__.py

```python

```

### backend/banking/management/commands/__init__.py

```python

```

### backend/banking/migrations/0001_initial.py

```python
# Generated by Django 5.2.6 on 2026-09-21 17:24

import banking.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.CharField(max_length=20, unique=True)),
                ('account_type', models.CharField(choices=[('SAVINGS', 'Savings Account'), ('CURRENT', 'Current Account'), ('SALARY', 'Salary Account')], default='SAVINGS', max_length=20)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('DORMANT', 'Dormant'), ('CLOSED', 'Closed')], default='ACTIVE', max_length=20)),
                ('ifsc_code', models.CharField(default='BANKFL0001234', max_length=20)),
                ('branch', models.CharField(default='BankFlow Demo Branch', max_length=120)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_id', models.CharField(default=banking.models.default_loan_id, max_length=30, unique=True)),
                ('loan_type', models.CharField(choices=[('PERSONAL', 'Personal Loan'), ('HOME', 'Home Loan'), ('EDUCATION', 'Education Loan'), ('VEHICLE', 'Vehicle Loan')], max_length=20)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=14)),
                ('interest_rate', models.DecimalField(decimal_places=2, default=9.5, max_digits=5)),
                ('tenure_months', models.PositiveIntegerField(default=12)),
                ('emi', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('remaining_amount', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected'), ('ACTIVE', 'Active'), ('COMPLETED', 'Completed')], default='PENDING', max_length=12)),
                ('purpose', models.CharField(blank=True, max_length=255)),
                ('monthly_income', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('employment_type', models.CharField(choices=[('SALARIED', 'Salaried'), ('SELF_EMPLOYED', 'Self Employed'), ('STUDENT', 'Student'), ('RETIRED', 'Retired'), ('OTHER', 'Other')], default='SALARIED', max_length=20)),
                ('applied_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-applied_at'],
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('message', models.TextField()),
                ('notification_type', models.CharField(choices=[('TRANSACTION', 'Transaction'), ('LOAN', 'Loan'), ('SECURITY', 'Security'), ('SUMMARY', 'Summary'), ('SYSTEM', 'System')], default='SYSTEM', max_length=20)),
                ('is_read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(default=banking.models.default_transaction_id, max_length=30, unique=True)),
                ('date', models.DateTimeField()),
                ('description', models.CharField(max_length=200)),
                ('category', models.CharField(choices=[('Salary', 'Salary'), ('Food', 'Food'), ('Shopping', 'Shopping'), ('Travel', 'Travel'), ('Bills', 'Bills'), ('Entertainment', 'Entertainment'), ('Transfer', 'Transfer'), ('Other', 'Other')], default='Other', max_length=20)),
                ('transaction_type', models.CharField(choices=[('CREDIT', 'Credit'), ('DEBIT', 'Debit')], max_length=10)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=14)),
                ('status', models.CharField(choices=[('COMPLETED', 'Completed'), ('PENDING', 'Pending'), ('FAILED', 'Failed')], default='COMPLETED', max_length=12)),
                ('balance_after', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]
```

### backend/banking/migrations/0002_initial.py

```python
# Generated by Django 5.2.6 on 2026-09-21 17:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('banking', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='loan',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loans', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='transaction',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='banking.account'),
        ),
    ]
```

### backend/banking/migrations/__init__.py

```python

```

### backend/banking/urls/__init__.py

```python

```

### backend/config/__init__.py

```python

```

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

### backend/users/migrations/0001_initial.py

```python
# Generated by Django 5.2.6 on 2026-09-21 17:24

import django.db.models.deletion
import django.utils.timezone
import users.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('name', models.CharField(max_length=150)),
                ('role', models.CharField(choices=[('CUSTOMER', 'Customer'), ('ADMIN', 'Bank Employee / Admin')], default='CUSTOMER', max_length=20)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', users.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='CustomerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('address', models.CharField(blank=True, max_length=255)),
                ('occupation', models.CharField(blank=True, max_length=120)),
                ('employment_type', models.CharField(choices=[('SALARIED', 'Salaried'), ('SELF_EMPLOYED', 'Self Employed'), ('STUDENT', 'Student'), ('RETIRED', 'Retired'), ('OTHER', 'Other')], default='SALARIED', max_length=20)),
                ('monthly_income', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
```

### backend/users/migrations/__init__.py

```python

```

### backend/users/urls/__init__.py

```python

```

## Frontend (React and Vite)

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

### frontend/src/index.css

```css
:root {
  color-scheme: light;
  /* Surface tokens used by the components instead of hard coded light colours,
     so one attribute on <html> switches the whole application. */
  --bf-tint: #eef2fd;
  --bf-surface: #f8f9fd;
  --bf-panel: #fbfcff;
  --bf-paper: #ffffff;
  --bf-border: #e6e9f2;
  --bf-glow: #e8eefc;
}

html[data-theme="dark"] {
  color-scheme: dark;
  --bf-tint: #202b47;
  --bf-surface: #1a2237;
  --bf-panel: #141b2c;
  --bf-paper: #161d2f;
  --bf-border: #28324a;
  --bf-glow: #1b2540;
}

html,
body,
#root {
  height: 100%;
  margin: 0;
}

body {
  font-family: "Inter", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
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

html[data-theme="dark"] ::-webkit-scrollbar-thumb {
  background: #344060;
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

### frontend/src/theme.js

```javascript
import { createTheme } from "@mui/material/styles";

/**
 * BankFlow design tokens.
 * One builder serves light and dark mode so every page stays consistent.
 */
const LIGHT = {
  primary: { main: "#1b3a8f", light: "#4361ee", dark: "#122a68", contrastText: "#ffffff" },
  secondary: { main: "#0ea5e9", contrastText: "#ffffff" },
  success: { main: "#16a34a" },
  error: { main: "#e11d48" },
  warning: { main: "#f59e0b" },
  info: { main: "#6366f1" },
  background: { default: "#f4f6fb", paper: "#ffffff" },
  text: { primary: "#111a2e", secondary: "#5a6478" },
  divider: "#e6e9f2",
};

const DARK = {
  primary: { main: "#7b96ff", light: "#a9baff", dark: "#5a76e6", contrastText: "#0b1020" },
  secondary: { main: "#4fc3f7", contrastText: "#0b1020" },
  success: { main: "#4ade80" },
  error: { main: "#fb7185" },
  warning: { main: "#fbbf24" },
  info: { main: "#8b95f8" },
  background: { default: "#0d1220", paper: "#161d2f" },
  text: { primary: "#e9edf9", secondary: "#9fabc4" },
  divider: "#28324a",
};

export function createAppTheme(mode = "light") {
  const palette = mode === "dark" ? DARK : LIGHT;
  const isDark = mode === "dark";

  return createTheme({
    palette: { mode, ...palette },
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
        styleOverrides: { root: { backgroundImage: "none" } },
      },
      MuiCard: {
        defaultProps: { elevation: 0 },
        styleOverrides: {
          root: {
            backgroundImage: "none",
            border: "1px solid",
            borderColor: palette.divider,
            boxShadow: isDark
              ? "none"
              : "0 1px 2px rgba(17, 26, 46, 0.04), 0 8px 24px rgba(17, 26, 46, 0.04)",
          },
        },
      },
      MuiButton: {
        defaultProps: { disableElevation: true },
        styleOverrides: { root: { borderRadius: 10, paddingInline: 18 } },
      },
      MuiChip: { styleOverrides: { root: { fontWeight: 600 } } },
      MuiTableCell: {
        styleOverrides: {
          head: {
            fontWeight: 700,
            color: palette.text.secondary,
            backgroundColor: "var(--bf-surface)",
          },
        },
      },
      MuiAppBar: { defaultProps: { elevation: 0, color: "inherit" } },
    },
  });
}

export default createAppTheme("light");
```

### frontend/src/main.jsx

```jsx
import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";

import App from "./App.jsx";
import { AuthProvider } from "./context/AuthContext.jsx";
import { ColorModeProvider } from "./context/ColorModeContext.jsx";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    {/* ColorModeProvider owns the MUI theme, so light and dark mode work from one place. */}
    <ColorModeProvider>
      {/* The future flags remove the React Router v7 upgrade warnings in the console. */}
      <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
        <AuthProvider>
          <App />
        </AuthProvider>
      </BrowserRouter>
    </ColorModeProvider>
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

  async changePassword(payload) {
    const { data } = await api.post("/auth/change-password/", payload);
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
  // Same filters as the list, but as a CSV file for spreadsheets.
  exportTransactions: (params = {}) =>
    api
      .get("/transactions/export/", { params, responseType: "blob" })
      .then((r) => r.data),

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
import Brightness4Icon from "@mui/icons-material/Brightness4";
import Brightness7Icon from "@mui/icons-material/Brightness7";
import { useLocation, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext.jsx";
import { useColorMode } from "../context/ColorModeContext.jsx";
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
  const { mode, toggleColorMode } = useColorMode();
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
        backgroundColor: "background.paper",
        backdropFilter: "blur(8px)",
        borderBottom: "1px solid",
        borderColor: "divider",
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

        <Tooltip title={mode === "dark" ? "Switch to light mode" : "Switch to dark mode"}>
          <IconButton onClick={toggleColorMode} aria-label="Toggle dark mode">
            {mode === "dark" ? <Brightness7Icon /> : <Brightness4Icon />}
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
                backgroundColor: "var(--bf-tint)",
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
                    backgroundColor: "var(--bf-tint)",
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
            borderRight: "1px solid var(--bf-border)",
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
        background: gradient || undefined,
        bgcolor: gradient ? undefined : "background.paper",
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
              backgroundColor: gradient ? "rgba(255,255,255,.18)" : "var(--bf-tint)",
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
                backgroundColor: "var(--bf-tint)",
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
            backgroundColor: isUser ? "primary.main" : "background.paper",
            color: isUser ? "#ffffff" : "text.primary",
            border: isUser ? "none" : "1px solid var(--bf-border)",
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
        backgroundColor: "var(--bf-panel)",
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
          "radial-gradient(900px 420px at 20% 10%, var(--bf-glow) 0%, var(--bf-surface) 55%), var(--bf-surface)",
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

          <Box sx={{ mt: 3, p: 2, borderRadius: 3, backgroundColor: "var(--bf-surface)" }}>
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
          "radial-gradient(900px 420px at 80% 5%, var(--bf-glow) 0%, var(--bf-surface) 55%), var(--bf-surface)",
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
            caption={`Savings rate ${data.savings_rate}% this month`}
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

        <Grid item xs={12}>
          <SectionCard
            title="Daily spending"
            subtitle={`Last 14 days • average ${formatCurrency(data.average_daily_spend)} per day`}
          >
            <Box sx={{ height: 240 }}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={data.daily_spending}>
                  <CartesianGrid strokeDasharray="3 3" stroke="var(--bf-border)" />
                  <XAxis dataKey="label" tick={{ fontSize: 11 }} interval={0} angle={-25} dy={8} height={48} />
                  <YAxis tick={{ fontSize: 12 }} tickFormatter={(value) => `${value / 1000}k`} />
                  <ChartTooltip formatter={(value) => formatCurrency(value)} />
                  <Bar dataKey="amount" name="Spent" fill="#0ea5e9" radius={[6, 6, 0, 0]} maxBarSize={26} />
                </BarChart>
              </ResponsiveContainer>
            </Box>
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
                          backgroundColor: "var(--bf-tint)",
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
                    sx={{ p: 1.25, borderRadius: 2, backgroundColor: item.is_read ? "var(--bf-panel)" : "var(--bf-tint)" }}
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
import DownloadIcon from "@mui/icons-material/Download";

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
  const [exporting, setExporting] = useState(false);

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

  const exportCsv = async () => {
    setExporting(true);
    setError("");
    try {
      const blob = await bankingService.exportTransactions({
        search: debouncedSearch || undefined,
        category: filters.category,
        type: filters.type,
        status: filters.status,
        start_date: filters.start_date || undefined,
        end_date: filters.end_date || undefined,
        ordering: filters.ordering,
      });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = "bankflow-transactions.csv";
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    } catch (err) {
      setError("The CSV could not be created. Please try again.");
    } finally {
      setExporting(false);
    }
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
          <Stack direction="row" spacing={1.5}>
            <Button
              variant="outlined"
              startIcon={<FilterAltOffIcon />}
              onClick={resetFilters}
              disabled={activeFilterCount === 0 && !filters.search}
            >
              Reset filters{activeFilterCount ? ` (${activeFilterCount})` : ""}
            </Button>
            <Button
              variant="contained"
              startIcon={<DownloadIcon />}
              onClick={exportCsv}
              disabled={exporting}
            >
              {exporting ? "Preparing..." : "Export CSV"}
            </Button>
          </Stack>
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
        sx={{ mb: 2, borderBottom: "1px solid var(--bf-border)" }}
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

          <Box sx={{ mt: 3, p: 2, borderRadius: 3, backgroundColor: "var(--bf-surface)" }}>
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
          sx={{ p: 2, borderBottom: "1px solid var(--bf-border)" }}
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

        <Box sx={{ flexGrow: 1, overflowY: "auto", p: { xs: 2, md: 3 }, backgroundColor: "var(--bf-panel)" }}>
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
        <Box sx={{ p: 2, borderTop: "1px solid var(--bf-border)" }}>
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
        sx={{ mb: 2, borderBottom: "1px solid var(--bf-border)" }}
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
                  borderLeft: item.is_read ? "4px solid var(--bf-border)" : "4px solid #1b3a8f",
                  backgroundColor: item.is_read ? "var(--bf-paper)" : "var(--bf-panel)",
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
                      backgroundColor: "var(--bf-tint)",
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
import LockResetIcon from "@mui/icons-material/LockReset";

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
  const [passwordForm, setPasswordForm] = useState({
    current_password: "",
    new_password: "",
    confirm_password: "",
  });
  const [passwordErrors, setPasswordErrors] = useState({});
  const [changingPassword, setChangingPassword] = useState(false);

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

  const handlePasswordChange = async (event) => {
    event.preventDefault();
    const nextErrors = {};
    if (!passwordForm.current_password) {
      nextErrors.current_password = "Enter your current password.";
    }
    if (!passwordForm.new_password) {
      nextErrors.new_password = "Enter a new password.";
    } else if (passwordForm.new_password.length < 8) {
      nextErrors.new_password = "Use at least 8 characters.";
    } else if (passwordForm.new_password === passwordForm.current_password) {
      nextErrors.new_password = "Choose a password different from the current one.";
    }
    if (passwordForm.confirm_password !== passwordForm.new_password) {
      nextErrors.confirm_password = "The two new passwords do not match.";
    }
    setPasswordErrors(nextErrors);
    if (Object.keys(nextErrors).length) return;

    setChangingPassword(true);
    setError("");
    try {
      await authService.changePassword(passwordForm);
      setPasswordForm({ current_password: "", new_password: "", confirm_password: "" });
      setSnack("Password changed. Use the new password the next time you log in.");
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setChangingPassword(false);
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

          <SectionCard
            title="Change password"
            subtitle="Confirm your current password, then choose a new one"
            sx={{ mt: 2.5 }}
          >
            <form onSubmit={handlePasswordChange}>
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    type="password"
                    label="Current password"
                    autoComplete="current-password"
                    value={passwordForm.current_password}
                    onChange={(event) =>
                      setPasswordForm({ ...passwordForm, current_password: event.target.value })
                    }
                    error={Boolean(passwordErrors.current_password)}
                    helperText={passwordErrors.current_password}
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    type="password"
                    label="New password"
                    autoComplete="new-password"
                    value={passwordForm.new_password}
                    onChange={(event) =>
                      setPasswordForm({ ...passwordForm, new_password: event.target.value })
                    }
                    error={Boolean(passwordErrors.new_password)}
                    helperText={passwordErrors.new_password || "At least 8 characters."}
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    type="password"
                    label="Confirm new password"
                    autoComplete="new-password"
                    value={passwordForm.confirm_password}
                    onChange={(event) =>
                      setPasswordForm({ ...passwordForm, confirm_password: event.target.value })
                    }
                    error={Boolean(passwordErrors.confirm_password)}
                    helperText={passwordErrors.confirm_password}
                  />
                </Grid>
              </Grid>
              <Button
                type="submit"
                variant="outlined"
                startIcon={<LockResetIcon />}
                disabled={changingPassword}
                sx={{ mt: 2 }}
              >
                {changingPassword ? "Updating..." : "Change password"}
              </Button>
            </form>
          </SectionCard>
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
                  <Box sx={{ p: 2, borderRadius: 2, backgroundColor: "var(--bf-surface)" }}>
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

### frontend/package-lock.json

```json
{
  "name": "bankflow-frontend",
  "version": "1.0.0",
  "lockfileVersion": 3,
  "requires": true,
  "packages": {
    "": {
      "name": "bankflow-frontend",
      "version": "1.0.0",
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
    },
    "node_modules/@babel/code-frame": {
      "version": "7.29.7",
      "resolved": "https://registry.npmjs.org/@babel/code-frame/-/code-frame-7.29.7.tgz",
      "integrity": "sha512-Aup7aUOfpbAUg2ROOJN6Iw5f9DMBlzu0mIkm/malLQFN/YQgO48wCj0Kxa3sEHJvPVFg7siR+qRInwXd2qhQKw==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-validator-identifier": "^7.29.7",
        "js-tokens": "^4.0.0",
        "picocolors": "^1.1.1"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/compat-data": {
      "version": "7.29.7",
      "resolved": "https://registry.npmjs.org/@babel/compat-data/-/compat-data-7.29.7.tgz",
      "integrity": "sha512-locTkQyKvwIEgBzVrn8693ebc97F2U8ZHjbXwDXJ5Fn2TCpNwTlKcaKLkdHop5c/icOFE7qt7Q9JC5hnKNa6Gg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/core": {
      "version": "7.29.7",
      "resolved": "https://registry.npmjs.org/@babel/core/-/core-7.29.7.tgz",
      "integrity": "sha512-RgHBCvtjbOK2gXSNBNIkNoEc9qoVEtau3hj8gEqKQuL3HZAibKarWFEI3Lfm6EYKkLalOh8eSrj9b+ch9H/VBA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/code-frame": "^7.29.7",
        "@babel/generator": "^7.29.7",
        "@babel/helper-compilation-targets": "^7.29.7",
        "@babel/helper-module-transforms": "^7.29.7",
        "@babel/helpers": "^7.29.7",
        "@babel/parser": "^7.29.7",
        "@babel/template": "^7.29.7",
        "@babel/traverse": "^7.29.7",
        "@babel/types": "^7.29.7",
        "@jridgewell/remapping": "^2.3.5",
        "convert-source-map": "^2.0.0",
        "debug": "^4.1.0",
        "gensync": "^1.0.0-beta.2",
        "json5": "^2.2.3",
        "semver": "^6.3.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/babel"
      }
    },
    "node_modules/@babel/core/node_modules/convert-source-map": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/convert-source-map/-/convert-source-map-2.0.0.tgz",
      "integrity": "sha512-Kvp459HrV2FEJ1CAsi1Ku+MY3kasH19TFykTz2xWmMeq6bk2NU3XXvfJ+Q61m0xktWwt+1HSYf3JZsTms3aRJg==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/@babel/generator": {
      "version": "7.29.8",
      "resolved": "https://registry.npmjs.org/@babel/generator/-/generator-7.29.8.tgz",
      "integrity": "sha512-gZbepsdh3WDtgZKWL+vTPh71LSBrm/Y4/QDZBVCcYfmeTEEuoOYwlSy+G1StfJg+/Zy550u/3TATbm7qDbbMtg==",
      "license": "MIT",
      "dependencies": {
        "@babel/parser": "^7.29.8",
        "@babel/types": "^7.29.8",
        "@jridgewell/gen-mapping": "^0.3.12",
        "@jridgewell/trace-mapping": "^0.3.28",
        "jsesc": "^3.0.2"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-compilation-targets": {
      "version": "7.29.7",
      "resolved": "https://registry.npmjs.org/@babel/helper-compilation-targets/-/helper-compilation-targets-7.29.7.tgz",
      "integrity": "sha512-wem6WaBj4NaVYVdNhLPPVacES6ZJ+KBBfSkTMD3YZxbP3rm3Di85tJU5ljaUNhaOynt+Aj0xruhYuzQBt8n71g==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/compat-data": "^7.29.7",
        "@babel/helper-validator-option": "^7.29.7",
        "browserslist": "^4.24.0",
        "lru-cache": "^5.1.1",
        "semver": "^6.3.1"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-globals": {
      "version": "7.29.7",
      "resolved": "https://registry.npmjs.org/@babel/helper-globals/-/helper-globals-7.29.7.tgz",
      "integrity": "sha512-3nQVUAtvkKH9zahfWgw96Jc/uFOmjACE1kQz82E2lqWmHBgjzbNlsC22nuQTfahmWeQtTq5nQ/4Nnd2A1wj4zA==",
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-module-imports": {
      "version": "7.29.7",
      "resolved": "https://registry.npmjs.org/@babel/helper-module-imports/-/helper-module-imports-7.29.7.tgz",
      "integrity": "sha512-ejHwrQQYcm9xnTivShn2IDOlIzInN34AXskvq9QicvCtEzq1Vzclu/tKF8Jq1Cg8JG2GL6/EmjgsCT7lXepE3g==",
      "license": "MIT",
      "dependencies": {
        "@babel/traverse": "^7.29.7",
        "@babel/types": "^7.29.7"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-module-transforms": {
      "version": "7.29.7",
      "resolved": "https://registry.npmjs.org/@babel/helper-module-transforms/-/helper-module-transforms-7.29.7.tgz",
      "integrity": "sha512-UPUVSyXbOh627KiCIGQSgwWzGeBKLkaJ9PJEdrngIwMSzxLR4jS4+f1f1jb7VzBbg8nFLaYotvVPFCTqdrmTAg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-module-imports": "^7.29.7",
        "@babel/helper-validator-identifier": "^7.29.7",
        "@babel/traverse": "^7.29.7"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/@babel/helper-plugin-utils": {
      "version": "7.29.7",
      "resolved": "https://registry.npmjs.org/@babel/helper-plugin-utils/-/helper-plugin-utils-7.29.7.tgz",
      "integrity": "sha512-G7sHYigPY17oO5SYWnfD/0MTBwVR781S/JI643e/JhUYgVgWE/61SoW3NH9KWUKyKq5LVh3npif99Wkt6j86Jw==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-string-parser": {
      "version": "7.29.7",
      "resolved": "https://registry.npmjs.org/@babel/helper-string-parser/-/helper-string-parser-7.29.7.tgz",
      "integrity": "sha512-Pb5ijPrZ89GDH8223L4UP8i6QApWxs04RbPQJTeWDV0/keR2E36MeKnyr6LYmUUvqRRI+Iv87SuF1W6ErINzYw==",
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-validator-identifier": {
      "version": "7.29.7",
      "resolved": "https://registry.npmjs.org/@babel/helper-validator-identifier/-/helper-validator-identifier-7.29.7.tgz",
      "integrity": "sha512-qehxGkRj55h/ff8EMaJ+cYhyaKlHIxqYDn682wQD7RNp9UujOQsHog2uS0r2vzr4pW+sXf90NeeayjcNaX3fFg==",
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-validator-option": {
      "version": "7.29.7",
      "resolved": "https://registry.npmjs.org/@babel/helper-validator-option/-/helper-validator-option-7.29.7.tgz",
      "integrity": "sha512-N9ZErrD+yW5geCDtBqnOoxmR8+tNKiGuxKlDpuJxfsqpa2dFcexaziGAE/qoHLiDDreVNMupxGmSoNlyvsA3gw==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helpers": {
      "version": "7.29.7",
      "resolved": "https://registry.npmjs.org/@babel/helpers/-/helpers-7.29.7.tgz",
      "integrity": "sha512-1k2lAGRMfHTcwuNYcCNUmaUffmQv8KWMfh2iJUUeRlwlwH4FdNG7mfPI10NPfLHJFThE4Tyr4mv7kTNZOiPuBg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/template": "^7.29.7",
        "@babel/types": "^7.29.7"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/parser": {
      "version": "7.29.9",
      "resolved": "https://registry.npmjs.org/@babel/parser/-/parser-7.29.9.tgz",
      "integrity": "sha512-CjXrNHTnvqBVqHgdBysY3vk2T8tpJHb5/RMeHJBTyVa9xgugCB0CJTx/3oO8RV2QRQP391RWpB7D6hLjm8V9uA==",
      "license": "MIT",
      "dependencies": {
        "@babel/types": "^7.29.8"
      },
      "bin": {
        "parser": "bin/babel-parser.js"
      },
      "engines": {
        "node": ">=6.0.0"
      }
    },
    "node_modules/@babel/plugin-transform-react-jsx-self": {
      "version": "7.29.7",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-react-jsx-self/-/plugin-transform-react-jsx-self-7.29.7.tgz",
      "integrity": "sha512-TL0hMc9xzy86VD31nUiwzd5otRAcyEPcsegCxolO0PvcXuH1v0kECe/UIznYFihpkvU5wg/jk4v0TTEFfm53fw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.29.7"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-react-jsx-source": {
      "version": "7.29.7",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-react-jsx-source/-/plugin-transform-react-jsx-source-7.29.7.tgz",
      "integrity": "sha512-06IyK09H3wi4cGbhDBwp5gUGo0IKtnYa8tyTiephirPCK6fbobVGiXMMI5zLQ4aKEYP3wZ3ArU44o+8KMrSG/Q==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.29.7"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/runtime": {
      "version": "7.29.7",
      "resolved": "https://registry.npmjs.org/@babel/runtime/-/runtime-7.29.7.tgz",
      "integrity": "sha512-Nq8OhGWiZIZGV6hLHoyAKLLcJihP/xFeBMGJoUrxTX2psI8dCifzLhZISFb+VWS3wFMRDmCGw5R+dOySCqPLhw==",
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/template": {
      "version": "7.29.7",
      "resolved": "https://registry.npmjs.org/@babel/template/-/template-7.29.7.tgz",
      "integrity": "sha512-puq+Gf35oI24FeN11LkoUQFqv9uwNeWpxXZi/Ji3rRIoKAzKnxRaZ+Gkj0vKS9ZCiTESfng1N9LyOyXvo+m+Gg==",
      "license": "MIT",
      "dependencies": {
        "@babel/code-frame": "^7.29.7",
        "@babel/parser": "^7.29.7",
        "@babel/types": "^7.29.7"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/traverse": {
      "version": "7.29.8",
      "resolved": "https://registry.npmjs.org/@babel/traverse/-/traverse-7.29.8.tgz",
      "integrity": "sha512-I5z7H3bf/41ktsNVLtpN0wAa336HkqIHQ5BuPLEhTkt1jVSyZpeNKIzTgEWmlxjdg81R0IgUCcaE+Ok3NvrfZg==",
      "license": "MIT",
      "dependencies": {
        "@babel/code-frame": "^7.29.7",
        "@babel/generator": "^7.29.8",
        "@babel/helper-globals": "^7.29.7",
        "@babel/parser": "^7.29.8",
        "@babel/template": "^7.29.7",
        "@babel/types": "^7.29.8",
        "debug": "^4.3.1"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/types": {
      "version": "7.29.8",
      "resolved": "https://registry.npmjs.org/@babel/types/-/types-7.29.8.tgz",
      "integrity": "sha512-Vj1jF3cPfxg7OAfoI7QnVKLoILlm2JF9pnVHrX8qx7AHMiYWT+NDAA7jChlNgRS4WTLc/fD1lXLmPixluj+3Gg==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-string-parser": "^7.29.7",
        "@babel/helper-validator-identifier": "^7.29.7"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@emotion/babel-plugin": {
      "version": "11.13.5",
      "resolved": "https://registry.npmjs.org/@emotion/babel-plugin/-/babel-plugin-11.13.5.tgz",
      "integrity": "sha512-pxHCpT2ex+0q+HH91/zsdHkw/lXd468DIN2zvfvLtPKLLMo6gQj7oLObq8PhkrxOZb/gGCq03S3Z7PDhS8pduQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-module-imports": "^7.16.7",
        "@babel/runtime": "^7.18.3",
        "@emotion/hash": "^0.9.2",
        "@emotion/memoize": "^0.9.0",
        "@emotion/serialize": "^1.3.3",
        "babel-plugin-macros": "^3.1.0",
        "convert-source-map": "^1.5.0",
        "escape-string-regexp": "^4.0.0",
        "find-root": "^1.1.0",
        "source-map": "^0.5.7",
        "stylis": "4.2.0"
      }
    },
    "node_modules/@emotion/cache": {
      "version": "11.14.0",
      "resolved": "https://registry.npmjs.org/@emotion/cache/-/cache-11.14.0.tgz",
      "integrity": "sha512-L/B1lc/TViYk4DcpGxtAVbx0ZyiKM5ktoIyafGkH6zg/tj+mA+NE//aPYKG0k8kCHSHVJrpLpcAlOBEXQ3SavA==",
      "license": "MIT",
      "dependencies": {
        "@emotion/memoize": "^0.9.0",
        "@emotion/sheet": "^1.4.0",
        "@emotion/utils": "^1.4.2",
        "@emotion/weak-memoize": "^0.4.0",
        "stylis": "4.2.0"
      }
    },
    "node_modules/@emotion/hash": {
      "version": "0.9.2",
      "resolved": "https://registry.npmjs.org/@emotion/hash/-/hash-0.9.2.tgz",
      "integrity": "sha512-MyqliTZGuOm3+5ZRSaaBGP3USLw6+EGykkwZns2EPC5g8jJ4z9OrdZY9apkl3+UP9+sdz76YYkwCKP5gh8iY3g==",
      "license": "MIT"
    },
    "node_modules/@emotion/is-prop-valid": {
      "version": "1.4.0",
      "resolved": "https://registry.npmjs.org/@emotion/is-prop-valid/-/is-prop-valid-1.4.0.tgz",
      "integrity": "sha512-QgD4fyscGcbbKwJmqNvUMSE02OsHUa+lAWKdEUIJKgqe5IwRSKd7+KhibEWdaKwgjLj0DRSHA9biAIqGBk05lw==",
      "license": "MIT",
      "dependencies": {
        "@emotion/memoize": "^0.9.0"
      }
    },
    "node_modules/@emotion/memoize": {
      "version": "0.9.0",
      "resolved": "https://registry.npmjs.org/@emotion/memoize/-/memoize-0.9.0.tgz",
      "integrity": "sha512-30FAj7/EoJ5mwVPOWhAyCX+FPfMDrVecJAM+Iw9NRoSl4BBAQeqj4cApHHUXOVvIPgLVDsCFoz/hGD+5QQD1GQ==",
      "license": "MIT"
    },
    "node_modules/@emotion/react": {
      "version": "11.14.0",
      "resolved": "https://registry.npmjs.org/@emotion/react/-/react-11.14.0.tgz",
      "integrity": "sha512-O000MLDBDdk/EohJPFUqvnp4qnHeYkVP5B0xEG0D/L7cOKP9kefu2DXn8dj74cQfsEzUqh+sr1RzFqiL1o+PpA==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.18.3",
        "@emotion/babel-plugin": "^11.13.5",
        "@emotion/cache": "^11.14.0",
        "@emotion/serialize": "^1.3.3",
        "@emotion/use-insertion-effect-with-fallbacks": "^1.2.0",
        "@emotion/utils": "^1.4.2",
        "@emotion/weak-memoize": "^0.4.0",
        "hoist-non-react-statics": "^3.3.1"
      },
      "peerDependencies": {
        "react": ">=16.8.0"
      },
      "peerDependenciesMeta": {
        "@types/react": {
          "optional": true
        }
      }
    },
    "node_modules/@emotion/serialize": {
      "version": "1.3.3",
      "resolved": "https://registry.npmjs.org/@emotion/serialize/-/serialize-1.3.3.tgz",
      "integrity": "sha512-EISGqt7sSNWHGI76hC7x1CksiXPahbxEOrC5RjmFRJTqLyEK9/9hZvBbiYn70dw4wuwMKiEMCUlR6ZXTSWQqxA==",
      "license": "MIT",
      "dependencies": {
        "@emotion/hash": "^0.9.2",
        "@emotion/memoize": "^0.9.0",
        "@emotion/unitless": "^0.10.0",
        "@emotion/utils": "^1.4.2",
        "csstype": "^3.0.2"
      }
    },
    "node_modules/@emotion/sheet": {
      "version": "1.4.0",
      "resolved": "https://registry.npmjs.org/@emotion/sheet/-/sheet-1.4.0.tgz",
      "integrity": "sha512-fTBW9/8r2w3dXWYM4HCB1Rdp8NLibOw2+XELH5m5+AkWiL/KqYX6dc0kKYlaYyKjrQ6ds33MCdMPEwgs2z1rqg==",
      "license": "MIT"
    },
    "node_modules/@emotion/styled": {
      "version": "11.14.1",
      "resolved": "https://registry.npmjs.org/@emotion/styled/-/styled-11.14.1.tgz",
      "integrity": "sha512-qEEJt42DuToa3gurlH4Qqc1kVpNq8wO8cJtDzU46TjlzWjDlsVyevtYCRijVq3SrHsROS+gVQ8Fnea108GnKzw==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.18.3",
        "@emotion/babel-plugin": "^11.13.5",
        "@emotion/is-prop-valid": "^1.3.0",
        "@emotion/serialize": "^1.3.3",
        "@emotion/use-insertion-effect-with-fallbacks": "^1.2.0",
        "@emotion/utils": "^1.4.2"
      },
      "peerDependencies": {
        "@emotion/react": "^11.0.0-rc.0",
        "react": ">=16.8.0"
      },
      "peerDependenciesMeta": {
        "@types/react": {
          "optional": true
        }
      }
    },
    "node_modules/@emotion/unitless": {
      "version": "0.10.0",
      "resolved": "https://registry.npmjs.org/@emotion/unitless/-/unitless-0.10.0.tgz",
      "integrity": "sha512-dFoMUuQA20zvtVTuxZww6OHoJYgrzfKM1t52mVySDJnMSEa08ruEvdYQbhvyu6soU+NeLVd3yKfTfT0NeV6qGg==",
      "license": "MIT"
    },
    "node_modules/@emotion/use-insertion-effect-with-fallbacks": {
      "version": "1.2.0",
      "resolved": "https://registry.npmjs.org/@emotion/use-insertion-effect-with-fallbacks/-/use-insertion-effect-with-fallbacks-1.2.0.tgz",
      "integrity": "sha512-yJMtVdH59sxi/aVJBpk9FQq+OR8ll5GT8oWd57UpeaKEVGab41JWaCFA7FRLoMLloOZF/c/wsPoe+bfGmRKgDg==",
      "license": "MIT",
      "peerDependencies": {
        "react": ">=16.8.0"
      }
    },
    "node_modules/@emotion/utils": {
      "version": "1.4.2",
      "resolved": "https://registry.npmjs.org/@emotion/utils/-/utils-1.4.2.tgz",
      "integrity": "sha512-3vLclRofFziIa3J2wDh9jjbkUz9qk5Vi3IZ/FSTKViB0k+ef0fPV7dYrUIugbgupYDx7v9ud/SjrtEP8Y4xLoA==",
      "license": "MIT"
    },
    "node_modules/@emotion/weak-memoize": {
      "version": "0.4.0",
      "resolved": "https://registry.npmjs.org/@emotion/weak-memoize/-/weak-memoize-0.4.0.tgz",
      "integrity": "sha512-snKqtPW01tN0ui7yu9rGv69aJXr/a/Ywvl11sUjNtEcRc+ng/mQriFL0wLXMef74iHa/EkftbDzU9F8iFbH+zg==",
      "license": "MIT"
    },
    "node_modules/@esbuild/aix-ppc64": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/aix-ppc64/-/aix-ppc64-0.21.5.tgz",
      "integrity": "sha512-1SDgH6ZSPTlggy1yI6+Dbkiz8xzpHJEVAlF/AM1tHPLsf5STom9rwtjE4hKAF20FfXXNTFqEYXyJNWh1GiZedQ==",
      "cpu": [
        "ppc64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "aix"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@esbuild/android-arm": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/android-arm/-/android-arm-0.21.5.tgz",
      "integrity": "sha512-vCPvzSjpPHEi1siZdlvAlsPxXl7WbOVUBBAowWug4rJHb68Ox8KualB+1ocNvT5fjv6wpkX6o/iEpbDrf68zcg==",
      "cpu": [
        "arm"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "android"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@esbuild/android-arm64": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/android-arm64/-/android-arm64-0.21.5.tgz",
      "integrity": "sha512-c0uX9VAUBQ7dTDCjq+wdyGLowMdtR/GoC2U5IYk/7D1H1JYC0qseD7+11iMP2mRLN9RcCMRcjC4YMclCzGwS/A==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "android"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@esbuild/android-x64": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/android-x64/-/android-x64-0.21.5.tgz",
      "integrity": "sha512-D7aPRUUNHRBwHxzxRvp856rjUHRFW1SdQATKXH2hqA0kAZb1hKmi02OpYRacl0TxIGz/ZmXWlbZgjwWYaCakTA==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "android"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@esbuild/darwin-arm64": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/darwin-arm64/-/darwin-arm64-0.21.5.tgz",
      "integrity": "sha512-DwqXqZyuk5AiWWf3UfLiRDJ5EDd49zg6O9wclZ7kUMv2WRFr4HKjXp/5t8JZ11QbQfUS6/cRCKGwYhtNAY88kQ==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "darwin"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@esbuild/darwin-x64": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/darwin-x64/-/darwin-x64-0.21.5.tgz",
      "integrity": "sha512-se/JjF8NlmKVG4kNIuyWMV/22ZaerB+qaSi5MdrXtd6R08kvs2qCN4C09miupktDitvh8jRFflwGFBQcxZRjbw==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "darwin"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@esbuild/freebsd-arm64": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/freebsd-arm64/-/freebsd-arm64-0.21.5.tgz",
      "integrity": "sha512-5JcRxxRDUJLX8JXp/wcBCy3pENnCgBR9bN6JsY4OmhfUtIHe3ZW0mawA7+RDAcMLrMIZaf03NlQiX9DGyB8h4g==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "freebsd"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@esbuild/freebsd-x64": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/freebsd-x64/-/freebsd-x64-0.21.5.tgz",
      "integrity": "sha512-J95kNBj1zkbMXtHVH29bBriQygMXqoVQOQYA+ISs0/2l3T9/kj42ow2mpqerRBxDJnmkUDCaQT/dfNXWX/ZZCQ==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "freebsd"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@esbuild/linux-arm": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-arm/-/linux-arm-0.21.5.tgz",
      "integrity": "sha512-bPb5AHZtbeNGjCKVZ9UGqGwo8EUu4cLq68E95A53KlxAPRmUyYv2D6F0uUI65XisGOL1hBP5mTronbgo+0bFcA==",
      "cpu": [
        "arm"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@esbuild/linux-arm64": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-arm64/-/linux-arm64-0.21.5.tgz",
      "integrity": "sha512-ibKvmyYzKsBeX8d8I7MH/TMfWDXBF3db4qM6sy+7re0YXya+K1cem3on9XgdT2EQGMu4hQyZhan7TeQ8XkGp4Q==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@esbuild/linux-ia32": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-ia32/-/linux-ia32-0.21.5.tgz",
      "integrity": "sha512-YvjXDqLRqPDl2dvRODYmmhz4rPeVKYvppfGYKSNGdyZkA01046pLWyRKKI3ax8fbJoK5QbxblURkwK/MWY18Tg==",
      "cpu": [
        "ia32"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@esbuild/linux-loong64": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-loong64/-/linux-loong64-0.21.5.tgz",
      "integrity": "sha512-uHf1BmMG8qEvzdrzAqg2SIG/02+4/DHB6a9Kbya0XDvwDEKCoC8ZRWI5JJvNdUjtciBGFQ5PuBlpEOXQj+JQSg==",
      "cpu": [
        "loong64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@esbuild/linux-mips64el": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-mips64el/-/linux-mips64el-0.21.5.tgz",
      "integrity": "sha512-IajOmO+KJK23bj52dFSNCMsz1QP1DqM6cwLUv3W1QwyxkyIWecfafnI555fvSGqEKwjMXVLokcV5ygHW5b3Jbg==",
      "cpu": [
        "mips64el"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@esbuild/linux-ppc64": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-ppc64/-/linux-ppc64-0.21.5.tgz",
      "integrity": "sha512-1hHV/Z4OEfMwpLO8rp7CvlhBDnjsC3CttJXIhBi+5Aj5r+MBvy4egg7wCbe//hSsT+RvDAG7s81tAvpL2XAE4w==",
      "cpu": [
        "ppc64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@esbuild/linux-riscv64": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-riscv64/-/linux-riscv64-0.21.5.tgz",
      "integrity": "sha512-2HdXDMd9GMgTGrPWnJzP2ALSokE/0O5HhTUvWIbD3YdjME8JwvSCnNGBnTThKGEB91OZhzrJ4qIIxk/SBmyDDA==",
      "cpu": [
        "riscv64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@esbuild/linux-s390x": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-s390x/-/linux-s390x-0.21.5.tgz",
      "integrity": "sha512-zus5sxzqBJD3eXxwvjN1yQkRepANgxE9lgOW2qLnmr8ikMTphkjgXu1HR01K4FJg8h1kEEDAqDcZQtbrRnB41A==",
      "cpu": [
        "s390x"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@esbuild/linux-x64": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-x64/-/linux-x64-0.21.5.tgz",
      "integrity": "sha512-1rYdTpyv03iycF1+BhzrzQJCdOuAOtaqHTWJZCWvijKD2N5Xu0TtVC8/+1faWqcP9iBCWOmjmhoH94dH82BxPQ==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@esbuild/netbsd-x64": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/netbsd-x64/-/netbsd-x64-0.21.5.tgz",
      "integrity": "sha512-Woi2MXzXjMULccIwMnLciyZH4nCIMpWQAs049KEeMvOcNADVxo0UBIQPfSmxB3CWKedngg7sWZdLvLczpe0tLg==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "netbsd"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@esbuild/openbsd-x64": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/openbsd-x64/-/openbsd-x64-0.21.5.tgz",
      "integrity": "sha512-HLNNw99xsvx12lFBUwoT8EVCsSvRNDVxNpjZ7bPn947b8gJPzeHWyNVhFsaerc0n3TsbOINvRP2byTZ5LKezow==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "openbsd"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@esbuild/sunos-x64": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/sunos-x64/-/sunos-x64-0.21.5.tgz",
      "integrity": "sha512-6+gjmFpfy0BHU5Tpptkuh8+uw3mnrvgs+dSPQXQOv3ekbordwnzTVEb4qnIvQcYXq6gzkyTnoZ9dZG+D4garKg==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "sunos"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@esbuild/win32-arm64": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/win32-arm64/-/win32-arm64-0.21.5.tgz",
      "integrity": "sha512-Z0gOTd75VvXqyq7nsl93zwahcTROgqvuAcYDUr+vOv8uHhNSKROyU961kgtCD1e95IqPKSQKH7tBTslnS3tA8A==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "win32"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@esbuild/win32-ia32": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/win32-ia32/-/win32-ia32-0.21.5.tgz",
      "integrity": "sha512-SWXFF1CL2RVNMaVs+BBClwtfZSvDgtL//G/smwAc5oVK/UPu2Gu9tIaRgFmYFFKrmg3SyAjSrElf0TiJ1v8fYA==",
      "cpu": [
        "ia32"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "win32"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@esbuild/win32-x64": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/win32-x64/-/win32-x64-0.21.5.tgz",
      "integrity": "sha512-tQd/1efJuzPC6rCFwEvLtci/xNFcTZknmXs98FYDfGE4wP9ClFV98nyKrzJKVPMhdDnjzLhdUyMX4PsQAPjwIw==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "win32"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@jridgewell/gen-mapping": {
      "version": "0.3.13",
      "resolved": "https://registry.npmjs.org/@jridgewell/gen-mapping/-/gen-mapping-0.3.13.tgz",
      "integrity": "sha512-2kkt/7niJ6MgEPxF0bYdQ6etZaA+fQvDcLKckhy1yIQOzaoKjBBjSj63/aLVjYE3qhRt5dvM+uUyfCg6UKCBbA==",
      "license": "MIT",
      "dependencies": {
        "@jridgewell/sourcemap-codec": "^1.5.0",
        "@jridgewell/trace-mapping": "^0.3.24"
      }
    },
    "node_modules/@jridgewell/remapping": {
      "version": "2.3.5",
      "resolved": "https://registry.npmjs.org/@jridgewell/remapping/-/remapping-2.3.5.tgz",
      "integrity": "sha512-LI9u/+laYG4Ds1TDKSJW2YPrIlcVYOwi2fUC6xB43lueCjgxV4lffOCZCtYFiH6TNOX+tQKXx97T4IKHbhyHEQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@jridgewell/gen-mapping": "^0.3.5",
        "@jridgewell/trace-mapping": "^0.3.24"
      }
    },
    "node_modules/@jridgewell/resolve-uri": {
      "version": "3.1.2",
      "resolved": "https://registry.npmjs.org/@jridgewell/resolve-uri/-/resolve-uri-3.1.2.tgz",
      "integrity": "sha512-bRISgCIjP20/tbWSPWMEi54QVPRZExkuD9lJL+UIxUKtwVJA8wW1Trb1jMs1RFXo1CBTNZ/5hpC9QvmKWdopKw==",
      "license": "MIT",
      "engines": {
        "node": ">=6.0.0"
      }
    },
    "node_modules/@jridgewell/sourcemap-codec": {
      "version": "1.6.0",
      "resolved": "https://registry.npmjs.org/@jridgewell/sourcemap-codec/-/sourcemap-codec-1.6.0.tgz",
      "integrity": "sha512-T7jf+5zgsZHwNJ4lvQ7/aezbyk0nNX+zJVWpmHA7VYsEx7a7qr5Rg5IbtJFqkgze5Y2sruq1RUY8Q837Od7iFw==",
      "license": "MIT"
    },
    "node_modules/@jridgewell/trace-mapping": {
      "version": "0.3.31",
      "resolved": "https://registry.npmjs.org/@jridgewell/trace-mapping/-/trace-mapping-0.3.31.tgz",
      "integrity": "sha512-zzNR+SdQSDJzc8joaeP8QQoCQr8NuYx2dIIytl1QeBEZHJ9uW6hebsrYgbz8hJwUQao3TWCMtmfV8Nu1twOLAw==",
      "license": "MIT",
      "dependencies": {
        "@jridgewell/resolve-uri": "^3.1.0",
        "@jridgewell/sourcemap-codec": "^1.4.14"
      }
    },
    "node_modules/@mui/core-downloads-tracker": {
      "version": "5.18.0",
      "resolved": "https://registry.npmjs.org/@mui/core-downloads-tracker/-/core-downloads-tracker-5.18.0.tgz",
      "integrity": "sha512-jbhwoQ1AY200PSSOrNXmrFCaSDSJWP7qk6urkTmIirvRXDROkqe+QwcLlUiw/PrREwsIF/vm3/dAXvjlMHF0RA==",
      "license": "MIT",
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/mui-org"
      }
    },
    "node_modules/@mui/icons-material": {
      "version": "5.18.0",
      "resolved": "https://registry.npmjs.org/@mui/icons-material/-/icons-material-5.18.0.tgz",
      "integrity": "sha512-1s0vEZj5XFXDMmz3Arl/R7IncFqJ+WQ95LDp1roHWGDE2oCO3IS4/hmiOv1/8SD9r6B7tv9GLiqVZYHo+6PkTg==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.23.9"
      },
      "engines": {
        "node": ">=12.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/mui-org"
      },
      "peerDependencies": {
        "@mui/material": "^5.0.0",
        "@types/react": "^17.0.0 || ^18.0.0 || ^19.0.0",
        "react": "^17.0.0 || ^18.0.0 || ^19.0.0"
      },
      "peerDependenciesMeta": {
        "@types/react": {
          "optional": true
        }
      }
    },
    "node_modules/@mui/material": {
      "version": "5.18.0",
      "resolved": "https://registry.npmjs.org/@mui/material/-/material-5.18.0.tgz",
      "integrity": "sha512-bbH/HaJZpFtXGvWg3TsBWG4eyt3gah3E7nCNU8GLyRjVoWcA91Vm/T+sjHfUcwgJSw9iLtucfHBoq+qW/T30aA==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.23.9",
        "@mui/core-downloads-tracker": "^5.18.0",
        "@mui/system": "^5.18.0",
        "@mui/types": "~7.2.15",
        "@mui/utils": "^5.17.1",
        "@popperjs/core": "^2.11.8",
        "@types/react-transition-group": "^4.4.10",
        "clsx": "^2.1.0",
        "csstype": "^3.1.3",
        "prop-types": "^15.8.1",
        "react-is": "^19.0.0",
        "react-transition-group": "^4.4.5"
      },
      "engines": {
        "node": ">=12.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/mui-org"
      },
      "peerDependencies": {
        "@emotion/react": "^11.5.0",
        "@emotion/styled": "^11.3.0",
        "@types/react": "^17.0.0 || ^18.0.0 || ^19.0.0",
        "react": "^17.0.0 || ^18.0.0 || ^19.0.0",
        "react-dom": "^17.0.0 || ^18.0.0 || ^19.0.0"
      },
      "peerDependenciesMeta": {
        "@emotion/react": {
          "optional": true
        },
        "@emotion/styled": {
          "optional": true
        },
        "@types/react": {
          "optional": true
        }
      }
    },
    "node_modules/@mui/private-theming": {
      "version": "5.17.1",
      "resolved": "https://registry.npmjs.org/@mui/private-theming/-/private-theming-5.17.1.tgz",
      "integrity": "sha512-XMxU0NTYcKqdsG8LRmSoxERPXwMbp16sIXPcLVgLGII/bVNagX0xaheWAwFv8+zDK7tI3ajllkuD3GZZE++ICQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.23.9",
        "@mui/utils": "^5.17.1",
        "prop-types": "^15.8.1"
      },
      "engines": {
        "node": ">=12.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/mui-org"
      },
      "peerDependencies": {
        "@types/react": "^17.0.0 || ^18.0.0 || ^19.0.0",
        "react": "^17.0.0 || ^18.0.0 || ^19.0.0"
      },
      "peerDependenciesMeta": {
        "@types/react": {
          "optional": true
        }
      }
    },
    "node_modules/@mui/styled-engine": {
      "version": "5.18.0",
      "resolved": "https://registry.npmjs.org/@mui/styled-engine/-/styled-engine-5.18.0.tgz",
      "integrity": "sha512-BN/vKV/O6uaQh2z5rXV+MBlVrEkwoS/TK75rFQ2mjxA7+NBo8qtTAOA4UaM0XeJfn7kh2wZ+xQw2HAx0u+TiBg==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.23.9",
        "@emotion/cache": "^11.13.5",
        "@emotion/serialize": "^1.3.3",
        "csstype": "^3.1.3",
        "prop-types": "^15.8.1"
      },
      "engines": {
        "node": ">=12.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/mui-org"
      },
      "peerDependencies": {
        "@emotion/react": "^11.4.1",
        "@emotion/styled": "^11.3.0",
        "react": "^17.0.0 || ^18.0.0 || ^19.0.0"
      },
      "peerDependenciesMeta": {
        "@emotion/react": {
          "optional": true
        },
        "@emotion/styled": {
          "optional": true
        }
      }
    },
    "node_modules/@mui/system": {
      "version": "5.18.0",
      "resolved": "https://registry.npmjs.org/@mui/system/-/system-5.18.0.tgz",
      "integrity": "sha512-ojZGVcRWqWhu557cdO3pWHloIGJdzVtxs3rk0F9L+x55LsUjcMUVkEhiF7E4TMxZoF9MmIHGGs0ZX3FDLAf0Xw==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.23.9",
        "@mui/private-theming": "^5.17.1",
        "@mui/styled-engine": "^5.18.0",
        "@mui/types": "~7.2.15",
        "@mui/utils": "^5.17.1",
        "clsx": "^2.1.0",
        "csstype": "^3.1.3",
        "prop-types": "^15.8.1"
      },
      "engines": {
        "node": ">=12.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/mui-org"
      },
      "peerDependencies": {
        "@emotion/react": "^11.5.0",
        "@emotion/styled": "^11.3.0",
        "@types/react": "^17.0.0 || ^18.0.0 || ^19.0.0",
        "react": "^17.0.0 || ^18.0.0 || ^19.0.0"
      },
      "peerDependenciesMeta": {
        "@emotion/react": {
          "optional": true
        },
        "@emotion/styled": {
          "optional": true
        },
        "@types/react": {
          "optional": true
        }
      }
    },
    "node_modules/@mui/types": {
      "version": "7.2.24",
      "resolved": "https://registry.npmjs.org/@mui/types/-/types-7.2.24.tgz",
      "integrity": "sha512-3c8tRt/CbWZ+pEg7QpSwbdxOk36EfmhbKf6AGZsD1EcLDLTSZoxxJ86FVtcjxvjuhdyBiWKSTGZFaXCnidO2kw==",
      "license": "MIT",
      "peerDependencies": {
        "@types/react": "^17.0.0 || ^18.0.0 || ^19.0.0"
      },
      "peerDependenciesMeta": {
        "@types/react": {
          "optional": true
        }
      }
    },
    "node_modules/@mui/utils": {
      "version": "5.17.1",
      "resolved": "https://registry.npmjs.org/@mui/utils/-/utils-5.17.1.tgz",
      "integrity": "sha512-jEZ8FTqInt2WzxDV8bhImWBqeQRD99c/id/fq83H0ER9tFl+sfZlaAoCdznGvbSQQ9ividMxqSV2c7cC1vBcQg==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.23.9",
        "@mui/types": "~7.2.15",
        "@types/prop-types": "^15.7.12",
        "clsx": "^2.1.1",
        "prop-types": "^15.8.1",
        "react-is": "^19.0.0"
      },
      "engines": {
        "node": ">=12.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/mui-org"
      },
      "peerDependencies": {
        "@types/react": "^17.0.0 || ^18.0.0 || ^19.0.0",
        "react": "^17.0.0 || ^18.0.0 || ^19.0.0"
      },
      "peerDependenciesMeta": {
        "@types/react": {
          "optional": true
        }
      }
    },
    "node_modules/@napi-rs/lzma-linux-x64-gnu": {
      "version": "1.5.1",
      "resolved": "https://registry.npmjs.org/@napi-rs/lzma-linux-x64-gnu/-/lzma-linux-x64-gnu-1.5.1.tgz",
      "integrity": "sha512-oTXEIha4SsuXdTA4Iyskj0kpdx2yVXdhd75c2v3xGrHFfVMsbhTPZU/nMPL4sWKo4pBHm3aucLaqGlF696dTyQ==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "libc": [
        "glibc"
      ],
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": "^22.20 || ^24.12 || >=25"
      }
    },
    "node_modules/@popperjs/core": {
      "version": "2.11.8",
      "resolved": "https://registry.npmjs.org/@popperjs/core/-/core-2.11.8.tgz",
      "integrity": "sha512-P1st0aksCrn9sGZhp8GMYwBnQsbvAWsZAX44oXNNvLHGqAOcoVxmjZiohstwQ7SqKnbR47akdNi+uleWD8+g6A==",
      "license": "MIT",
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/popperjs"
      }
    },
    "node_modules/@remix-run/router": {
      "version": "1.23.4",
      "resolved": "https://registry.npmjs.org/@remix-run/router/-/router-1.23.4.tgz",
      "integrity": "sha512-q7j5geK7xs3UJSdm9/iytUNclBnLmYx1EnSeCFXHPeutdqgIMeFeHtUZgS3EhlKxdBEAu8OwtJCwmLrEzpSs7Q==",
      "license": "MIT",
      "engines": {
        "node": ">=14.0.0"
      }
    },
    "node_modules/@rolldown/pluginutils": {
      "version": "1.0.0-beta.27",
      "resolved": "https://registry.npmjs.org/@rolldown/pluginutils/-/pluginutils-1.0.0-beta.27.tgz",
      "integrity": "sha512-+d0F4MKMCbeVUJwG96uQ4SgAznZNSq93I3V+9NHA4OpvqG8mRCpGdKmK8l/dl02h2CCDHwW2FqilnTyDcAnqjA==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/@rollup/rollup-android-arm-eabi": {
      "version": "4.63.4",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-android-arm-eabi/-/rollup-android-arm-eabi-4.63.4.tgz",
      "integrity": "sha512-I+BSHzTAhKN2n7ZwGZsegGcZjDpLqFOMAtJz/u6uFGe0pUFbq56dEHjqJV/ZUdRJtNXNxA+hREUatZBvMR3Oiw==",
      "cpu": [
        "arm"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "android"
      ]
    },
    "node_modules/@rollup/rollup-android-arm64": {
      "version": "4.63.4",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-android-arm64/-/rollup-android-arm64-4.63.4.tgz",
      "integrity": "sha512-pu3BdjS2LtEzRu2elmGzS3fIeWSZy4BMDIaLNwjorO76+k2d0LMluijhsDx3KQyQBQ/lLUZCQA9/s6csvUfuhw==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "android"
      ]
    },
    "node_modules/@rollup/rollup-darwin-arm64": {
      "version": "4.63.4",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-darwin-arm64/-/rollup-darwin-arm64-4.63.4.tgz",
      "integrity": "sha512-xfSrj9MHnWK9GaSqT9U0ImHtH/N8WZlHLx4cZHiuLcqs640hvZ3hLPd5UR2AZS57FaE8HrRUSpltbZdWRxHiDA==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "darwin"
      ]
    },
    "node_modules/@rollup/rollup-darwin-x64": {
      "version": "4.63.4",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-darwin-x64/-/rollup-darwin-x64-4.63.4.tgz",
      "integrity": "sha512-bqU99PLJb/dqb3S0GIMdeuyAEETSUgZBoqXYd3Sd+WCsV+MmPhnN6JrotWyir31+QgH7EvvE5/mwGJlEoci8Fw==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "darwin"
      ]
    },
    "node_modules/@rollup/rollup-freebsd-arm64": {
      "version": "4.63.4",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-freebsd-arm64/-/rollup-freebsd-arm64-4.63.4.tgz",
      "integrity": "sha512-JinsFZ5G40oXQb+sUuiA5x689vhr6dDYK0H0NL+rwKdL6CqnmYN8PE4ZwfRSoIjrCxqTQG/SLfTtSvHeGxoVlw==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "freebsd"
      ]
    },
    "node_modules/@rollup/rollup-freebsd-x64": {
      "version": "4.63.4",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-freebsd-x64/-/rollup-freebsd-x64-4.63.4.tgz",
      "integrity": "sha512-GAdA4UxpiNm27cLHr2GqXBpAD0x9FqwYBY7/YSP0Ss0/PNi4k8gbviqpIpYbVSRBaS2ZcegXEzgTQMbRNCwxCw==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "freebsd"
      ]
    },
    "node_modules/@rollup/rollup-linux-arm-gnueabihf": {
      "version": "4.63.4",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-linux-arm-gnueabihf/-/rollup-linux-arm-gnueabihf-4.63.4.tgz",
      "integrity": "sha512-qDd6NoA1znaLjp4jR5U/KWCdLAKDJNB8W9ChbbDaKbo0xA+Atln5HK6LFCZ4oJQpemtRZA288DCirFRjrspptw==",
      "cpu": [
        "arm"
      ],
      "dev": true,
      "libc": [
        "glibc"
      ],
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@rollup/rollup-linux-arm-musleabihf": {
      "version": "4.63.4",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-linux-arm-musleabihf/-/rollup-linux-arm-musleabihf-4.63.4.tgz",
      "integrity": "sha512-WtB5Tz5KTNINb8ZA+8sQ7bmjuS1JrRT7YverYIhUGdWWDlpzVWmIwuZE+jidkEXUn1l0zrEkaIMa8dHF3NGcsA==",
      "cpu": [
        "arm"
      ],
      "dev": true,
      "libc": [
        "musl"
      ],
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@rollup/rollup-linux-arm64-gnu": {
      "version": "4.63.4",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-linux-arm64-gnu/-/rollup-linux-arm64-gnu-4.63.4.tgz",
      "integrity": "sha512-VcQ3L1tjnkKzWjryAVaFhHEWcqOfICX9uxVVoDzm2t0DpgKRHd2zOpVrJc0xsWeBZcBFyYROCIBdyR/fS174pg==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "libc": [
        "glibc"
      ],
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@rollup/rollup-linux-arm64-musl": {
      "version": "4.63.4",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-linux-arm64-musl/-/rollup-linux-arm64-musl-4.63.4.tgz",
      "integrity": "sha512-6+ZQX6P5s0cMDN2Ypb8Lbm2+/sZYmZjdaYny992ujUU9UKi/4CWoJWsl1pNvjWJHNHGK51m+jKGLlh1ylb2ifQ==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "libc": [
        "musl"
      ],
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@rollup/rollup-linux-loong64-gnu": {
      "version": "4.63.4",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-linux-loong64-gnu/-/rollup-linux-loong64-gnu-4.63.4.tgz",
      "integrity": "sha512-D72ZnvkFkBXOfzMMQLcwfPLyGkKb7HZ9/mf97B7v6/P5Lbv4oFOtSY/uHbS8lH6uKUOxoKiuokdb50XZSzzbJw==",
      "cpu": [
        "loong64"
      ],
      "dev": true,
      "libc": [
        "glibc"
      ],
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@rollup/rollup-linux-loong64-musl": {
      "version": "4.63.4",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-linux-loong64-musl/-/rollup-linux-loong64-musl-4.63.4.tgz",
      "integrity": "sha512-piU6BxeqA3O9KSu3kRCIQQtNqFFaTu21SEV4FwaRZowpnj3bLaWPZHw+xFqCs0XlJ+aOH3PTRWGoglH+mKA/OA==",
      "cpu": [
        "loong64"
      ],
      "dev": true,
      "libc": [
        "musl"
      ],
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@rollup/rollup-linux-ppc64-gnu": {
      "version": "4.63.4",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-linux-ppc64-gnu/-/rollup-linux-ppc64-gnu-4.63.4.tgz",
      "integrity": "sha512-/5PGpHwqt2EEEOUs1XwzubE/ucr0dWDQ+to3zqi4Ds7EWpwtQ79wXc4JBoxqj/OwpawTsKWzJxHfSuBOq3DrWA==",
      "cpu": [
        "ppc64"
      ],
      "dev": true,
      "libc": [
        "glibc"
      ],
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@rollup/rollup-linux-ppc64-musl": {
      "version": "4.63.4",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-linux-ppc64-musl/-/rollup-linux-ppc64-musl-4.63.4.tgz",
      "integrity": "sha512-cX3beZDLWt7G2oJF+nhChiT+qtaihs+S2xi7ziGmVB+2pwPng6D0Ed0HmElQOgv2UsUmSJJLGwpBao/3TDx3VA==",
      "cpu": [
        "ppc64"
      ],
      "dev": true,
      "libc": [
        "musl"
      ],
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@rollup/rollup-linux-riscv64-gnu": {
      "version": "4.63.4",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-linux-riscv64-gnu/-/rollup-linux-riscv64-gnu-4.63.4.tgz",
      "integrity": "sha512-1uz2mGWHyptR7DgHHrlbdRAjXK7v7elGZ9lMja910/RP+ZYbX6xAmCiU9UZSX4hqmgtHMv6lr5l3kq1HIOpcag==",
      "cpu": [
        "riscv64"
      ],
      "dev": true,
      "libc": [
        "glibc"
      ],
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@rollup/rollup-linux-riscv64-musl": {
      "version": "4.63.4",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-linux-riscv64-musl/-/rollup-linux-riscv64-musl-4.63.4.tgz",
      "integrity": "sha512-nLS8topojxyz7SRpKR2IODRpQ0XPZ+xaOXvT3+hqK/Uy8Lo5HFgkkIBiIrCu5tL5YqzTvgovGw55PwpahTAGig==",
      "cpu": [
        "riscv64"
      ],
      "dev": true,
      "libc": [
        "musl"
      ],
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@rollup/rollup-linux-s390x-gnu": {
      "version": "4.63.4",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-linux-s390x-gnu/-/rollup-linux-s390x-gnu-4.63.4.tgz",
      "integrity": "sha512-gs7DRKotr3l3q+jGPQBjH0ng1FjlEDm5ueQrkw5JtQvtLyEIcLASqAEaor56BhkKRzk+IcQzrcanBdb/bBQn8g==",
      "cpu": [
        "s390x"
      ],
      "dev": true,
      "libc": [
        "glibc"
      ],
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@rollup/rollup-linux-x64-gnu": {
      "version": "4.63.4",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-linux-x64-gnu/-/rollup-linux-x64-gnu-4.63.4.tgz",
      "integrity": "sha512-791ET7W17NnScOZM7h4dX5hYspxE28htPFsb1awY/NRR8+PRNkS53e475rDdxXXDrP+kwnCcNWg9CX5ztn/Aqw==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "libc": [
        "glibc"
      ],
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@rollup/rollup-linux-x64-musl": {
      "version": "4.63.4",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-linux-x64-musl/-/rollup-linux-x64-musl-4.63.4.tgz",
      "integrity": "sha512-iwZQRcmj7g88g3tzefIrQY7qvmuA/cfYwhrDtTBhsmukO4U2huVO5W+86XacUMRvdSFVAc6kZUZy21JaRwiB9w==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "libc": [
        "musl"
      ],
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@rollup/rollup-openbsd-x64": {
      "version": "4.63.4",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-openbsd-x64/-/rollup-openbsd-x64-4.63.4.tgz",
      "integrity": "sha512-dVHFp9gRWrdTpnqQuGfCwd7hOQDatK1VCP2iWhLY/cGrOQs/ucFzJ6A5SRqbXX12ZDI8EUuejSM5kwg+ja7Png==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "openbsd"
      ]
    },
    "node_modules/@rollup/rollup-openharmony-arm64": {
      "version": "4.63.4",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-openharmony-arm64/-/rollup-openharmony-arm64-4.63.4.tgz",
      "integrity": "sha512-t3NlauOW6gxZVVFcBEnO62Cb4wbyDFL416gTg1uFI/2tgqYQlf69FbSE115Ajre9I+c26Lk4mcmdFUsS/DGifQ==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "openharmony"
      ]
    },
    "node_modules/@rollup/rollup-win32-arm64-msvc": {
      "version": "4.63.4",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-win32-arm64-msvc/-/rollup-win32-arm64-msvc-4.63.4.tgz",
      "integrity": "sha512-xWuIaSye5FWZF8+UYtVEcHtRJDN5kN9Kfgxx3Kq8XIov9KSKbc1fiqQCm90SKrgQbUXZelbnUhnlUJmfSE7P9A==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "win32"
      ]
    },
    "node_modules/@rollup/rollup-win32-ia32-msvc": {
      "version": "4.63.4",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-win32-ia32-msvc/-/rollup-win32-ia32-msvc-4.63.4.tgz",
      "integrity": "sha512-9ALJJUOg/ZflMJepVo2PlgsGxSaxN7SQ4Z8GoZfVlarWr6r3rkHUNsd/zAio7p4YMtChSMXPionxej4Hkf6CXQ==",
      "cpu": [
        "ia32"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "win32"
      ]
    },
    "node_modules/@rollup/rollup-win32-x64-gnu": {
      "version": "4.63.4",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-win32-x64-gnu/-/rollup-win32-x64-gnu-4.63.4.tgz",
      "integrity": "sha512-blj9z5qx/Pv4WU0W1NMFDB97e0JH5ed+aZGywW8WCvp/NhWX/4PFAq5uu6Q0AebNn+Vo6KzUYDT++JzTT5ojlQ==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "win32"
      ]
    },
    "node_modules/@rollup/rollup-win32-x64-msvc": {
      "version": "4.63.4",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-win32-x64-msvc/-/rollup-win32-x64-msvc-4.63.4.tgz",
      "integrity": "sha512-Erx822VRBwLa124shbj+wNXe//BOgMEctDV0m1aqTQdNO1S69DgNUCFKC1RCeZfixs1J31l6igk1ziyXErbigQ==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "win32"
      ]
    },
    "node_modules/@types/babel__core": {
      "version": "7.20.5",
      "resolved": "https://registry.npmjs.org/@types/babel__core/-/babel__core-7.20.5.tgz",
      "integrity": "sha512-qoQprZvz5wQFJwMDqeseRXWv3rqMvhgpbXFfVyWhbx9X47POIA6i/+dXefEmZKoAgOaTdaIgNSMqMIU61yRyzA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/parser": "^7.20.7",
        "@babel/types": "^7.20.7",
        "@types/babel__generator": "*",
        "@types/babel__template": "*",
        "@types/babel__traverse": "*"
      }
    },
    "node_modules/@types/babel__generator": {
      "version": "7.27.0",
      "resolved": "https://registry.npmjs.org/@types/babel__generator/-/babel__generator-7.27.0.tgz",
      "integrity": "sha512-ufFd2Xi92OAVPYsy+P4n7/U7e68fex0+Ee8gSG9KX7eo084CWiQ4sdxktvdl0bOPupXtVJPY19zk6EwWqUQ8lg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/types": "^7.0.0"
      }
    },
    "node_modules/@types/babel__template": {
      "version": "7.4.4",
      "resolved": "https://registry.npmjs.org/@types/babel__template/-/babel__template-7.4.4.tgz",
      "integrity": "sha512-h/NUaSyG5EyxBIp8YRxo4RMe2/qQgvyowRwVMzhYhBCONbW8PUsg4lkFMrhgZhUe5z3L3MiLDuvyJ/CaPa2A8A==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/parser": "^7.1.0",
        "@babel/types": "^7.0.0"
      }
    },
    "node_modules/@types/babel__traverse": {
      "version": "7.28.0",
      "resolved": "https://registry.npmjs.org/@types/babel__traverse/-/babel__traverse-7.28.0.tgz",
      "integrity": "sha512-8PvcXf70gTDZBgt9ptxJ8elBeBjcLOAcOtoO/mPJjtji1+CdGbHgm77om1GrsPxsiE+uXIpNSK64UYaIwQXd4Q==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/types": "^7.28.2"
      }
    },
    "node_modules/@types/d3-array": {
      "version": "3.2.2",
      "resolved": "https://registry.npmjs.org/@types/d3-array/-/d3-array-3.2.2.tgz",
      "integrity": "sha512-hOLWVbm7uRza0BYXpIIW5pxfrKe0W+D5lrFiAEYR+pb6w3N2SwSMaJbXdUfSEv+dT4MfHBLtn5js0LAWaO6otw==",
      "license": "MIT"
    },
    "node_modules/@types/d3-color": {
      "version": "3.1.3",
      "resolved": "https://registry.npmjs.org/@types/d3-color/-/d3-color-3.1.3.tgz",
      "integrity": "sha512-iO90scth9WAbmgv7ogoq57O9YpKmFBbmoEoCHDB2xMBY0+/KVrqAaCDyCE16dUspeOvIxFFRI+0sEtqDqy2b4A==",
      "license": "MIT"
    },
    "node_modules/@types/d3-ease": {
      "version": "3.0.2",
      "resolved": "https://registry.npmjs.org/@types/d3-ease/-/d3-ease-3.0.2.tgz",
      "integrity": "sha512-NcV1JjO5oDzoK26oMzbILE6HW7uVXOHLQvHshBUW4UMdZGfiY6v5BeQwh9a9tCzv+CeefZQHJt5SRgK154RtiA==",
      "license": "MIT"
    },
    "node_modules/@types/d3-interpolate": {
      "version": "3.0.4",
      "resolved": "https://registry.npmjs.org/@types/d3-interpolate/-/d3-interpolate-3.0.4.tgz",
      "integrity": "sha512-mgLPETlrpVV1YRJIglr4Ez47g7Yxjl1lj7YKsiMCb27VJH9W8NVM6Bb9d8kkpG/uAQS5AmbA48q2IAolKKo1MA==",
      "license": "MIT",
      "dependencies": {
        "@types/d3-color": "*"
      }
    },
    "node_modules/@types/d3-path": {
      "version": "3.1.1",
      "resolved": "https://registry.npmjs.org/@types/d3-path/-/d3-path-3.1.1.tgz",
      "integrity": "sha512-VMZBYyQvbGmWyWVea0EHs/BwLgxc+MKi1zLDCONksozI4YJMcTt8ZEuIR4Sb1MMTE8MMW49v0IwI5+b7RmfWlg==",
      "license": "MIT"
    },
    "node_modules/@types/d3-scale": {
      "version": "4.0.9",
      "resolved": "https://registry.npmjs.org/@types/d3-scale/-/d3-scale-4.0.9.tgz",
      "integrity": "sha512-dLmtwB8zkAeO/juAMfnV+sItKjlsw2lKdZVVy6LRr0cBmegxSABiLEpGVmSJJ8O08i4+sGR6qQtb6WtuwJdvVw==",
      "license": "MIT",
      "dependencies": {
        "@types/d3-time": "*"
      }
    },
    "node_modules/@types/d3-shape": {
      "version": "3.2.0",
      "resolved": "https://registry.npmjs.org/@types/d3-shape/-/d3-shape-3.2.0.tgz",
      "integrity": "sha512-kVd74ta9eof3eJOvbNd1vGKS/XERRyQbT26Og63hIsvDO84cjD5gEOhsXf26w3FSoNlPVz84DOFcKv/oou+fMw==",
      "license": "MIT",
      "dependencies": {
        "@types/d3-path": "*"
      }
    },
    "node_modules/@types/d3-time": {
      "version": "3.0.4",
      "resolved": "https://registry.npmjs.org/@types/d3-time/-/d3-time-3.0.4.tgz",
      "integrity": "sha512-yuzZug1nkAAaBlBBikKZTgzCeA+k1uy4ZFwWANOfKw5z5LRhV0gNA7gNkKm7HoK+HRN0wX3EkxGk0fpbWhmB7g==",
      "license": "MIT"
    },
    "node_modules/@types/d3-timer": {
      "version": "3.0.2",
      "resolved": "https://registry.npmjs.org/@types/d3-timer/-/d3-timer-3.0.2.tgz",
      "integrity": "sha512-Ps3T8E8dZDam6fUyNiMkekK3XUsaUEik+idO9/YjPtfj2qruF8tFBXS7XhtE4iIXBLxhmLjP3SXpLhVf21I9Lw==",
      "license": "MIT"
    },
    "node_modules/@types/estree": {
      "version": "1.0.9",
      "resolved": "https://registry.npmjs.org/@types/estree/-/estree-1.0.9.tgz",
      "integrity": "sha512-GhdPgy1el4/ImP05X05Uw4cw2/M93BCUmnEvWZNStlCzEKME4Fkk+YpoA5OiHNQmoS7Cafb8Xa3Pya8m1Qrzeg==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/@types/parse-json": {
      "version": "4.0.2",
      "resolved": "https://registry.npmjs.org/@types/parse-json/-/parse-json-4.0.2.tgz",
      "integrity": "sha512-dISoDXWWQwUquiKsyZ4Ng+HX2KsPL7LyHKHQwgGFEA3IaKac4Obd+h2a/a6waisAoepJlBcx9paWqjA8/HVjCw==",
      "license": "MIT"
    },
    "node_modules/@types/prop-types": {
      "version": "15.7.15",
      "resolved": "https://registry.npmjs.org/@types/prop-types/-/prop-types-15.7.15.tgz",
      "integrity": "sha512-F6bEyamV9jKGAFBEmlQnesRPGOQqS2+Uwi0Em15xenOxHaf2hv6L8YCVn3rPdPJOiJfPiCnLIRyvwVaqMY3MIw==",
      "license": "MIT"
    },
    "node_modules/@types/react": {
      "version": "19.3.0",
      "resolved": "https://registry.npmjs.org/@types/react/-/react-19.3.0.tgz",
      "integrity": "sha512-N0rFCuH9YoxG9/m61l9MfpJKfmLOVU0em7ipIz6TRgSSkvReLB9vL85GB+yr8Bs5leqpvg96JSwF4ZS1s4viQg==",
      "license": "MIT",
      "peer": true,
      "dependencies": {
        "csstype": "^3.2.2"
      }
    },
    "node_modules/@types/react-transition-group": {
      "version": "4.4.12",
      "resolved": "https://registry.npmjs.org/@types/react-transition-group/-/react-transition-group-4.4.12.tgz",
      "integrity": "sha512-8TV6R3h2j7a91c+1DXdJi3Syo69zzIZbz7Lg5tORM5LEJG7X/E6a1V3drRyBRZq7/utz7A+c4OgYLiLcYGHG6w==",
      "license": "MIT",
      "peerDependencies": {
        "@types/react": "*"
      }
    },
    "node_modules/@vitejs/plugin-react": {
      "version": "4.7.0",
      "resolved": "https://registry.npmjs.org/@vitejs/plugin-react/-/plugin-react-4.7.0.tgz",
      "integrity": "sha512-gUu9hwfWvvEDBBmgtAowQCojwZmJ5mcLn3aufeCsitijs3+f2NsrPtlAWIR6OPiqljl96GVCUbLe0HyqIpVaoA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/core": "^7.28.0",
        "@babel/plugin-transform-react-jsx-self": "^7.27.1",
        "@babel/plugin-transform-react-jsx-source": "^7.27.1",
        "@rolldown/pluginutils": "1.0.0-beta.27",
        "@types/babel__core": "^7.20.5",
        "react-refresh": "^0.17.0"
      },
      "engines": {
        "node": "^14.18.0 || >=16.0.0"
      },
      "peerDependencies": {
        "vite": "^4.2.0 || ^5.0.0 || ^6.0.0 || ^7.0.0"
      }
    },
    "node_modules/agent-base": {
      "version": "6.0.2",
      "resolved": "https://registry.npmjs.org/agent-base/-/agent-base-6.0.2.tgz",
      "integrity": "sha512-RZNwNclF7+MS/8bDg70amg32dyeZGZxiDuQmZxKLAlQjr3jGyLx+4Kkk58UO7D2QdgFIQCovuSuZESne6RG6XQ==",
      "license": "MIT",
      "dependencies": {
        "debug": "4"
      },
      "engines": {
        "node": ">= 6.0.0"
      }
    },
    "node_modules/asynckit": {
      "version": "0.4.0",
      "resolved": "https://registry.npmjs.org/asynckit/-/asynckit-0.4.0.tgz",
      "integrity": "sha512-Oei9OH4tRh0YqU3GxhX79dM/mwVgvbZJaSNaRk+bshkj0S5cfHcgYakreBjrHwatXKbz+IoIdYLxrKim2MjW0Q==",
      "license": "MIT"
    },
    "node_modules/axios": {
      "version": "1.20.0",
      "resolved": "https://registry.npmjs.org/axios/-/axios-1.20.0.tgz",
      "integrity": "sha512-r8aOh8j9cGKpgQAqpzrUHnSIc6a59Y3Xf/cv8sy1DrHCkZHzQGEuoq1tARk6qSyDdtQGSDgpb9kFlruzPvrgwg==",
      "license": "MIT",
      "dependencies": {
        "follow-redirects": "^1.16.0",
        "form-data": "^4.0.6",
        "https-proxy-agent": "^5.0.1",
        "proxy-from-env": "^2.1.0"
      }
    },
    "node_modules/babel-plugin-macros": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/babel-plugin-macros/-/babel-plugin-macros-3.1.0.tgz",
      "integrity": "sha512-Cg7TFGpIr01vOQNODXOOaGz2NpCU5gl8x1qJFbb6hbZxR7XrcE2vtbAsTAbJ7/xwJtUuJEw8K8Zr/AE0LHlesg==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.12.5",
        "cosmiconfig": "^7.0.0",
        "resolve": "^1.19.0"
      },
      "engines": {
        "node": ">=10",
        "npm": ">=6"
      }
    },
    "node_modules/baseline-browser-mapping": {
      "version": "2.11.25",
      "resolved": "https://registry.npmjs.org/baseline-browser-mapping/-/baseline-browser-mapping-2.11.25.tgz",
      "integrity": "sha512-gMmEShwwq7FJqMwvfRwvCl00v4kN+KOfJqXn+f4nrufak5gNHJOksd/60Dvjuz7sI8Y5WiSFBa8FEYr+zoyqCw==",
      "dev": true,
      "license": "Apache-2.0",
      "bin": {
        "baseline-browser-mapping": "dist/cli.cjs"
      },
      "engines": {
        "node": ">=6.0.0"
      }
    },
    "node_modules/browserslist": {
      "version": "4.29.0",
      "resolved": "https://registry.npmjs.org/browserslist/-/browserslist-4.29.0.tgz",
      "integrity": "sha512-3GSvyjvDI4Dur1Meg2BekJquu5uF+9R9a1+5M1Mde192eZoXbeXjzgOsgqPS2V8D5wrrip0gR5Hf/GhWQ9ZzaA==",
      "dev": true,
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/browserslist"
        },
        {
          "type": "tidelift",
          "url": "https://tidelift.com/funding/github/npm/browserslist"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "MIT",
      "dependencies": {
        "baseline-browser-mapping": "^2.11.23",
        "caniuse-lite": "^1.0.30001810",
        "electron-to-chromium": "^1.5.427",
        "node-releases": "^2.0.55",
        "update-browserslist-db": "^1.3.3"
      },
      "bin": {
        "browserslist": "cli.js"
      },
      "engines": {
        "node": "^6 || ^7 || ^8 || ^9 || ^10 || ^11 || ^12 || >=13.7"
      }
    },
    "node_modules/call-bind-apply-helpers": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/call-bind-apply-helpers/-/call-bind-apply-helpers-1.0.2.tgz",
      "integrity": "sha512-Sp1ablJ0ivDkSzjcaJdxEunN5/XvksFJ2sMBFfq6x0ryhQV/2b/KwFe21cMpmHtPOSij8K99/wSfoEuTObmuMQ==",
      "license": "MIT",
      "dependencies": {
        "es-errors": "^1.3.0",
        "function-bind": "^1.1.2"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/callsites": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/callsites/-/callsites-3.1.0.tgz",
      "integrity": "sha512-P8BjAsXvZS+VIDUI11hHCQEv74YT67YUi5JJFNWIqL235sBmjX4+qx9Muvls5ivyNENctx46xQLQ3aTuE7ssaQ==",
      "license": "MIT",
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/caniuse-lite": {
      "version": "1.0.30001810",
      "resolved": "https://registry.npmjs.org/caniuse-lite/-/caniuse-lite-1.0.30001810.tgz",
      "integrity": "sha512-TITQPUkaz+aVk5GL6NhOdwk1aEaNTSDPsGFWrTuhKGtjTF70jL/Oht2W4c6rXUe5fu7Ie19VIahAXHIIiWWNeg==",
      "dev": true,
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/browserslist"
        },
        {
          "type": "tidelift",
          "url": "https://tidelift.com/funding/github/npm/caniuse-lite"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "CC-BY-4.0"
    },
    "node_modules/clsx": {
      "version": "2.1.1",
      "resolved": "https://registry.npmjs.org/clsx/-/clsx-2.1.1.tgz",
      "integrity": "sha512-eYm0QWBtUrBWZWG0d386OGAw16Z995PiOVo2B7bjWSbHedGl5e0ZWaq65kOGgUSNesEIDkB9ISbTg/JK9dhCZA==",
      "license": "MIT",
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/combined-stream": {
      "version": "1.0.8",
      "resolved": "https://registry.npmjs.org/combined-stream/-/combined-stream-1.0.8.tgz",
      "integrity": "sha512-FQN4MRfuJeHf7cBbBMJFXhKSDq+2kAArBlmRBvcvFE5BB1HZKXtSFASDhdlz9zOYwxh8lDdnvmMOe/+5cdoEdg==",
      "license": "MIT",
      "dependencies": {
        "delayed-stream": "~1.0.0"
      },
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/convert-source-map": {
      "version": "1.9.0",
      "resolved": "https://registry.npmjs.org/convert-source-map/-/convert-source-map-1.9.0.tgz",
      "integrity": "sha512-ASFBup0Mz1uyiIjANan1jzLQami9z1PoYSZCiiYW2FczPbenXc45FZdBZLzOT+r6+iciuEModtmCti+hjaAk0A==",
      "license": "MIT"
    },
    "node_modules/cosmiconfig": {
      "version": "7.1.0",
      "resolved": "https://registry.npmjs.org/cosmiconfig/-/cosmiconfig-7.1.0.tgz",
      "integrity": "sha512-AdmX6xUzdNASswsFtmwSt7Vj8po9IuqXm0UXz7QKPuEUmPB4XyjGfaAr2PSuELMwkRMVH1EpIkX5bTZGRB3eCA==",
      "license": "MIT",
      "dependencies": {
        "@types/parse-json": "^4.0.0",
        "import-fresh": "^3.2.1",
        "parse-json": "^5.0.0",
        "path-type": "^4.0.0",
        "yaml": "^1.10.0"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/csstype": {
      "version": "3.2.3",
      "resolved": "https://registry.npmjs.org/csstype/-/csstype-3.2.3.tgz",
      "integrity": "sha512-z1HGKcYy2xA8AGQfwrn0PAy+PB7X/GSj3UVJW9qKyn43xWa+gl5nXmU4qqLMRzWVLFC8KusUX8T/0kCiOYpAIQ==",
      "license": "MIT"
    },
    "node_modules/d3-array": {
      "version": "3.2.4",
      "resolved": "https://registry.npmjs.org/d3-array/-/d3-array-3.2.4.tgz",
      "integrity": "sha512-tdQAmyA18i4J7wprpYq8ClcxZy3SC31QMeByyCFyRt7BVHdREQZ5lpzoe5mFEYZUWe+oq8HBvk9JjpibyEV4Jg==",
      "license": "ISC",
      "dependencies": {
        "internmap": "1 - 2"
      },
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/d3-color": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/d3-color/-/d3-color-3.1.0.tgz",
      "integrity": "sha512-zg/chbXyeBtMQ1LbD/WSoW2DpC3I0mpmPdW+ynRTj/x2DAWYrIY7qeZIHidozwV24m4iavr15lNwIwLxRmOxhA==",
      "license": "ISC",
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/d3-ease": {
      "version": "3.0.1",
      "resolved": "https://registry.npmjs.org/d3-ease/-/d3-ease-3.0.1.tgz",
      "integrity": "sha512-wR/XK3D3XcLIZwpbvQwQ5fK+8Ykds1ip7A2Txe0yxncXSdq1L9skcG7blcedkOX+ZcgxGAmLX1FrRGbADwzi0w==",
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/d3-format": {
      "version": "3.1.2",
      "resolved": "https://registry.npmjs.org/d3-format/-/d3-format-3.1.2.tgz",
      "integrity": "sha512-AJDdYOdnyRDV5b6ArilzCPPwc1ejkHcoyFarqlPqT7zRYjhavcT3uSrqcMvsgh2CgoPbK3RCwyHaVyxYcP2Arg==",
      "license": "ISC",
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/d3-interpolate": {
      "version": "3.0.1",
      "resolved": "https://registry.npmjs.org/d3-interpolate/-/d3-interpolate-3.0.1.tgz",
      "integrity": "sha512-3bYs1rOD33uo8aqJfKP3JWPAibgw8Zm2+L9vBKEHJ2Rg+viTR7o5Mmv5mZcieN+FRYaAOWX5SJATX6k1PWz72g==",
      "license": "ISC",
      "dependencies": {
        "d3-color": "1 - 3"
      },
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/d3-path": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/d3-path/-/d3-path-3.1.0.tgz",
      "integrity": "sha512-p3KP5HCf/bvjBSSKuXid6Zqijx7wIfNW+J/maPs+iwR35at5JCbLUT0LzF1cnjbCHWhqzQTIN2Jpe8pRebIEFQ==",
      "license": "ISC",
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/d3-scale": {
      "version": "4.0.2",
      "resolved": "https://registry.npmjs.org/d3-scale/-/d3-scale-4.0.2.tgz",
      "integrity": "sha512-GZW464g1SH7ag3Y7hXjf8RoUuAFIqklOAq3MRl4OaWabTFJY9PN/E1YklhXLh+OQ3fM9yS2nOkCoS+WLZ6kvxQ==",
      "license": "ISC",
      "dependencies": {
        "d3-array": "2.10.0 - 3",
        "d3-format": "1 - 3",
        "d3-interpolate": "1.2.0 - 3",
        "d3-time": "2.1.1 - 3",
        "d3-time-format": "2 - 4"
      },
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/d3-shape": {
      "version": "3.2.0",
      "resolved": "https://registry.npmjs.org/d3-shape/-/d3-shape-3.2.0.tgz",
      "integrity": "sha512-SaLBuwGm3MOViRq2ABk3eLoxwZELpH6zhl3FbAoJ7Vm1gofKx6El1Ib5z23NUEhF9AsGl7y+dzLe5Cw2AArGTA==",
      "license": "ISC",
      "dependencies": {
        "d3-path": "^3.1.0"
      },
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/d3-time": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/d3-time/-/d3-time-3.1.0.tgz",
      "integrity": "sha512-VqKjzBLejbSMT4IgbmVgDjpkYrNWUYJnbCGo874u7MMKIWsILRX+OpX/gTk8MqjpT1A/c6HY2dCA77ZN0lkQ2Q==",
      "license": "ISC",
      "dependencies": {
        "d3-array": "2 - 3"
      },
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/d3-time-format": {
      "version": "4.1.0",
      "resolved": "https://registry.npmjs.org/d3-time-format/-/d3-time-format-4.1.0.tgz",
      "integrity": "sha512-dJxPBlzC7NugB2PDLwo9Q8JiTR3M3e4/XANkreKSUxF8vvXKqm1Yfq4Q5dl8budlunRVlUUaDUgFt7eA8D6NLg==",
      "license": "ISC",
      "dependencies": {
        "d3-time": "1 - 3"
      },
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/d3-timer": {
      "version": "3.0.1",
      "resolved": "https://registry.npmjs.org/d3-timer/-/d3-timer-3.0.1.tgz",
      "integrity": "sha512-ndfJ/JxxMd3nw31uyKoY2naivF+r29V+Lc0svZxe1JvvIRmi8hUsrMvdOwgS1o6uBHmiz91geQ0ylPP0aj1VUA==",
      "license": "ISC",
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/debug": {
      "version": "4.4.3",
      "resolved": "https://registry.npmjs.org/debug/-/debug-4.4.3.tgz",
      "integrity": "sha512-RGwwWnwQvkVfavKVt22FGLw+xYSdzARwm0ru6DhTVA3umU5hZc28V3kO4stgYryrTlLpuvgI9GiijltAjNbcqA==",
      "license": "MIT",
      "dependencies": {
        "ms": "^2.1.3"
      },
      "engines": {
        "node": ">=6.0"
      },
      "peerDependenciesMeta": {
        "supports-color": {
          "optional": true
        }
      }
    },
    "node_modules/decimal.js-light": {
      "version": "2.5.1",
      "resolved": "https://registry.npmjs.org/decimal.js-light/-/decimal.js-light-2.5.1.tgz",
      "integrity": "sha512-qIMFpTMZmny+MMIitAB6D7iVPEorVw6YQRWkvarTkT4tBeSLLiHzcwj6q0MmYSFCiVpiqPJTJEYIrpcPzVEIvg==",
      "license": "MIT"
    },
    "node_modules/delayed-stream": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/delayed-stream/-/delayed-stream-1.0.0.tgz",
      "integrity": "sha512-ZySD7Nf91aLB0RxL4KGrKHBXl7Eds1DAmEdcoVawXnLD7SDhpNgtuII2aAkg7a7QS41jxPSZ17p4VdGnMHk3MQ==",
      "license": "MIT",
      "engines": {
        "node": ">=0.4.0"
      }
    },
    "node_modules/dom-helpers": {
      "version": "5.2.1",
      "resolved": "https://registry.npmjs.org/dom-helpers/-/dom-helpers-5.2.1.tgz",
      "integrity": "sha512-nRCa7CK3VTrM2NmGkIy4cbK7IZlgBE/PYMn55rrXefr5xXDP0LdtfPnblFDoVdcAfslJ7or6iqAUnx0CCGIWQA==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.8.7",
        "csstype": "^3.0.2"
      }
    },
    "node_modules/dunder-proto": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/dunder-proto/-/dunder-proto-1.0.1.tgz",
      "integrity": "sha512-KIN/nDJBQRcXw0MLVhZE9iQHmG68qAVIBg9CqmUYjmQIhgij9U5MFvrqkUL5FbtyyzZuOeOt0zdeRe4UY7ct+A==",
      "license": "MIT",
      "dependencies": {
        "call-bind-apply-helpers": "^1.0.1",
        "es-errors": "^1.3.0",
        "gopd": "^1.2.0"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/electron-to-chromium": {
      "version": "1.5.433",
      "resolved": "https://registry.npmjs.org/electron-to-chromium/-/electron-to-chromium-1.5.433.tgz",
      "integrity": "sha512-5lCAbyZBjtmUt/RAGHRqrL2q0oEFRThDAsZHHDn9XHa89Qw7gMYOeSicBTy+AHfvo0r6vwsZvqNJTQIQy1BLzA==",
      "dev": true,
      "license": "ISC"
    },
    "node_modules/error-ex": {
      "version": "1.3.4",
      "resolved": "https://registry.npmjs.org/error-ex/-/error-ex-1.3.4.tgz",
      "integrity": "sha512-sqQamAnR14VgCr1A618A3sGrygcpK+HEbenA/HiEAkkUwcZIIB/tgWqHFxWgOyDh4nB4JCRimh79dR5Ywc9MDQ==",
      "license": "MIT",
      "dependencies": {
        "is-arrayish": "^0.2.1"
      }
    },
    "node_modules/es-define-property": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/es-define-property/-/es-define-property-1.0.1.tgz",
      "integrity": "sha512-e3nRfgfUZ4rNGL232gUgX06QNyyez04KdjFrF+LTRoOXmrOgFKDg4BCdsjW8EnT69eqdYGmRpJwiPVYNrCaW3g==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/es-errors": {
      "version": "1.3.0",
      "resolved": "https://registry.npmjs.org/es-errors/-/es-errors-1.3.0.tgz",
      "integrity": "sha512-Zf5H2Kxt2xjTvbJvP2ZWLEICxA6j+hAmMzIlypy4xcBg1vKVnx89Wy0GbS+kf5cwCVFFzdCFh2XSCFNULS6csw==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/es-object-atoms": {
      "version": "1.1.2",
      "resolved": "https://registry.npmjs.org/es-object-atoms/-/es-object-atoms-1.1.2.tgz",
      "integrity": "sha512-HWcBoN6NileqtSydK2FqHbS/LoDd2pqrnQHLyJzBj4kOp/ky2MWMN694xOfkK8/SnUsW2DH7EfyVlydKCsm1Zw==",
      "license": "MIT",
      "dependencies": {
        "es-errors": "^1.3.0"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/es-set-tostringtag": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/es-set-tostringtag/-/es-set-tostringtag-2.1.0.tgz",
      "integrity": "sha512-j6vWzfrGVfyXxge+O0x5sh6cvxAog0a/4Rdd2K36zCMV5eJ+/+tOAngRO8cODMNWbVRdVlmGZQL2YS3yR8bIUA==",
      "license": "MIT",
      "dependencies": {
        "es-errors": "^1.3.0",
        "get-intrinsic": "^1.2.6",
        "has-tostringtag": "^1.0.2",
        "hasown": "^2.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/esbuild": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/esbuild/-/esbuild-0.21.5.tgz",
      "integrity": "sha512-mg3OPMV4hXywwpoDxu3Qda5xCKQi+vCTZq8S9J/EpkhB2HzKXq4SNFZE3+NK93JYxc8VMSep+lOUSC/RVKaBqw==",
      "dev": true,
      "hasInstallScript": true,
      "license": "MIT",
      "bin": {
        "esbuild": "bin/esbuild"
      },
      "engines": {
        "node": ">=12"
      },
      "optionalDependencies": {
        "@esbuild/aix-ppc64": "0.21.5",
        "@esbuild/android-arm": "0.21.5",
        "@esbuild/android-arm64": "0.21.5",
        "@esbuild/android-x64": "0.21.5",
        "@esbuild/darwin-arm64": "0.21.5",
        "@esbuild/darwin-x64": "0.21.5",
        "@esbuild/freebsd-arm64": "0.21.5",
        "@esbuild/freebsd-x64": "0.21.5",
        "@esbuild/linux-arm": "0.21.5",
        "@esbuild/linux-arm64": "0.21.5",
        "@esbuild/linux-ia32": "0.21.5",
        "@esbuild/linux-loong64": "0.21.5",
        "@esbuild/linux-mips64el": "0.21.5",
        "@esbuild/linux-ppc64": "0.21.5",
        "@esbuild/linux-riscv64": "0.21.5",
        "@esbuild/linux-s390x": "0.21.5",
        "@esbuild/linux-x64": "0.21.5",
        "@esbuild/netbsd-x64": "0.21.5",
        "@esbuild/openbsd-x64": "0.21.5",
        "@esbuild/sunos-x64": "0.21.5",
        "@esbuild/win32-arm64": "0.21.5",
        "@esbuild/win32-ia32": "0.21.5",
        "@esbuild/win32-x64": "0.21.5"
      }
    },
    "node_modules/escalade": {
      "version": "3.2.0",
      "resolved": "https://registry.npmjs.org/escalade/-/escalade-3.2.0.tgz",
      "integrity": "sha512-WUj2qlxaQtO4g6Pq5c29GTcWGDyd8itL8zTlipgECz3JesAiiOKotd8JU6otB3PACgG6xkJUyVhboMS+bje/jA==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/escape-string-regexp": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/escape-string-regexp/-/escape-string-regexp-4.0.0.tgz",
      "integrity": "sha512-TtpcNJ3XAzx3Gq8sWRzJaVajRs0uVxA2YAkdb1jm2YkPz4G6egUFAyA3n5vtEIZefPk5Wa4UXbKuS5fKkJWdgA==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/eventemitter3": {
      "version": "4.0.7",
      "resolved": "https://registry.npmjs.org/eventemitter3/-/eventemitter3-4.0.7.tgz",
      "integrity": "sha512-8guHBZCwKnFhYdHr2ysuRWErTwhoN2X8XELRlrRwpmfeY2jjuUN4taQMsULKUVo1K4DvZl+0pgfyoysHxvmvEw==",
      "license": "MIT"
    },
    "node_modules/fast-equals": {
      "version": "5.4.3",
      "resolved": "https://registry.npmjs.org/fast-equals/-/fast-equals-5.4.3.tgz",
      "integrity": "sha512-8unmvA0qrfpFWBYUate9BTGtQdKHWBYt+KdAIkag7Vvxe7wz8Q2nJg7fLMC0bJqe0bjP31kca7Ckaawrs4Istg==",
      "license": "MIT",
      "engines": {
        "node": ">=6.0.0"
      }
    },
    "node_modules/find-root": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/find-root/-/find-root-1.1.0.tgz",
      "integrity": "sha512-NKfW6bec6GfKc0SGx1e07QZY9PE99u0Bft/0rzSD5k3sO/vwkVUpDUKVm5Gpp5Ue3YfShPFTX2070tDs5kB9Ng==",
      "license": "MIT"
    },
    "node_modules/follow-redirects": {
      "version": "1.16.0",
      "resolved": "https://registry.npmjs.org/follow-redirects/-/follow-redirects-1.16.0.tgz",
      "integrity": "sha512-y5rN/uOsadFT/JfYwhxRS5R7Qce+g3zG97+JrtFZlC9klX/W5hD7iiLzScI4nZqUS7DNUdhPgw4xI8W2LuXlUw==",
      "funding": [
        {
          "type": "individual",
          "url": "https://github.com/sponsors/RubenVerborgh"
        }
      ],
      "license": "MIT",
      "engines": {
        "node": ">=4.0"
      },
      "peerDependenciesMeta": {
        "debug": {
          "optional": true
        }
      }
    },
    "node_modules/form-data": {
      "version": "4.0.6",
      "resolved": "https://registry.npmjs.org/form-data/-/form-data-4.0.6.tgz",
      "integrity": "sha512-vKatAh4SlVfgbv+YtmhiRjhEMJsYpsG1Y2rMQtR+SVSbytsSD1YGzDIcrAJmdFec88u/+VoGmxnl+80gL1tRCQ==",
      "license": "MIT",
      "dependencies": {
        "asynckit": "^0.4.0",
        "combined-stream": "^1.0.8",
        "es-set-tostringtag": "^2.1.0",
        "hasown": "^2.0.4",
        "mime-types": "^2.1.35"
      },
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/fsevents": {
      "version": "2.3.3",
      "resolved": "https://registry.npmjs.org/fsevents/-/fsevents-2.3.3.tgz",
      "integrity": "sha512-5xoDfX+fL7faATnagmWPpbFtwh/R77WmMMqqHGS65C3vvB0YHrgF+B1YmZ3441tMj5n63k0212XNoJwzlhffQw==",
      "dev": true,
      "hasInstallScript": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "darwin"
      ],
      "engines": {
        "node": "^8.16.0 || ^10.6.0 || >=11.0.0"
      }
    },
    "node_modules/function-bind": {
      "version": "1.1.2",
      "resolved": "https://registry.npmjs.org/function-bind/-/function-bind-1.1.2.tgz",
      "integrity": "sha512-7XHNxH7qX9xG5mIwxkhumTox/MIRNcOgDrxWsMt2pAr23WHp6MrRlN7FBSFpCpr+oVO0F744iUgR82nJMfG2SA==",
      "license": "MIT",
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/gensync": {
      "version": "1.0.0-beta.2",
      "resolved": "https://registry.npmjs.org/gensync/-/gensync-1.0.0-beta.2.tgz",
      "integrity": "sha512-3hN7NaskYvMDLQY55gnW3NQ+mesEAepTqlg+VEbj7zzqEMBVNhzcGYYeqFo/TlYz6eQiFcp1HcsCZO+nGgS8zg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/get-intrinsic": {
      "version": "1.3.0",
      "resolved": "https://registry.npmjs.org/get-intrinsic/-/get-intrinsic-1.3.0.tgz",
      "integrity": "sha512-9fSjSaos/fRIVIp+xSJlE6lfwhES7LNtKaCBIamHsjr2na1BiABJPo0mOjjz8GJDURarmCPGqaiVg5mfjb98CQ==",
      "license": "MIT",
      "dependencies": {
        "call-bind-apply-helpers": "^1.0.2",
        "es-define-property": "^1.0.1",
        "es-errors": "^1.3.0",
        "es-object-atoms": "^1.1.1",
        "function-bind": "^1.1.2",
        "get-proto": "^1.0.1",
        "gopd": "^1.2.0",
        "has-symbols": "^1.1.0",
        "hasown": "^2.0.2",
        "math-intrinsics": "^1.1.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/get-proto": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/get-proto/-/get-proto-1.0.1.tgz",
      "integrity": "sha512-sTSfBjoXBp89JvIKIefqw7U2CCebsc74kiY6awiGogKtoSGbgjYE/G/+l9sF3MWFPNc9IcoOC4ODfKHfxFmp0g==",
      "license": "MIT",
      "dependencies": {
        "dunder-proto": "^1.0.1",
        "es-object-atoms": "^1.0.0"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/gopd": {
      "version": "1.2.0",
      "resolved": "https://registry.npmjs.org/gopd/-/gopd-1.2.0.tgz",
      "integrity": "sha512-ZUKRh6/kUFoAiTAtTYPZJ3hw9wNxx+BIBOijnlG9PnrJsCcSjs1wyyD6vJpaYtgnzDrKYRSqf3OO6Rfa93xsRg==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/has-symbols": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/has-symbols/-/has-symbols-1.1.0.tgz",
      "integrity": "sha512-1cDNdwJ2Jaohmb3sg4OmKaMBwuC48sYni5HUw2DvsC8LjGTLK9h+eb1X6RyuOHe4hT0ULCW68iomhjUoKUqlPQ==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/has-tostringtag": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/has-tostringtag/-/has-tostringtag-1.0.2.tgz",
      "integrity": "sha512-NqADB8VjPFLM2V0VvHUewwwsw0ZWBaIdgo+ieHtK3hasLz4qeCRjYcqfB6AQrBggRKppKF8L52/VqdVsO47Dlw==",
      "license": "MIT",
      "dependencies": {
        "has-symbols": "^1.0.3"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/hasown": {
      "version": "2.0.4",
      "resolved": "https://registry.npmjs.org/hasown/-/hasown-2.0.4.tgz",
      "integrity": "sha512-T2UbfbBEF32wiepXIsMlTW9+dDYC6wMh/t/vYA4tuOMKqWz/n3vr1NFSxQiyP+zk2mXsoMA/i/7qV6LKut1t1A==",
      "license": "MIT",
      "dependencies": {
        "function-bind": "^1.1.2"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/hoist-non-react-statics": {
      "version": "3.3.2",
      "resolved": "https://registry.npmjs.org/hoist-non-react-statics/-/hoist-non-react-statics-3.3.2.tgz",
      "integrity": "sha512-/gGivxi8JPKWNm/W0jSmzcMPpfpPLc3dY/6GxhX2hQ9iGj3aDfklV4ET7NjKpSinLpJ5vafa9iiGIEZg10SfBw==",
      "license": "BSD-3-Clause",
      "dependencies": {
        "react-is": "^16.7.0"
      }
    },
    "node_modules/hoist-non-react-statics/node_modules/react-is": {
      "version": "16.13.1",
      "resolved": "https://registry.npmjs.org/react-is/-/react-is-16.13.1.tgz",
      "integrity": "sha512-24e6ynE2H+OKt4kqsOvNd8kBpV65zoxbA4BVsEOB3ARVWQki/DHzaUoC5KuON/BiccDaCCTZBuOcfZs70kR8bQ==",
      "license": "MIT"
    },
    "node_modules/https-proxy-agent": {
      "version": "5.0.1",
      "resolved": "https://registry.npmjs.org/https-proxy-agent/-/https-proxy-agent-5.0.1.tgz",
      "integrity": "sha512-dFcAjpTQFgoLMzC2VwU+C/CbS7uRL0lWmxDITmqm7C+7F0Odmj6s9l6alZc6AELXhrnggM2CeWSXHGOdX2YtwA==",
      "license": "MIT",
      "dependencies": {
        "agent-base": "6",
        "debug": "4"
      },
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/import-fresh": {
      "version": "3.3.1",
      "resolved": "https://registry.npmjs.org/import-fresh/-/import-fresh-3.3.1.tgz",
      "integrity": "sha512-TR3KfrTZTYLPB6jUjfx6MF9WcWrHL9su5TObK4ZkYgBdWKPOFoSoQIdEuTuR82pmtxH2spWG9h6etwfr1pLBqQ==",
      "license": "MIT",
      "dependencies": {
        "parent-module": "^1.0.0",
        "resolve-from": "^4.0.0"
      },
      "engines": {
        "node": ">=6"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/internmap": {
      "version": "2.0.3",
      "resolved": "https://registry.npmjs.org/internmap/-/internmap-2.0.3.tgz",
      "integrity": "sha512-5Hh7Y1wQbvY5ooGgPbDaL5iYLAPzMTUrjMulskHLH6wnv/A+1q5rgEaiuqEjB+oxGXIVZs1FF+R/KPN3ZSQYYg==",
      "license": "ISC",
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/is-arrayish": {
      "version": "0.2.1",
      "resolved": "https://registry.npmjs.org/is-arrayish/-/is-arrayish-0.2.1.tgz",
      "integrity": "sha512-zz06S8t0ozoDXMG+ube26zeCTNXcKIPJZJi8hBrF4idCLms4CG9QtK7qBl1boi5ODzFpjswb5JPmHCbMpjaYzg==",
      "license": "MIT"
    },
    "node_modules/is-core-module": {
      "version": "2.17.0",
      "resolved": "https://registry.npmjs.org/is-core-module/-/is-core-module-2.17.0.tgz",
      "integrity": "sha512-J/vG0zBCbIKOQFfufSwyXdMrsohyJIUNkrnmo6WZGzoM7tr/lsbfW5b2BvisL6zsyMzK9UxV9L6c7AoFbyXHOA==",
      "license": "MIT",
      "dependencies": {
        "hasown": "^2.0.4"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/js-tokens": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/js-tokens/-/js-tokens-4.0.0.tgz",
      "integrity": "sha512-RdJUflcE3cUzKiMqQgsCu06FPu9UdIJO0beYbPhHN4k6apgJtifcoCtT9bcxOpYBtpD2kCM6Sbzg4CausW/PKQ==",
      "license": "MIT"
    },
    "node_modules/jsesc": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/jsesc/-/jsesc-3.1.0.tgz",
      "integrity": "sha512-/sM3dO2FOzXjKQhJuo0Q173wf2KOo8t4I8vHy6lF9poUp7bKT0/NHE8fPX23PwfhnykfqnC2xRxOnVw5XuGIaA==",
      "license": "MIT",
      "bin": {
        "jsesc": "bin/jsesc"
      },
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/json-parse-even-better-errors": {
      "version": "2.3.1",
      "resolved": "https://registry.npmjs.org/json-parse-even-better-errors/-/json-parse-even-better-errors-2.3.1.tgz",
      "integrity": "sha512-xyFwyhro/JEof6Ghe2iz2NcXoj2sloNsWr/XsERDK/oiPCfaNhl5ONfp+jQdAZRQQ0IJWNzH9zIZF7li91kh2w==",
      "license": "MIT"
    },
    "node_modules/json5": {
      "version": "2.2.3",
      "resolved": "https://registry.npmjs.org/json5/-/json5-2.2.3.tgz",
      "integrity": "sha512-XmOWe7eyHYH14cLdVPoyg+GOH3rYX++KpzrylJwSW98t3Nk+U8XOl8FWKOgwtzdb8lXGf6zYwDUzeHMWfxasyg==",
      "dev": true,
      "license": "MIT",
      "bin": {
        "json5": "lib/cli.js"
      },
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/lines-and-columns": {
      "version": "1.2.4",
      "resolved": "https://registry.npmjs.org/lines-and-columns/-/lines-and-columns-1.2.4.tgz",
      "integrity": "sha512-7ylylesZQ/PV29jhEDl3Ufjo6ZX7gCqJr5F7PKrqc93v7fzSymt1BpwEU8nAUXs8qzzvqhbjhK5QZg6Mt/HkBg==",
      "license": "MIT"
    },
    "node_modules/lodash": {
      "version": "4.18.1",
      "resolved": "https://registry.npmjs.org/lodash/-/lodash-4.18.1.tgz",
      "integrity": "sha512-dMInicTPVE8d1e5otfwmmjlxkZoUpiVLwyeTdUsi/Caj/gfzzblBcCE5sRHV/AsjuCmxWrte2TNGSYuCeCq+0Q==",
      "license": "MIT"
    },
    "node_modules/loose-envify": {
      "version": "1.4.0",
      "resolved": "https://registry.npmjs.org/loose-envify/-/loose-envify-1.4.0.tgz",
      "integrity": "sha512-lyuxPGr/Wfhrlem2CL/UcnUc1zcqKAImBDzukY7Y5F/yQiNdko6+fRLevlw1HgMySw7f611UIY408EtxRSoK3Q==",
      "license": "MIT",
      "dependencies": {
        "js-tokens": "^3.0.0 || ^4.0.0"
      },
      "bin": {
        "loose-envify": "cli.js"
      }
    },
    "node_modules/lru-cache": {
      "version": "5.1.1",
      "resolved": "https://registry.npmjs.org/lru-cache/-/lru-cache-5.1.1.tgz",
      "integrity": "sha512-KpNARQA3Iwv+jTA0utUVVbrh+Jlrr1Fv0e56GGzAFOXN7dk/FviaDW8LHmK52DlcH4WP2n6gI8vN1aesBFgo9w==",
      "dev": true,
      "license": "ISC",
      "dependencies": {
        "yallist": "^3.0.2"
      }
    },
    "node_modules/math-intrinsics": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/math-intrinsics/-/math-intrinsics-1.1.0.tgz",
      "integrity": "sha512-/IXtbwEk5HTPyEwyKX6hGkYXxM9nbj64B+ilVJnC/R6B0pH5G4V3b0pVbL7DBj4tkhBAppbQUlf6F6Xl9LHu1g==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/mime-db": {
      "version": "1.52.0",
      "resolved": "https://registry.npmjs.org/mime-db/-/mime-db-1.52.0.tgz",
      "integrity": "sha512-sPU4uV7dYlvtWJxwwxHD0PuihVNiE7TyAbQ5SWxDCB9mUYvOgroQOwYQQOKPJ8CIbE+1ETVlOoK1UC2nU3gYvg==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/mime-types": {
      "version": "2.1.35",
      "resolved": "https://registry.npmjs.org/mime-types/-/mime-types-2.1.35.tgz",
      "integrity": "sha512-ZDY+bPm5zTTF+YpCrAU9nK0UgICYPT0QtT1NZWFv4s++TNkcgVaT0g6+4R2uI4MjQjzysHB1zxuWL50hzaeXiw==",
      "license": "MIT",
      "dependencies": {
        "mime-db": "1.52.0"
      },
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/ms": {
      "version": "2.1.3",
      "resolved": "https://registry.npmjs.org/ms/-/ms-2.1.3.tgz",
      "integrity": "sha512-6FlzubTLZG3J2a/NVCAleEhjzq5oxgHyaCU9yYXvcLsvoVaHJq/s5xXI6/XXP6tz7R9xAOtHnSO/tXtF3WRTlA==",
      "license": "MIT"
    },
    "node_modules/nanoid": {
      "version": "3.3.19",
      "resolved": "https://registry.npmjs.org/nanoid/-/nanoid-3.3.19.tgz",
      "integrity": "sha512-Y2tUNy4ouw6tq5oDSKeQYGOyhkUBhNOcGV/02KC+6kd9eDGqdZd++mjMiIDilrBYvjEnCYvVtsuHCuP+okSfug==",
      "dev": true,
      "funding": [
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "MIT",
      "bin": {
        "nanoid": "bin/nanoid.cjs"
      },
      "engines": {
        "node": "^10 || ^12 || ^13.7 || ^14 || >=15.0.1"
      }
    },
    "node_modules/node-releases": {
      "version": "2.0.56",
      "resolved": "https://registry.npmjs.org/node-releases/-/node-releases-2.0.56.tgz",
      "integrity": "sha512-x0InOIyzgdk+eyaWaRJFH5snEtiImgBgblZ2CyPrLmqqcuMQkEvcDPHbzqbD8eDsSeJbVOjn+crzyzHaM4D+/A==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/object-assign": {
      "version": "4.1.1",
      "resolved": "https://registry.npmjs.org/object-assign/-/object-assign-4.1.1.tgz",
      "integrity": "sha512-rJgTQnkUnH1sFw8yT6VSU3zD3sWmu6sZhIseY8VX+GRu3P6F7Fu+JNDoXfklElbLJSnc3FUQHVe4cU5hj+BcUg==",
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/parent-module": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/parent-module/-/parent-module-1.0.1.tgz",
      "integrity": "sha512-GQ2EWRpQV8/o+Aw8YqtfZZPfNRWZYkbidE9k5rpl/hC3vtHHBfGm2Ifi6qWV+coDGkrUKZAxE3Lot5kcsRlh+g==",
      "license": "MIT",
      "dependencies": {
        "callsites": "^3.0.0"
      },
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/parse-json": {
      "version": "5.2.0",
      "resolved": "https://registry.npmjs.org/parse-json/-/parse-json-5.2.0.tgz",
      "integrity": "sha512-ayCKvm/phCGxOkYRSCM82iDwct8/EonSEgCSxWxD7ve6jHggsFl4fZVQBPRNgQoKiuV/odhFrGzQXZwbifC8Rg==",
      "license": "MIT",
      "dependencies": {
        "@babel/code-frame": "^7.0.0",
        "error-ex": "^1.3.1",
        "json-parse-even-better-errors": "^2.3.0",
        "lines-and-columns": "^1.1.6"
      },
      "engines": {
        "node": ">=8"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/path-parse": {
      "version": "1.0.7",
      "resolved": "https://registry.npmjs.org/path-parse/-/path-parse-1.0.7.tgz",
      "integrity": "sha512-LDJzPVEEEPR+y48z93A0Ed0yXb8pAByGWo/k5YYdYgpY2/2EsOsksJrq7lOHxryrVOn1ejG6oAp8ahvOIQD8sw==",
      "license": "MIT"
    },
    "node_modules/path-type": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/path-type/-/path-type-4.0.0.tgz",
      "integrity": "sha512-gDKb8aZMDeD/tZWs9P6+q0J9Mwkdl6xMV8TjnGP3qJVJ06bdMgkbBlLU8IdfOsIsFz2BW1rNVT3XuNEl8zPAvw==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/picocolors": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/picocolors/-/picocolors-1.1.1.tgz",
      "integrity": "sha512-xceH2snhtb5M9liqDsmEw56le376mTZkEX/jEb/RxNFyegNul7eNslCXP9FDj/Lcu0X8KEyMceP2ntpaHrDEVA==",
      "license": "ISC"
    },
    "node_modules/postcss": {
      "version": "8.5.28",
      "resolved": "https://registry.npmjs.org/postcss/-/postcss-8.5.28.tgz",
      "integrity": "sha512-RRuzqDtt5Y9h3quz5hWhK+TPnsmVs6WwSU6LkJMeY4HstUEDuYTG8UJSdawMRzmzAtV+KEoG8N3Qg2qLy5vM/A==",
      "dev": true,
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/postcss/"
        },
        {
          "type": "tidelift",
          "url": "https://tidelift.com/funding/github/npm/postcss"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "MIT",
      "dependencies": {
        "nanoid": "^3.3.18",
        "picocolors": "^1.1.1",
        "source-map-js": "^1.2.1"
      },
      "engines": {
        "node": "^10 || ^12 || >=14"
      }
    },
    "node_modules/prop-types": {
      "version": "15.8.1",
      "resolved": "https://registry.npmjs.org/prop-types/-/prop-types-15.8.1.tgz",
      "integrity": "sha512-oj87CgZICdulUohogVAR7AjlC0327U4el4L6eAvOqCeudMDVU0NThNaV+b9Df4dXgSP1gXMTnPdhfe/2qDH5cg==",
      "license": "MIT",
      "dependencies": {
        "loose-envify": "^1.4.0",
        "object-assign": "^4.1.1",
        "react-is": "^16.13.1"
      }
    },
    "node_modules/prop-types/node_modules/react-is": {
      "version": "16.13.1",
      "resolved": "https://registry.npmjs.org/react-is/-/react-is-16.13.1.tgz",
      "integrity": "sha512-24e6ynE2H+OKt4kqsOvNd8kBpV65zoxbA4BVsEOB3ARVWQki/DHzaUoC5KuON/BiccDaCCTZBuOcfZs70kR8bQ==",
      "license": "MIT"
    },
    "node_modules/proxy-from-env": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/proxy-from-env/-/proxy-from-env-2.1.0.tgz",
      "integrity": "sha512-cJ+oHTW1VAEa8cJslgmUZrc+sjRKgAKl3Zyse6+PV38hZe/V6Z14TbCuXcan9F9ghlz4QrFr2c92TNF82UkYHA==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/react": {
      "version": "18.3.1",
      "resolved": "https://registry.npmjs.org/react/-/react-18.3.1.tgz",
      "integrity": "sha512-wS+hAgJShR0KhEvPJArfuPVN1+Hz1t0Y6n5jLrGQbkb4urgPE/0Rve+1kMB1v/oWgHgm4WIcV+i7F2pTVj+2iQ==",
      "license": "MIT",
      "dependencies": {
        "loose-envify": "^1.1.0"
      },
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/react-dom": {
      "version": "18.3.1",
      "resolved": "https://registry.npmjs.org/react-dom/-/react-dom-18.3.1.tgz",
      "integrity": "sha512-5m4nQKp+rZRb09LNH59GM4BxTh9251/ylbKIbpe7TpGxfJ+9kv6BLkLBXIjjspbgbnIBNqlI23tRnTWT0snUIw==",
      "license": "MIT",
      "dependencies": {
        "loose-envify": "^1.1.0",
        "scheduler": "^0.23.2"
      },
      "peerDependencies": {
        "react": "^18.3.1"
      }
    },
    "node_modules/react-icons": {
      "version": "5.7.0",
      "resolved": "https://registry.npmjs.org/react-icons/-/react-icons-5.7.0.tgz",
      "integrity": "sha512-LBLy340Rzqy6+/yVhZKT3B/QpP1BZaesGqasf09HPOBzRarcDIFH0WwXlXQfE7q7ipxK4MSiC5DIBWURCny6fw==",
      "license": "MIT",
      "peerDependencies": {
        "react": "*"
      }
    },
    "node_modules/react-is": {
      "version": "19.3.0",
      "resolved": "https://registry.npmjs.org/react-is/-/react-is-19.3.0.tgz",
      "integrity": "sha512-UpMYezM4v5/18F28aC66AEsjXIgE02kyEMH6yLdgLXu/UTfa1Ntwck/nNLrbqJsEXW7gPb0coNO9FQse9WTovA==",
      "license": "MIT"
    },
    "node_modules/react-refresh": {
      "version": "0.17.0",
      "resolved": "https://registry.npmjs.org/react-refresh/-/react-refresh-0.17.0.tgz",
      "integrity": "sha512-z6F7K9bV85EfseRCp2bzrpyQ0Gkw1uLoCel9XBVWPg/TjRj94SkJzUTGfOa4bs7iJvBWtQG0Wq7wnI0syw3EBQ==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/react-router": {
      "version": "6.30.6",
      "resolved": "https://registry.npmjs.org/react-router/-/react-router-6.30.6.tgz",
      "integrity": "sha512-5HfK7k5im7LTOB0EqCQmfvy4C13G92Ssj1VTmouTK3AJvyjKTnFuCV0vcMAD/JS+JC4DvDIBRrlAeJIFjh5VWg==",
      "license": "MIT",
      "dependencies": {
        "@remix-run/router": "1.23.4"
      },
      "engines": {
        "node": ">=14.0.0"
      },
      "peerDependencies": {
        "react": ">=16.8"
      }
    },
    "node_modules/react-router-dom": {
      "version": "6.30.6",
      "resolved": "https://registry.npmjs.org/react-router-dom/-/react-router-dom-6.30.6.tgz",
      "integrity": "sha512-0RHKZz7wwffvkU+2MFVT2NnjK44ssLEV+m0CAJaS2Ksmorrwj7WxH00jO0SOCW26/tINUnJHToXblDs33I38YQ==",
      "license": "MIT",
      "dependencies": {
        "@remix-run/router": "1.23.4",
        "react-router": "6.30.6"
      },
      "engines": {
        "node": ">=14.0.0"
      },
      "peerDependencies": {
        "react": ">=16.8",
        "react-dom": ">=16.8"
      }
    },
    "node_modules/react-smooth": {
      "version": "4.0.4",
      "resolved": "https://registry.npmjs.org/react-smooth/-/react-smooth-4.0.4.tgz",
      "integrity": "sha512-gnGKTpYwqL0Iii09gHobNolvX4Kiq4PKx6eWBCYYix+8cdw+cGo3do906l1NBPKkSWx1DghC1dlWG9L2uGd61Q==",
      "license": "MIT",
      "dependencies": {
        "fast-equals": "^5.0.1",
        "prop-types": "^15.8.1",
        "react-transition-group": "^4.4.5"
      },
      "peerDependencies": {
        "react": "^16.8.0 || ^17.0.0 || ^18.0.0 || ^19.0.0",
        "react-dom": "^16.8.0 || ^17.0.0 || ^18.0.0 || ^19.0.0"
      }
    },
    "node_modules/react-transition-group": {
      "version": "4.4.5",
      "resolved": "https://registry.npmjs.org/react-transition-group/-/react-transition-group-4.4.5.tgz",
      "integrity": "sha512-pZcd1MCJoiKiBR2NRxeCRg13uCXbydPnmB4EOeRrY7480qNWO8IIgQG6zlDkm6uRMsURXPuKq0GWtiM59a5Q6g==",
      "license": "BSD-3-Clause",
      "dependencies": {
        "@babel/runtime": "^7.5.5",
        "dom-helpers": "^5.0.1",
        "loose-envify": "^1.4.0",
        "prop-types": "^15.6.2"
      },
      "peerDependencies": {
        "react": ">=16.6.0",
        "react-dom": ">=16.6.0"
      }
    },
    "node_modules/recharts": {
      "version": "2.15.4",
      "resolved": "https://registry.npmjs.org/recharts/-/recharts-2.15.4.tgz",
      "integrity": "sha512-UT/q6fwS3c1dHbXv2uFgYJ9BMFHu3fwnd7AYZaEQhXuYQ4hgsxLvsUXzGdKeZrW5xopzDCvuA2N41WJ88I7zIw==",
      "deprecated": "1.x and 2.x branches are no longer active. Bump to Recharts v3 to receive latest features and bugfixes. See https://github.com/recharts/recharts/wiki/3.0-migration-guide",
      "license": "MIT",
      "dependencies": {
        "clsx": "^2.0.0",
        "eventemitter3": "^4.0.1",
        "lodash": "^4.17.21",
        "react-is": "^18.3.1",
        "react-smooth": "^4.0.4",
        "recharts-scale": "^0.4.4",
        "tiny-invariant": "^1.3.1",
        "victory-vendor": "^36.6.8"
      },
      "engines": {
        "node": ">=14"
      },
      "peerDependencies": {
        "react": "^16.0.0 || ^17.0.0 || ^18.0.0 || ^19.0.0",
        "react-dom": "^16.0.0 || ^17.0.0 || ^18.0.0 || ^19.0.0"
      }
    },
    "node_modules/recharts-scale": {
      "version": "0.4.5",
      "resolved": "https://registry.npmjs.org/recharts-scale/-/recharts-scale-0.4.5.tgz",
      "integrity": "sha512-kivNFO+0OcUNu7jQquLXAxz1FIwZj8nrj+YkOKc5694NbjCvcT6aSZiIzNzd2Kul4o4rTto8QVR9lMNtxD4G1w==",
      "license": "MIT",
      "dependencies": {
        "decimal.js-light": "^2.4.1"
      }
    },
    "node_modules/recharts/node_modules/react-is": {
      "version": "18.3.1",
      "resolved": "https://registry.npmjs.org/react-is/-/react-is-18.3.1.tgz",
      "integrity": "sha512-/LLMVyas0ljjAtoYiPqYiL8VWXzUUdThrmU5+n20DZv+a+ClRoevUzw5JxU+Ieh5/c87ytoTBV9G1FiKfNJdmg==",
      "license": "MIT"
    },
    "node_modules/resolve": {
      "version": "1.22.12",
      "resolved": "https://registry.npmjs.org/resolve/-/resolve-1.22.12.tgz",
      "integrity": "sha512-TyeJ1zif53BPfHootBGwPRYT1RUt6oGWsaQr8UyZW/eAm9bKoijtvruSDEmZHm92CwS9nj7/fWttqPCgzep8CA==",
      "license": "MIT",
      "dependencies": {
        "es-errors": "^1.3.0",
        "is-core-module": "^2.16.1",
        "path-parse": "^1.0.7",
        "supports-preserve-symlinks-flag": "^1.0.0"
      },
      "bin": {
        "resolve": "bin/resolve"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/resolve-from": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/resolve-from/-/resolve-from-4.0.0.tgz",
      "integrity": "sha512-pb/MYmXstAkysRFx8piNI1tGFNQIFA3vkE3Gq4EuA1dF6gHp/+vgZqsCGJapvy8N3Q+4o7FwvquPJcnZ7RYy4g==",
      "license": "MIT",
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/rollup": {
      "version": "4.63.4",
      "resolved": "https://registry.npmjs.org/rollup/-/rollup-4.63.4.tgz",
      "integrity": "sha512-4U0liVayNIoLp3GFl1FcI8561WepLnZ1rqfraGh7S9B3Ur5F9S283y8Futii7RUU2C/97tOBmBy7nYvhoiOpbQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@types/estree": "1.0.9"
      },
      "bin": {
        "rollup": "dist/bin/rollup"
      },
      "engines": {
        "node": ">=18.0.0",
        "npm": ">=8.0.0"
      },
      "optionalDependencies": {
        "@napi-rs/lzma-linux-x64-gnu": "1.5.1",
        "@rollup/rollup-android-arm-eabi": "4.63.4",
        "@rollup/rollup-android-arm64": "4.63.4",
        "@rollup/rollup-darwin-arm64": "4.63.4",
        "@rollup/rollup-darwin-x64": "4.63.4",
        "@rollup/rollup-freebsd-arm64": "4.63.4",
        "@rollup/rollup-freebsd-x64": "4.63.4",
        "@rollup/rollup-linux-arm-gnueabihf": "4.63.4",
        "@rollup/rollup-linux-arm-musleabihf": "4.63.4",
        "@rollup/rollup-linux-arm64-gnu": "4.63.4",
        "@rollup/rollup-linux-arm64-musl": "4.63.4",
        "@rollup/rollup-linux-loong64-gnu": "4.63.4",
        "@rollup/rollup-linux-loong64-musl": "4.63.4",
        "@rollup/rollup-linux-ppc64-gnu": "4.63.4",
        "@rollup/rollup-linux-ppc64-musl": "4.63.4",
        "@rollup/rollup-linux-riscv64-gnu": "4.63.4",
        "@rollup/rollup-linux-riscv64-musl": "4.63.4",
        "@rollup/rollup-linux-s390x-gnu": "4.63.4",
        "@rollup/rollup-linux-x64-gnu": "4.63.4",
        "@rollup/rollup-linux-x64-musl": "4.63.4",
        "@rollup/rollup-openbsd-x64": "4.63.4",
        "@rollup/rollup-openharmony-arm64": "4.63.4",
        "@rollup/rollup-win32-arm64-msvc": "4.63.4",
        "@rollup/rollup-win32-ia32-msvc": "4.63.4",
        "@rollup/rollup-win32-x64-gnu": "4.63.4",
        "@rollup/rollup-win32-x64-msvc": "4.63.4",
        "fsevents": "~2.3.2"
      }
    },
    "node_modules/scheduler": {
      "version": "0.23.2",
      "resolved": "https://registry.npmjs.org/scheduler/-/scheduler-0.23.2.tgz",
      "integrity": "sha512-UOShsPwz7NrMUqhR6t0hWjFduvOzbtv7toDH1/hIrfRNIDBnnBWd0CwJTGvTpngVlmwGCdP9/Zl/tVrDqcuYzQ==",
      "license": "MIT",
      "dependencies": {
        "loose-envify": "^1.1.0"
      }
    },
    "node_modules/semver": {
      "version": "6.3.1",
      "resolved": "https://registry.npmjs.org/semver/-/semver-6.3.1.tgz",
      "integrity": "sha512-BR7VvDCVHO+q2xBEWskxS6DJE1qRnb7DxzUrogb71CWoSficBxYsiAGd+Kl0mmq/MprG9yArRkyrQxTO6XjMzA==",
      "dev": true,
      "license": "ISC",
      "bin": {
        "semver": "bin/semver.js"
      }
    },
    "node_modules/source-map": {
      "version": "0.5.7",
      "resolved": "https://registry.npmjs.org/source-map/-/source-map-0.5.7.tgz",
      "integrity": "sha512-LbrmJOMUSdEVxIKvdcJzQC+nQhe8FUZQTXQy6+I75skNgn3OoQ0DZA8YnFa7gp8tqtL3KPf1kmo0R5DoApeSGQ==",
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/source-map-js": {
      "version": "1.2.1",
      "resolved": "https://registry.npmjs.org/source-map-js/-/source-map-js-1.2.1.tgz",
      "integrity": "sha512-UXWMKhLOwVKb728IUtQPXxfYU+usdybtUrK/8uGE8CQMvrhOpwvzDBwj0QhSL7MQc7vIsISBG8VQ8+IDQxpfQA==",
      "dev": true,
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/stylis": {
      "version": "4.2.0",
      "resolved": "https://registry.npmjs.org/stylis/-/stylis-4.2.0.tgz",
      "integrity": "sha512-Orov6g6BB1sDfYgzWfTHDOxamtX1bE/zo104Dh9e6fqJ3PooipYyfJ0pUmrZO2wAvO8YbEyeFrkV91XTsGMSrw==",
      "license": "MIT"
    },
    "node_modules/supports-preserve-symlinks-flag": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/supports-preserve-symlinks-flag/-/supports-preserve-symlinks-flag-1.0.0.tgz",
      "integrity": "sha512-ot0WnXS9fgdkgIcePe6RHNk1WA8+muPa6cSjeR3V8K27q9BB1rTE3R1p7Hv0z1ZyAc8s6Vvv8DIyWf681MAt0w==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/tiny-invariant": {
      "version": "1.3.3",
      "resolved": "https://registry.npmjs.org/tiny-invariant/-/tiny-invariant-1.3.3.tgz",
      "integrity": "sha512-+FbBPE1o9QAYvviau/qC5SE3caw21q3xkvWKBtja5vgqOWIHHJ3ioaq1VPfn/Szqctz2bU/oYeKd9/z5BL+PVg==",
      "license": "MIT"
    },
    "node_modules/update-browserslist-db": {
      "version": "1.3.3",
      "resolved": "https://registry.npmjs.org/update-browserslist-db/-/update-browserslist-db-1.3.3.tgz",
      "integrity": "sha512-pJ2sYawQS0R/WI928Gj5GlPhTGzbMelq0+4INtSYNDV9ErKJcX6xjGWkoG/VnB3dpUm00zALaqkrUD77pO5TDQ==",
      "dev": true,
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/browserslist"
        },
        {
          "type": "tidelift",
          "url": "https://tidelift.com/funding/github/npm/browserslist"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "MIT",
      "dependencies": {
        "escalade": "^3.2.0",
        "picocolors": "^1.1.1"
      },
      "bin": {
        "update-browserslist-db": "cli.js"
      },
      "peerDependencies": {
        "browserslist": ">= 4.21.0"
      }
    },
    "node_modules/victory-vendor": {
      "version": "36.9.2",
      "resolved": "https://registry.npmjs.org/victory-vendor/-/victory-vendor-36.9.2.tgz",
      "integrity": "sha512-PnpQQMuxlwYdocC8fIJqVXvkeViHYzotI+NJrCuav0ZYFoq912ZHBk3mCeuj+5/VpodOjPe1z0Fk2ihgzlXqjQ==",
      "license": "MIT AND ISC",
      "dependencies": {
        "@types/d3-array": "^3.0.3",
        "@types/d3-ease": "^3.0.0",
        "@types/d3-interpolate": "^3.0.1",
        "@types/d3-scale": "^4.0.2",
        "@types/d3-shape": "^3.1.0",
        "@types/d3-time": "^3.0.0",
        "@types/d3-timer": "^3.0.0",
        "d3-array": "^3.1.6",
        "d3-ease": "^3.0.1",
        "d3-interpolate": "^3.0.1",
        "d3-scale": "^4.0.2",
        "d3-shape": "^3.1.0",
        "d3-time": "^3.0.0",
        "d3-timer": "^3.0.1"
      }
    },
    "node_modules/vite": {
      "version": "5.4.21",
      "resolved": "https://registry.npmjs.org/vite/-/vite-5.4.21.tgz",
      "integrity": "sha512-o5a9xKjbtuhY6Bi5S3+HvbRERmouabWbyUcpXXUA1u+GNUKoROi9byOJ8M0nHbHYHkYICiMlqxkg1KkYmm25Sw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "esbuild": "^0.21.3",
        "postcss": "^8.4.43",
        "rollup": "^4.20.0"
      },
      "bin": {
        "vite": "bin/vite.js"
      },
      "engines": {
        "node": "^18.0.0 || >=20.0.0"
      },
      "funding": {
        "url": "https://github.com/vitejs/vite?sponsor=1"
      },
      "optionalDependencies": {
        "fsevents": "~2.3.3"
      },
      "peerDependencies": {
        "@types/node": "^18.0.0 || >=20.0.0",
        "less": "*",
        "lightningcss": "^1.21.0",
        "sass": "*",
        "sass-embedded": "*",
        "stylus": "*",
        "sugarss": "*",
        "terser": "^5.4.0"
      },
      "peerDependenciesMeta": {
        "@types/node": {
          "optional": true
        },
        "less": {
          "optional": true
        },
        "lightningcss": {
          "optional": true
        },
        "sass": {
          "optional": true
        },
        "sass-embedded": {
          "optional": true
        },
        "stylus": {
          "optional": true
        },
        "sugarss": {
          "optional": true
        },
        "terser": {
          "optional": true
        }
      }
    },
    "node_modules/yallist": {
      "version": "3.1.1",
      "resolved": "https://registry.npmjs.org/yallist/-/yallist-3.1.1.tgz",
      "integrity": "sha512-a4UGQaWPH59mOXUYnAG2ewncQS4i4F43Tv3JoAM+s2VDAmS9NsK8GpDMLrCHPksFT7h3K6TOoUNn2pb7RoXx4g==",
      "dev": true,
      "license": "ISC"
    },
    "node_modules/yaml": {
      "version": "1.10.3",
      "resolved": "https://registry.npmjs.org/yaml/-/yaml-1.10.3.tgz",
      "integrity": "sha512-vIYeF1u3CjlhAFekPPAk2h/Kv4T3mAkMox5OymRiJQB0spDP10LHvt+K7G9Ny6NuuMAb25/6n1qyUjAcGNf/AA==",
      "license": "ISC",
      "engines": {
        "node": ">= 6"
      }
    }
  }
}
```

## Tooling

### tools/build_bankflow_docx.py

```python
#!/usr/bin/env python3
"""Build the BankFlow setup guide DOCX: step-by-step instructions + complete source code.

Usage:
    python build_bankflow_docx.py [page-map.json]

The optional page-map.json is produced by measure_pages.py after the first render and
supplies the real page number for every contents entry. When it is missing the contents
page numbers are omitted, so the document still builds cleanly on the first pass.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import (
    WD_ALIGN_PARAGRAPH,
    WD_LINE_SPACING,
    WD_TAB_ALIGNMENT,
    WD_TAB_LEADER,
)
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

# The project root: override with BANKFLOW_ROOT, otherwise use the parent of tools/.
ROOT = Path(os.environ.get("BANKFLOW_ROOT") or Path(__file__).resolve().parents[1])
OUTPUT = ROOT / "BankFlow-Complete-Setup-Guide-with-Full-Code.docx"

CODE_FONT = "Consolas"
CODE_SIZE = Pt(7.5)
CODE_LINE = Pt(9)
BODY_FONT = "Calibri"
BODY_SIZE = Pt(10.5)

HEADER_FILL = "1B3A8F"
HEADER_TEXT = "FFFFFF"
ROW_TINT = "F4F6FB"
BORDER_GREY = "D9D9D9"


# --------------------------------------------------------------------------- #
# low level docx helpers
# --------------------------------------------------------------------------- #
def black(style, size=None, bold=None):
    style.font.color.rgb = RGBColor(0, 0, 0)
    style.font.name = BODY_FONT
    if size is not None:
        style.font.size = size
    if bold is not None:
        style.font.bold = bold


def strip_paragraph_borders(style):
    ppr = style.element.get_or_add_pPr()
    for border in ppr.findall(qn("w:pBdr")):
        ppr.remove(border)


def configure_styles(doc: Document) -> None:
    normal = doc.styles["Normal"]
    black(normal, BODY_SIZE)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.12

    title = doc.styles["Title"]
    black(title, Pt(24), bold=True)
    strip_paragraph_borders(title)
    title.paragraph_format.space_after = Pt(10)

    h1 = doc.styles["Heading 1"]
    black(h1, Pt(17), bold=True)
    strip_paragraph_borders(h1)
    h1.paragraph_format.space_before = Pt(20)
    h1.paragraph_format.space_after = Pt(8)
    h1.paragraph_format.keep_with_next = True

    h2 = doc.styles["Heading 2"]
    black(h2, Pt(13.5), bold=True)
    strip_paragraph_borders(h2)
    h2.paragraph_format.space_before = Pt(14)
    h2.paragraph_format.space_after = Pt(6)
    h2.paragraph_format.keep_with_next = True

    h3 = doc.styles["Heading 3"]
    black(h3, Pt(11), bold=True)
    strip_paragraph_borders(h3)
    h3.paragraph_format.space_before = Pt(12)
    h3.paragraph_format.space_after = Pt(4)
    h3.paragraph_format.keep_with_next = True

    code = doc.styles.add_style("CodeBlock", 1)  # 1 = paragraph style
    code.base_style = doc.styles["Normal"]
    code.font.name = CODE_FONT
    code.font.size = CODE_SIZE
    code.font.color.rgb = RGBColor(0x11, 0x1A, 0x2E)
    rpr = code.element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attr), CODE_FONT)
    pf = code.paragraph_format
    pf.space_before = Pt(2)
    pf.space_after = Pt(10)
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    pf.line_spacing = CODE_LINE
    pf.left_indent = Cm(0.3)
    pf.keep_together = False

    caption = doc.styles.add_style("FileNote", 1)
    caption.base_style = doc.styles["Normal"]
    caption.font.size = Pt(9.5)
    caption.font.italic = True
    caption.font.color.rgb = RGBColor(0x40, 0x4A, 0x60)
    caption.paragraph_format.space_after = Pt(4)


def page_setup(doc: Document) -> None:
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(1.9)
    section.bottom_margin = Cm(1.9)
    section.left_margin = Cm(1.9)
    section.right_margin = Cm(1.9)

    footer = section.footer
    paragraph = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph.paragraph_format.space_before = Pt(4)
    run = paragraph.add_run()
    run.font.size = Pt(8.5)
    run.font.name = BODY_FONT
    run.font.color.rgb = RGBColor(0x5A, 0x64, 0x78)
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = "PAGE"
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run._r.append(begin)
    run._r.append(instr)
    run._r.append(end)


def shade_cell(cell, fill) -> None:
    tcpr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    tcpr.append(shd)


def set_borders(table, color=BORDER_GREY, size="6") -> None:
    tbl_pr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        element = OxmlElement(f"w:{edge}")
        element.set(qn("w:val"), "single")
        element.set(qn("w:sz"), size)
        element.set(qn("w:space"), "0")
        element.set(qn("w:color"), color)
        borders.append(element)
    tbl_pr.append(borders)


def set_cell_margins(table, top=60, start=90, bottom=60, end=90) -> None:
    tbl_pr = table._tbl.tblPr
    margin = OxmlElement("w:tblCellMar")
    for tag, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        element = OxmlElement(f"w:{tag}")
        element.set(qn("w:w"), str(value))
        element.set(qn("w:type"), "dxa")
        margin.append(element)
    tbl_pr.append(margin)


def repeat_header(row) -> None:
    tr_pr = row._tr.get_or_add_trPr()
    element = OxmlElement("w:tblHeader")
    element.set(qn("w:val"), "true")
    tr_pr.append(element)


def add_code(doc: Document, text: str) -> None:
    """One paragraph per code block; line breaks keep it compact and page-splittable."""
    lines = text.replace("\r\n", "\n").rstrip("\n").split("\n")
    paragraph = doc.add_paragraph(style="CodeBlock")
    run = paragraph.add_run(lines[0])
    for line in lines[1:]:
        run.add_break()
        run.add_text(line)


def add_table(doc, header, rows, widths, font_size=Pt(9), header_size=Pt(9)):
    table = doc.add_table(rows=1, cols=len(header))
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    table.autofit = False
    set_borders(table)
    set_cell_margins(table)
    repeat_header(table.rows[0])

    for index, text in enumerate(header):
        cell = table.rows[0].cells[index]
        cell.width = Cm(widths[index])
        shade_cell(cell, HEADER_FILL)
        paragraph = cell.paragraphs[0]
        paragraph.paragraph_format.space_after = Pt(0)
        run = paragraph.add_run(text)
        run.bold = True
        run.font.size = header_size
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        run.font.name = BODY_FONT

    for row_index, row in enumerate(rows):
        cells = table.add_row().cells
        for col_index, text in enumerate(row):
            cell = cells[col_index]
            cell.width = Cm(widths[col_index])
            if row_index % 2 == 1:
                shade_cell(cell, ROW_TINT)
            paragraph = cell.paragraphs[0]
            paragraph.paragraph_format.space_after = Pt(0)
            paragraph.paragraph_format.line_spacing = 1.05
            run = paragraph.add_run(str(text))
            run.font.size = font_size
            run.font.name = BODY_FONT
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return table


def add_bullets(doc, items) -> None:
    for item in items:
        paragraph = doc.add_paragraph(item, style="List Bullet")
        paragraph.paragraph_format.space_after = Pt(3)


def add_numbers(doc, items) -> None:
    for item in items:
        paragraph = doc.add_paragraph(item, style="List Number")
        paragraph.paragraph_format.space_after = Pt(3)


def add_file(doc: Document, rel_path: str, note: str = "") -> None:
    path = ROOT / rel_path
    doc.add_heading(rel_path, level=3)
    if note:
        paragraph = doc.add_paragraph(style="FileNote")
        paragraph.add_run(note)
    add_code(doc, path.read_text(encoding="utf-8"))


def page_break(doc) -> None:
    doc.add_page_break()


# --------------------------------------------------------------------------- #
# document content
# --------------------------------------------------------------------------- #
def build(page_map: dict) -> None:
    doc = Document()
    configure_styles(doc)
    page_setup(doc)

    doc.add_paragraph("BankFlow AI Banking Assistant Complete Setup Guide and Source Code", style="Title")
    doc.add_paragraph(
        "BankFlow is a demonstration banking application built with React, Vite and Material UI on "
        "the front end and Django, Django REST Framework and JWT on the back end. This document "
        "contains every step required to create the project on a new computer, followed by the "
        "complete source code of all 96 files in the order you create them."
    )
    doc.add_paragraph(
        "Work through the steps in sequence. Each step explains what you are building and why, "
        "lists the commands to run, and then gives the files for that step with their full code. "
        "After the backend steps you have a working API with three fictional customers and "
        "twenty-eight transactions. After the frontend steps you have a website you can demonstrate "
        "in about ten minutes."
    )
    doc.add_paragraph(
        "Every account, transaction, loan and notification in BankFlow is fictional. The "
        "application never moves real money and must not be used with real banking credentials."
    )

    # ------------------------------------------------------------------ contents
    doc.add_heading("Contents", level=1)
    contents = [
        ("Step 1. Install the required software", "step1"),
        ("Step 2. Create the project folders", "step2"),
        ("Step 3. Create the Django project and virtual environment", "step3"),
        ("Step 4. Backend configuration files", "step4"),
        ("Step 5. Build the users app for authentication and profiles", "step5"),
        ("Step 6. Build the banking app for accounts, transactions and loans", "step6"),
        ("Step 7. Build the assistant app with the AI service", "step7"),
        ("Step 8. Create the database and load the demo data", "step8"),
        ("Step 9. Run the backend test suite", "step9"),
        ("Step 10. Check the API by hand", "step10"),
        ("Step 11. Create the React frontend and install packages", "step11"),
        ("Step 12. Frontend project files", "step12"),
        ("Step 13. API layer, authentication context and helpers", "step13"),
        ("Step 14. Shared components", "step14"),
        ("Step 15. Customer pages", "step15"),
        ("Step 16. Bank employee pages", "step16"),
        ("Step 17. Build the production bundle", "step17"),
        ("Step 18. Run the whole application", "step18"),
        ("Step 19. Demo logins and the ten minute demo script", "step19"),
        ("Step 20. Troubleshooting", "step20"),
        ("Appendix A. API endpoint reference", "appendixa"),
        ("Appendix B. Complete file manifest", "appendixb"),
        ("Appendix C. Database models and relationships", "appendixc"),
        ("Appendix D. Deployment notes and future improvements", "appendixd"),
    ]
    for index, (label, key) in enumerate(contents, start=1):
        paragraph = doc.add_paragraph()
        paragraph.paragraph_format.space_after = Pt(2)
        paragraph.paragraph_format.tab_stops.add_tab_stop(
            Cm(17.2), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS
        )
        paragraph.add_run(f"{index}. {label}")
        page = page_map.get(key)
        if page:
            paragraph.add_run(f"\t{page}")

    page_break(doc)

    # ------------------------------------------------------------------- step 1
    doc.add_heading("Step 1. Install the required software", level=1)
    doc.add_paragraph(
        "Install the two runtimes the project depends on and confirm the versions before you "
        "create any files. The versions below are the ones this project was built and tested with. "
        "Any newer minor release works as well."
    )
    add_table(
        doc,
        ["Tool", "Version used here", "How to check", "Why the project needs it"],
        [
            ["Python", "3.14.5 (3.10 or newer)", "python --version",
             "Runs Django, the REST API, the seed command and the test suite"],
            ["Node.js", "24.19.0 (18 or newer)", "node --version",
             "Runs Vite and builds the React front end"],
            ["npm", "12.0.2", "npm --version", "Installs the frontend packages"],
            ["A code editor", "Visual Studio Code", "-",
             "Creates and edits the project files"],
            ["A web browser", "Chrome or Edge", "-",
             "Opens the demo website at http://localhost:5173"],
        ],
        [2.9, 3.6, 3.6, 7.1],
    )
    doc.add_paragraph(
        "Open a terminal in the folder where you want the project to live and check both runtimes."
    )
    add_code(
        doc,
        "python --version\n"
        "node --version\n"
        "npm --version",
    )

    # ------------------------------------------------------------------- step 2
    doc.add_heading("Step 2. Create the project folders", level=1)
    doc.add_paragraph(
        "BankFlow keeps the API and the website in two sibling folders so each one can be started "
        "and deployed on its own. Create the structure now; every later step adds files inside it."
    )
    add_code(
        doc,
        "mkdir banking_app\n"
        "cd banking_app\n"
        "mkdir backend\n"
        "mkdir frontend",
    )
    doc.add_paragraph(
        "After all the steps in this document the folder looks like the tree below. Files marked "
        "generated are produced by commands rather than typed by hand."
    )
    add_code(
        doc,
        "banking_app/\n"
        "  README.md\n"
        "  backend/\n"
        "    manage.py\n"
        "    requirements.txt\n"
        "    .env  .env.example\n"
        "    db.sqlite3                 (generated)\n"
        "    config/                    settings.py, urls.py, wsgi.py, asgi.py\n"
        "    users/                     models, serializers, views, urls, admin, tests\n"
        "    banking/                   models, services, serializers, views, admin_views, urls,\n"
        "                               management/commands/seed_demo.py, tests\n"
        "    assistant/                 models, ai_service, serializers, views, urls, tests\n"
        "  frontend/\n"
        "    index.html  package.json  vite.config.js  .env\n"
        "    public/bankflow.svg\n"
        "    src/\n"
        "      main.jsx  App.jsx  theme.js  index.css\n"
        "      components/  context/  services/  utils/  pages/  pages/admin/",
    )

    # ------------------------------------------------------------------- step 3
    doc.add_heading("Step 3. Create the Django project and virtual environment", level=1)
    doc.add_paragraph(
        "A virtual environment keeps the backend packages separate from every other Python "
        "project on the machine. Create it inside the backend folder, activate it, and install the "
        "five packages the API needs."
    )
    add_code(
        doc,
        "cd banking_app/backend\n"
        "python -m venv venv\n"
        "\n"
        "# Windows\n"
        "venv\\Scripts\\activate\n"
        "\n"
        "# macOS or Linux\n"
        "source venv/bin/activate",
    )
    doc.add_paragraph(
        "With the environment active, install the dependencies. The same packages are listed in "
        "requirements.txt in Step 4, so you can either run this command once or create the file "
        "first and run pip install -r requirements.txt."
    )
    add_code(
        doc,
        "pip install Django==5.2.6 djangorestframework==3.16.1 djangorestframework-simplejwt==5.5.1 \\\n"
        "            django-cors-headers==4.9.0 python-dotenv==1.1.1 \"psycopg[binary]==3.2.10\"",
    )
    doc.add_paragraph(
        "psycopg is only needed if you later switch the database to PostgreSQL. Installing it now "
        "keeps the switch to a single environment variable."
    )

    # ------------------------------------------------------------------- step 4
    doc.add_heading("Step 4. Backend configuration files", level=1)
    doc.add_paragraph(
        "The configuration package holds the project settings, the root URL map and the server "
        "entry points. Create the files below exactly as shown; the comments explain each "
        "decision, including how to switch from SQLite to PostgreSQL and how the JWT lifetimes "
        "are set."
    )
    add_file(doc, "backend/requirements.txt", "Pinned backend dependencies.")
    add_file(
        doc,
        "backend/.env.example",
        "Template for the environment file. Copy it to .env and change the values.",
    )
    add_file(doc, "backend/manage.py", "Django command line entry point.")
    add_file(doc, "backend/.gitignore", "Keeps the virtual environment, secrets and database out of git.")
    add_file(doc, "backend/config/__init__.py", "Marks the configuration folder as a Python package.")
    add_file(
        doc,
        "backend/config/settings.py",
        "Project settings: apps, middleware, database switch, JWT, CORS and the AI provider.",
    )
    add_file(
        doc,
        "backend/config/urls.py",
        "Root URL map that wires each app's urls module to its API prefix.",
    )
    add_file(doc, "backend/config/wsgi.py", "WSGI entry point used by production servers.")
    add_file(doc, "backend/config/asgi.py", "ASGI entry point for asynchronous servers.")
    doc.add_paragraph(
        "Copy the environment template so Django can read the secret key, the database choice and "
        "the optional AI settings."
    )
    add_code(doc, "copy .env.example .env        # cp .env.example .env on macOS or Linux")

    # ------------------------------------------------------------------- step 5
    doc.add_heading("Step 5. Build the users app for authentication and profiles", level=1)
    doc.add_paragraph(
        "The users app replaces the default Django user with one that logs in by email and carries "
        "a role field, so the same API can serve customers and bank employees. A profile model "
        "stores the contact and employment details the bank employee area displays."
    )
    doc.add_heading("Models, permissions and signals", level=2)
    doc.add_paragraph(
        "User is an AbstractUser with no username field, an email that must be unique, and a role "
        "that is either CUSTOMER or ADMIN. CustomerProfile is a one-to-one extension created "
        "automatically by a signal, so every user always has a complete profile object."
    )
    add_file(doc, "backend/users/__init__.py")
    add_file(doc, "backend/users/apps.py", "Registers the signal module when the app becomes ready.")
    add_file(doc, "backend/users/models.py", "User manager, User model and CustomerProfile.")
    add_file(doc, "backend/users/signals.py", "Creates a profile for every new user.")
    add_file(doc, "backend/users/permissions.py", "IsBankStaff guard for the employee endpoints.")
    doc.add_heading("Serializers, views and URLs", level=2)
    doc.add_paragraph(
        "The serializers validate registration, keep passwords hashed and restrict profile "
        "updates to the fields a customer is allowed to change. The views expose registration, "
        "profile read and profile update."
    )
    add_file(doc, "backend/users/serializers.py", "Registration, profile read and profile update.")
    add_file(doc, "backend/users/views.py", "Register and profile endpoints.")
    add_file(doc, "backend/users/urls/__init__.py")
    add_file(
        doc,
        "backend/users/urls/auth_urls.py",
        "Registration, login and refresh routes; login and refresh come from SimpleJWT.",
    )
    add_file(doc, "backend/users/urls/profile_urls.py", "The /api/profile/ route.")
    add_file(doc, "backend/users/admin.py", "Django admin registration for users and profiles.")
    add_file(
        doc,
        "backend/users/tests.py",
        "Tests for registration, duplicate email rejection, login and profile updates.",
    )

    # ------------------------------------------------------------------- step 6
    doc.add_heading("Step 6. Build the banking app for accounts, transactions and loans", level=1)
    doc.add_paragraph(
        "This is the core app. It holds the four banking models, the business logic that every "
        "screen and the AI assistant share, the customer API and the bank employee API."
    )
    doc.add_heading("Models and business logic", level=2)
    doc.add_paragraph(
        "Account holds the masked demo account, Transaction records every movement with a running "
        "balance, Loan stores the application, EMI, tenure and outstanding amount, and "
        "Notification carries the simulated alerts. services.py keeps all the arithmetic in one "
        "place: the EMI formula, month boundaries, period totals, category breakdowns, the six "
        "month trend, the ledger rebuild used by the seed command, and the demo transaction list."
    )
    add_file(doc, "backend/banking/__init__.py")
    add_file(doc, "backend/banking/apps.py")
    add_file(doc, "backend/banking/models.py", "Account, Transaction, Loan and Notification.")
    add_file(
        doc,
        "backend/banking/services.py",
        "Shared business logic: EMI, dashboard totals, category analysis, trends, seed ledger.",
    )
    doc.add_heading("Serializers and customer API", level=2)
    doc.add_paragraph(
        "The serializers turn the models into the JSON the React pages expect, including display "
        "labels and computed fields such as the masked account number and the loan progress. The "
        "views expose the dashboard, account, transaction, loan, EMI and notification endpoints."
    )
    add_file(doc, "backend/banking/serializers.py")
    add_file(doc, "backend/banking/views.py", "Customer endpoints, all JWT protected.")
    add_file(doc, "backend/banking/urls/__init__.py")
    add_file(doc, "backend/banking/urls/customer_urls.py")
    doc.add_heading("Bank employee API", level=2)
    doc.add_paragraph(
        "The employee endpoints reuse the same models but skip the per-customer filter, and every "
        "view requires the ADMIN role. The analytics view aggregates the whole portfolio; the loan "
        "endpoint approves, activates or rejects an application and writes a notification for the "
        "customer."
    )
    add_file(doc, "backend/banking/admin_views.py", "Admin dashboard, customer, loan and user APIs.")
    add_file(doc, "backend/banking/urls/admin_urls.py")
    add_file(doc, "backend/banking/admin.py", "Django admin registrations for the banking models.")
    doc.add_heading("Management command and tests", level=2)
    doc.add_paragraph(
        "The seed command creates the three fictional customers, their accounts, twenty-eight "
        "transactions across three months, six loan applications, the notification list and a "
        "saved AI conversation. It is written so the demo numbers always match the script: the "
        "balance is Rs 85,450, monthly income is Rs 45,000, monthly expenses are Rs 18,450 and the "
        "largest category is Shopping at Rs 7,200."
    )
    add_file(doc, "backend/banking/management/__init__.py")
    add_file(doc, "backend/banking/management/commands/__init__.py")
    add_file(
        doc,
        "backend/banking/management/commands/seed_demo.py",
        "Creates every piece of fictional demo data. Run it with python manage.py seed_demo --flush.",
    )
    add_file(
        doc,
        "backend/banking/tests.py",
        "Tests for the dashboard totals, filters, loan application, EMI endpoint and admin access.",
    )

    # ------------------------------------------------------------------- step 7
    doc.add_heading("Step 7. Build the assistant app with the AI service", level=1)
    doc.add_paragraph(
        "The assistant app stores conversations and holds the AI service. The service is split so "
        "the language model is optional: intent detection and data retrieval always run locally, "
        "and the rule based answers produce the response whenever no external key is configured."
    )
    doc.add_heading("Conversation model and AI service", level=2)
    doc.add_paragraph(
        "ChatMessage stores one question and one answer with its intent type and the provider that "
        "produced it, which is what the employee monitoring screen reads. ai_service.py exposes "
        "answer(), which detects the intent, builds a grounded snapshot of the customer data, asks "
        "the model if one is configured, and otherwise answers from the rule based engine. It also "
        "holds the banking knowledge base used for questions such as what is KYC or what is a "
        "credit score."
    )
    add_file(doc, "backend/assistant/__init__.py")
    add_file(doc, "backend/assistant/apps.py")
    add_file(doc, "backend/assistant/models.py", "ChatMessage model used for history and monitoring.")
    add_file(
        doc,
        "backend/assistant/ai_service.py",
        "Intent detection, data grounding, rule based fallback answers and the optional LLM call.",
    )
    doc.add_heading("Assistant API", level=2)
    doc.add_paragraph(
        "The chat view validates the question, calls the service, saves the exchange and returns "
        "the answer with its type and data. The history view returns the saved conversation and "
        "the suggestion list; the monitor view is restricted to bank employees."
    )
    add_file(doc, "backend/assistant/serializers.py")
    add_file(doc, "backend/assistant/views.py")
    add_file(doc, "backend/assistant/urls.py")
    add_file(doc, "backend/assistant/admin.py")
    add_file(
        doc,
        "backend/assistant/tests.py",
        "Tests every assistant intent, the saved history and the employee only monitor endpoint.",
    )

    # ------------------------------------------------------------------- step 8
    doc.add_heading("Step 8. Create the database and load the demo data", level=1)
    doc.add_paragraph(
        "Generate the migrations for the three apps, apply them to create the SQLite database, and "
        "run the seed command. The --flush flag clears any earlier demo data first, so the command "
        "can be repeated at any time to return to a known state."
    )
    add_code(
        doc,
        "python manage.py makemigrations users banking assistant\n"
        "python manage.py migrate\n"
        "python manage.py seed_demo --flush",
    )
    doc.add_paragraph(
        "The seed command prints the demo logins when it finishes. The expected output looks like "
        "this."
    )
    add_code(
        doc,
        "Seeded customer Mohammed Adnan\n"
        "Seeded customer Aisha Khan\n"
        "Seeded customer Rahul Verma\n"
        "\n"
        "Demo data ready.\n"
        "Admin    : admin@bankflow.com / Admin@12345\n"
        "Customer : mohammed@bankflow.com / Demo@12345\n"
        "Customer : aisha@bankflow.com / Demo@12345\n"
        "Customer : rahul@bankflow.com / Demo@12345",
    )
    doc.add_paragraph(
        "The same data is available in the Django admin at http://127.0.0.1:8000/admin/ using the "
        "admin account."
    )

    # ------------------------------------------------------------------- step 9
    doc.add_heading("Step 9. Run the backend test suite", level=1)
    doc.add_paragraph(
        "Django creates a separate test database, seeds nothing, and runs twenty-five tests that "
        "create their own data. The suite covers registration and login, profile updates, dashboard "
        "totals, transaction filters, loan applications, the EMI endpoint, notification state, the "
        "employee permission boundary and every assistant intent."
    )
    add_code(doc, "python manage.py test")
    doc.add_paragraph("A healthy run ends with this output.")
    add_code(
        doc,
        "Found 25 test(s).\n"
        "System check identified no issues (0 silenced).\n"
        "Creating test database for alias 'default'...\n"
        ".........................\n"
        "----------------------------------------------------------------------\n"
        "Ran 25 tests in 31.331s\n"
        "\n"
        "OK\n"
        "Destroying test database for alias 'default'...",
    )

    # ------------------------------------------------------------------ step 10
    doc.add_heading("Step 10. Check the API by hand", level=1)
    doc.add_paragraph(
        "Start the development server and confirm the endpoints answer before you build the "
        "website on top of them."
    )
    add_code(doc, "python manage.py runserver 127.0.0.1:8000")
    doc.add_paragraph(
        "In a second terminal, log in as the demo customer and call the dashboard, the transaction "
        "filter and the assistant. This is PowerShell; the curl equivalents follow."
    )
    add_code(
        doc,
        "$base = 'http://127.0.0.1:8000/api'\n"
        "$login = Invoke-RestMethod -Method Post -Uri \"$base/auth/login/\" -ContentType 'application/json' `\n"
        "  -Body (@{ email = 'mohammed@bankflow.com'; password = 'Demo@12345' } | ConvertTo-Json)\n"
        "$headers = @{ Authorization = \"Bearer $($login.access)\" }\n"
        "\n"
        "Invoke-RestMethod -Uri \"$base/dashboard/\" -Headers $headers\n"
        "Invoke-RestMethod -Uri \"$base/transactions/?category=Shopping&type=DEBIT\" -Headers $headers\n"
        "Invoke-RestMethod -Method Post -Uri \"$base/assistant/chat/\" -Headers $headers `\n"
        "  -ContentType 'application/json' -Body (@{ message = 'What is my balance?' } | ConvertTo-Json)",
    )
    add_code(
        doc,
        "# curl version\n"
        "TOKEN=$(curl -s -X POST http://127.0.0.1:8000/api/auth/login/ \\\n"
        "  -H 'Content-Type: application/json' \\\n"
        "  -d '{\"email\":\"mohammed@bankflow.com\",\"password\":\"Demo@12345\"}' | python -c \\\n"
        "  'import sys,json;print(json.load(sys.stdin)[\"access\"])')\n"
        "\n"
        "curl -s http://127.0.0.1:8000/api/dashboard/ -H \"Authorization: Bearer $TOKEN\"\n"
        "curl -s -X POST http://127.0.0.1:8000/api/assistant/chat/ -H \"Authorization: Bearer $TOKEN\" \\\n"
        "  -H 'Content-Type: application/json' -d '{\"message\":\"How much did I spend this month?\"}'",
    )
    doc.add_paragraph("The dashboard response starts with these values.")
    add_code(
        doc,
        '{"balance": 85450.0, "monthly_income": 45000.0, "monthly_expenses": 18450.0,\n'
        ' "monthly_savings": 26550.0, "active_loans": 2, "total_outstanding": 1137500.0,\n'
        ' "top_category": {"category": "Shopping", "amount": 7200.0, "color": "#8b5cf6"}, ...}',
    )
    doc.add_paragraph("The assistant response for the spending question looks like this.")
    add_code(
        doc,
        '{"response": "You spent Rs 18,450 this month. Your income for the month is Rs 45,000, "\n'
        '             "so your net savings are Rs 26,550.",\n'
        ' "type": "expense_summary", "intent": "expense_summary", "provider": "fallback",\n'
        ' "data": {"amount": 18450.0, "income": 45000.0, "savings": 26550.0}}',
    )

    # ------------------------------------------------------------------ step 11
    doc.add_heading("Step 11. Create the React frontend and install packages", level=1)
    doc.add_paragraph(
        "The website is a Vite project using React 18, Material UI for the components, Recharts for "
        "the charts, Axios for API calls and React Router for navigation. Create the project and "
        "install the packages, then replace the generated files with the ones in Step 12."
    )
    add_code(
        doc,
        "cd banking_app\n"
        "npm create vite@latest frontend -- --template react\n"
        "cd frontend\n"
        "\n"
        "npm install\n"
        "npm install @mui/material @mui/icons-material @emotion/react @emotion/styled\n"
        "npm install axios react-router-dom recharts react-icons",
    )
    doc.add_paragraph(
        "If your npm policy blocks package install scripts, approve them and re-run the install:"
    )
    add_code(doc, "npm install-scripts approve esbuild\nnpm install")

    # ------------------------------------------------------------------ step 12
    doc.add_heading("Step 12. Frontend project files", level=1)
    doc.add_paragraph(
        "These files define the Vite build, the HTML shell, the theme tokens and the route map. "
        "Replace package.json, index.html and vite.config.js with the versions below, and add the "
        "theme, stylesheet, entry point and route file."
    )
    add_file(doc, "frontend/package.json", "Scripts and dependency list for the front end.")
    add_file(doc, "frontend/vite.config.js", "Vite configuration: React plugin and dev server port.")
    add_file(doc, "frontend/index.html", "HTML shell that mounts the React application.")
    add_file(doc, "frontend/.env.example", "Template for the API base URL.")
    add_file(doc, "frontend/.gitignore", "Keeps node_modules, the build output and secrets out of git.")
    add_file(doc, "frontend/public/bankflow.svg", "Favicon used by the browser tab.")
    add_file(doc, "frontend/src/index.css", "Global styles and the small fade-in animation.")
    add_file(
        doc,
        "frontend/src/theme.js",
        "Material UI theme: navy banking palette, rounded corners, card and button defaults.",
    )
    add_file(doc, "frontend/src/main.jsx", "React entry point with the theme, router and auth provider.")
    add_file(
        doc,
        "frontend/src/App.jsx",
        "Route map: public pages, the protected customer area and the employee area.",
    )
    doc.add_paragraph(
        "Copy the environment template so the front end knows where the API lives."
    )
    add_code(doc, "copy .env.example .env        # cp .env.example .env on macOS or Linux")

    # ------------------------------------------------------------------ step 13
    doc.add_heading("Step 13. API layer, authentication context and helpers", level=1)
    doc.add_paragraph(
        "All network access goes through one Axios instance. It adds the JWT access token to every "
        "request, refreshes the token once when the API answers 401, signs the user out when the "
        "refresh fails, and converts any failure into a sentence the interface can display. The "
        "auth context keeps the signed-in user in React state and rehydrates it from the stored "
        "token when the page reloads."
    )
    add_file(doc, "frontend/src/services/api.js", "Axios instance, token store, refresh logic, error mapping.")
    add_file(doc, "frontend/src/services/authService.js", "Register, login, profile and logout calls.")
    add_file(doc, "frontend/src/services/bankingService.js", "Dashboard, account, transactions, loans, EMI, notifications.")
    add_file(doc, "frontend/src/services/aiService.js", "Chat, history, suggestions and clear history.")
    add_file(doc, "frontend/src/services/adminService.js", "Employee analytics, customers, loans, users and AI monitor.")
    add_file(doc, "frontend/src/context/AuthContext.jsx", "Authentication state, login, logout and role flags.")
    add_file(
        doc,
        "frontend/src/utils/formatCurrency.js",
        "Rupee, date, relative time and greeting formatting plus shared category and loan constants.",
    )
    add_file(
        doc,
        "frontend/src/utils/calculations.js",
        "Client side EMI, amortisation schedule and tenure label for instant feedback.",
    )

    # ------------------------------------------------------------------ step 14
    doc.add_heading("Step 14. Shared components", level=1)
    doc.add_paragraph(
        "The components build the application shell and the repeated pieces used by several pages: "
        "the responsive sidebar and app bar, the four statistic cards, the transaction table that "
        "both the customer and employee pages reuse, the loan card, the chat bubble, the route "
        "guard and a small set of layout helpers."
    )
    add_file(doc, "frontend/src/components/AppLayout.jsx", "Sidebar, app bar and page container.")
    add_file(doc, "frontend/src/components/Navbar.jsx", "App bar with page title, notifications and profile menu.")
    add_file(doc, "frontend/src/components/Sidebar.jsx", "Role aware navigation drawer that collapses on mobile.")
    add_file(doc, "frontend/src/components/DashboardCard.jsx", "Statistic card with icon, value and trend.")
    add_file(doc, "frontend/src/components/TransactionTable.jsx", "Reusable transaction table with loading and empty states.")
    add_file(doc, "frontend/src/components/LoanCard.jsx", "Loan summary card with progress and details link.")
    add_file(doc, "frontend/src/components/ChatMessage.jsx", "User and assistant chat bubbles.")
    add_file(doc, "frontend/src/components/ProtectedRoute.jsx", "Route guard for signed-in and employee only routes.")
    add_file(
        doc,
        "frontend/src/components/Common.jsx",
        "Page header, loader, error alert, empty state, status chip and section card.",
    )

    # ------------------------------------------------------------------ step 15
    doc.add_heading("Step 15. Customer pages", level=1)
    doc.add_paragraph(
        "These fourteen pages make up the customer experience, from the public landing page "
        "through to the AI assistant. The table lists what each page does and which API endpoints "
        "it calls."
    )
    add_table(
        doc,
        ["Page", "Route", "API endpoints used"],
        [
            ["Landing", "/", "none (static marketing page with demo logins)"],
            ["Login", "/login", "POST /api/auth/login/, GET /api/profile/"],
            ["Register", "/register", "POST /api/auth/register/"],
            ["Dashboard", "/dashboard", "GET /api/dashboard/, GET /api/notifications/"],
            ["Account", "/account", "GET /api/account/"],
            ["Transactions", "/transactions", "GET /api/transactions/ with filters and paging"],
            ["Transaction details", "/transactions/:id", "GET /api/transactions/<id>/"],
            ["Loans", "/loans", "GET /api/loans/, POST /api/loans/"],
            ["Loan details", "/loans/:id", "GET /api/loans/<id>/"],
            ["EMI calculator", "/emi-calculator", "POST /api/emi/ (verifies the local maths)"],
            ["AI assistant", "/assistant", "POST /api/assistant/chat/, GET and DELETE /api/assistant/history/"],
            ["Notifications", "/notifications", "GET /api/notifications/, PUT /api/notifications/<id>/"],
            ["Profile", "/profile", "GET /api/profile/, PUT /api/profile/"],
            ["Not found", "any unknown route", "none"],
        ],
        [3.9, 3.9, 9.4],
    )
    add_file(
        doc,
        "frontend/src/pages/Landing.jsx",
        "Public landing page with hero, feature cards, assistant preview, security and demo logins.",
    )
    add_file(doc, "frontend/src/pages/Login.jsx", "JWT login with demo autofill, validation and redirect by role.")
    add_file(doc, "frontend/src/pages/Register.jsx", "Registration form with client side validation.")
    add_file(
        doc,
        "frontend/src/pages/Dashboard.jsx",
        "KPI cards, quick actions, four Recharts charts, recent transactions and notifications.",
    )
    add_file(doc, "frontend/src/pages/Account.jsx", "Masked account card and account information list.")
    add_file(
        doc,
        "frontend/src/pages/Transactions.jsx",
        "Search, category, type and date filters, sorting, pagination and filtered totals.",
    )
    add_file(doc, "frontend/src/pages/TransactionDetails.jsx", "Single transaction view with the resulting balance.")
    add_file(
        doc,
        "frontend/src/pages/Loans.jsx",
        "Status tabs, totals and the demo loan application dialog with a live EMI preview.",
    )
    add_file(
        doc,
        "frontend/src/pages/LoanDetails.jsx",
        "Loan summary, progress bar, application details and the first twelve instalments.",
    )
    add_file(
        doc,
        "frontend/src/pages/EMICalculator.jsx",
        "Sliders and inputs, result cards, principal versus interest chart and server verification.",
    )
    add_file(
        doc,
        "frontend/src/pages/AIAssistant.jsx",
        "Chat interface with history panel, suggestion chips, typing state and error handling.",
    )
    add_file(doc, "frontend/src/pages/Notifications.jsx", "Read and unread tabs with mark read and mark all read.")
    add_file(doc, "frontend/src/pages/Profile.jsx", "Profile card and editable contact details.")
    add_file(doc, "frontend/src/pages/NotFound.jsx", "Friendly 404 page with routes back into the application.")

    # ------------------------------------------------------------------ step 16
    doc.add_heading("Step 16. Bank employee pages", level=1)
    doc.add_paragraph(
        "The employee area is guarded by the ADMIN role. These six pages reuse the components from "
        "Step 14 and read the admin endpoints, which return data for every customer."
    )
    add_table(
        doc,
        ["Page", "Route", "API endpoints used"],
        [
            ["Admin dashboard", "/admin", "GET /api/admin/analytics/"],
            ["Customer management", "/admin/customers", "GET /api/admin/customers/, GET /api/admin/customers/<id>/"],
            ["Transaction management", "/admin/transactions", "GET /api/admin/transactions/ with filters"],
            ["Loan management", "/admin/loans", "GET /api/admin/loans/, PATCH /api/admin/loans/<id>/"],
            ["Analytics", "/admin/analytics", "GET /api/admin/analytics/"],
            ["AI monitoring", "/admin/ai-monitor", "GET /api/assistant/monitor/"],
        ],
        [4.2, 4.2, 8.8],
    )
    add_file(
        doc,
        "frontend/src/pages/admin/AdminDashboard.jsx",
        "Six KPI cards, portfolio charts and the top customers table.",
    )
    add_file(
        doc,
        "frontend/src/pages/admin/CustomerManagement.jsx",
        "Searchable customer table and a customer 360 dialog.",
    )
    add_file(
        doc,
        "frontend/src/pages/admin/TransactionManagement.jsx",
        "Portfolio wide transaction table with the same filters as the customer page.",
    )
    add_file(
        doc,
        "frontend/src/pages/admin/LoanManagement.jsx",
        "Loan table with approve, activate and reject actions that notify the customer.",
    )
    add_file(
        doc,
        "frontend/src/pages/admin/AdminAnalytics.jsx",
        "Trend, category, transaction count and active loan ratio charts with a summary grid.",
    )
    add_file(
        doc,
        "frontend/src/pages/admin/AIMonitor.jsx",
        "Assistant monitoring: totals, intent breakdown and the full question log.",
    )

    # ------------------------------------------------------------------ step 17
    doc.add_heading("Step 17. Build the production bundle", level=1)
    doc.add_paragraph(
        "Vite compiles the React application into static files in dist/. Run this whenever you want "
        "to confirm the code still builds cleanly."
    )
    add_code(doc, "npm run build\nnpm run preview      # serves the production bundle locally")
    doc.add_paragraph("The build output lists the bundle files and their gzip sizes.")
    add_code(
        doc,
        "vite v5.4.21 building for production...\n"
        "transforming...\n"
        "checkmark 1868 modules transformed.\n"
        "dist/index.html                     0.62 kB gzip:   0.37 kB\n"
        "dist/assets/index-BYgGbjXY.css      0.50 kB gzip:   0.32 kB\n"
        "dist/assets/index-CX94YJLq.js   1,142.96 kB gzip: 331.14 kB\n"
        "checkmark built in 26.53s",
    )

    # ------------------------------------------------------------------ step 18
    doc.add_heading("Step 18. Run the whole application", level=1)
    doc.add_paragraph(
        "Start the API and the website in two terminals. Keep both running while you demonstrate "
        "the application."
    )
    add_code(
        doc,
        "# terminal 1 - backend\n"
        "cd banking_app/backend\n"
        "venv\\Scripts\\activate\n"
        "python manage.py runserver 127.0.0.1:8000\n"
        "\n"
        "# terminal 2 - frontend\n"
        "cd banking_app/frontend\n"
        "npm run dev",
    )
    doc.add_paragraph(
        "Open http://localhost:5173 for the website and http://127.0.0.1:8000/api/ for the API. "
        "The Django admin is at http://127.0.0.1:8000/admin/."
    )

    # ------------------------------------------------------------------ step 19
    doc.add_heading("Step 19. Demo logins and the ten minute demo script", level=1)
    add_table(
        doc,
        ["Role", "Email", "Password", "What it shows"],
        [
            ["Customer", "mohammed@bankflow.com", "Demo@12345",
             "Balance Rs 85,450, income Rs 45,000, expenses Rs 18,450, two active loans"],
            ["Customer", "aisha@bankflow.com", "Demo@12345", "Second customer with different loans"],
            ["Customer", "rahul@bankflow.com", "Demo@12345", "Third customer with a pending loan"],
            ["Bank employee", "admin@bankflow.com", "Admin@12345", "Employee dashboard and monitoring"],
        ],
        [3.0, 5.2, 3.0, 6.0],
    )
    doc.add_paragraph("Follow this sequence to demonstrate the project in about ten minutes.")
    add_numbers(
        doc,
        [
            "Open the landing page and point out the hero, the six feature cards, the assistant preview and the security section.",
            "Log in as mohammed@bankflow.com and land on the dashboard.",
            "Read the four statistic cards and the four charts, then use the quick actions.",
            "Open the account page and show the masked account number and the account status.",
            "Open transactions, filter by the Shopping category and by type, then open a transaction detail.",
            "Open loans, switch between the status tabs, and submit a new demo loan application with the live EMI preview.",
            "Open the EMI calculator, move the sliders and show the message that the Django API verified the result.",
            "Open the AI assistant and ask: What is my balance, How much did I spend this month, What was my biggest expense, What loans do I have, and Explain EMI. Show the history panel afterwards.",
            "Open notifications and mark one as read.",
            "Log out, log in as admin@bankflow.com and open the admin dashboard.",
            "Approve the pending loan in loan management and show the notification it creates for the customer.",
            "Open analytics and the AI monitoring page, then close on the architecture: React, Axios and JWT, Django REST Framework, the service layer, the database and the AI service.",
        ],
    )

    # ------------------------------------------------------------------ step 20
    doc.add_heading("Step 20. Troubleshooting", level=1)
    doc.add_paragraph(
        "These are the problems that come up most often when the project is set up on a new "
        "machine, with the cause and the fix."
    )
    add_table(
        doc,
        ["Symptom", "Likely cause", "Fix"],
        [
            ["The website shows a red banner about reaching the API",
             "The Django server is not running or the URL differs",
             "Start runserver on 127.0.0.1:8000 and check VITE_API_BASE_URL in frontend/.env"],
            ["Browser console reports a CORS error",
             "The frontend origin is missing from the allowed list",
             "Add it to CORS_ALLOWED_ORIGINS in backend/.env and restart the server"],
            ["Every request returns 401",
             "The access token expired and the refresh token is gone",
             "Log in again; tokens live in localStorage under bankflow_access and bankflow_refresh"],
            ["Login works but the dashboard is empty",
             "The demo data was never seeded",
             "Run python manage.py seed_demo --flush"],
            ["Command not found: manage.py",
             "The terminal is in the wrong folder",
             "cd into banking_app/backend before running manage.py"],
            ["port already in use",
             "Another process holds 8000 or 5173",
             "runserver 127.0.0.1:8001 and update VITE_API_BASE_URL, or stop the other process"],
            ["PostgreSQL connection refused",
             "DB_ENGINE is postgres but no server is running",
             "Set DB_ENGINE=sqlite in backend/.env, or start PostgreSQL and check the credentials"],
            ["npm install stops on blocked install scripts",
             "The package manager policy blocked esbuild",
             "Run npm install-scripts approve esbuild then npm install"],
            ["The assistant replies with the offline wording",
             "No external AI key is configured",
             "This is expected; set AI_PROVIDER=openai and OPENAI_API_KEY in backend/.env for model answers"],
            ["Charts render but the numbers look wrong",
             "The demo data was edited through the Django admin",
             "Run python manage.py seed_demo --flush to return to the documented values"],
        ],
        [5.2, 5.0, 7.0],
    )

    # -------------------------------------------------------------- appendix A
    page_break(doc)
    doc.add_heading("Appendix A. API endpoint reference", level=1)
    doc.add_paragraph(
        "Every endpoint accepts and returns JSON. Customer endpoints need the header "
        "Authorization: Bearer <access token>. Employee endpoints additionally require the ADMIN "
        "role and answer 403 for customers."
    )
    add_table(
        doc,
        ["Method", "Endpoint", "Purpose"],
        [
            ["POST", "/api/auth/register/", "Register a demo customer and create the demo account"],
            ["POST", "/api/auth/login/", "Return access and refresh tokens"],
            ["POST", "/api/auth/refresh/", "Exchange a refresh token for a new access token"],
            ["GET, PUT", "/api/profile/", "Read or update name, phone, address, occupation and income"],
            ["GET", "/api/dashboard/", "Balance, income, expenses, loans, categories, trend and recent transactions"],
            ["GET", "/api/account/", "Masked account number, type, status, branch and IFSC-like identifier"],
            ["GET", "/api/transactions/", "Paginated list; supports search, category, type, status, date and ordering"],
            ["GET", "/api/transactions/<id>/", "Single transaction with the resulting balance"],
            ["GET, POST", "/api/loans/", "List loans or submit a demo application"],
            ["GET", "/api/loans/<id>/", "Single loan with EMI and outstanding amount"],
            ["POST", "/api/emi/", "Server side EMI, total interest and total repayment"],
            ["GET", "/api/notifications/", "Notifications, optionally only unread"],
            ["PUT", "/api/notifications/<id>/", "Mark a notification read or unread"],
            ["POST", "/api/notifications/read-all/", "Mark every notification as read"],
            ["POST", "/api/assistant/chat/", "Ask the assistant and store the exchange"],
            ["GET, DELETE", "/api/assistant/history/", "Read or clear the saved conversation"],
            ["GET", "/api/assistant/suggestions/", "Suggested question chips"],
            ["GET", "/api/admin/analytics/", "Portfolio totals and every admin chart"],
            ["GET", "/api/admin/analytics/overview/", "The six KPI numbers used on the admin dashboard"],
            ["GET", "/api/admin/customers/", "Customer table, supports search"],
            ["GET", "/api/admin/customers/<id>/", "Customer 360 view with accounts, dashboard and loans"],
            ["GET", "/api/admin/transactions/", "All transactions with filters across every customer"],
            ["GET", "/api/admin/loans/", "All loans with status and type filters"],
            ["PATCH", "/api/admin/loans/<id>/", "Approve, activate or reject a loan and notify the customer"],
            ["GET", "/api/admin/users/", "User management table"],
            ["GET", "/api/assistant/monitor/", "Assistant totals, intent breakdown and the question log"],
        ],
        [2.2, 6.2, 8.8],
    )

    # -------------------------------------------------------------- appendix B
    doc.add_heading("Appendix B. Complete file manifest", level=1)
    doc.add_paragraph(
        "The manifest lists every file in the project with its purpose and length. Generated files "
        "are marked, because they are produced by the commands in Steps 8 and 11 rather than typed."
    )
    manifest = []
    for rel_path, purpose in MANIFEST:
        path = ROOT / rel_path
        lines = len(path.read_text(encoding="utf-8").splitlines()) if path.exists() else 0
        manifest.append([rel_path, purpose, str(lines)])
    add_table(
        doc,
        ["Path", "Purpose", "Lines"],
        manifest,
        [6.4, 9.0, 1.8],
        font_size=Pt(8.5),
        header_size=Pt(8.5),
    )

    # -------------------------------------------------------------- appendix C
    doc.add_heading("Appendix C. Database models and relationships", level=1)
    doc.add_paragraph(
        "Seven models carry the whole application. The relationship chain is User to "
        "CustomerProfile to Account to Transaction, with loans, notifications and chat messages "
        "attached to the user."
    )
    add_code(
        doc,
        "User (users)\n"
        "  |-- CustomerProfile   one to one\n"
        "  |-- Account           one to many\n"
        "  |     '-- Transaction one to many\n"
        "  |-- Loan              one to many\n"
        "  |-- Notification      one to many\n"
        "  '-- ChatMessage       one to many",
    )
    add_table(
        doc,
        ["Model", "Key fields", "Relationships"],
        [
            ["User", "email (login), name, role, is_active", "Source of every customer record"],
            ["CustomerProfile", "phone, address, occupation, employment_type, monthly_income",
             "One to one with User"],
            ["Account", "account_number, account_type, balance, status, ifsc_code, branch",
             "Many to one with User, one to many with Transaction"],
            ["Transaction", "transaction_id, date, description, category, transaction_type, amount, status, balance_after",
             "Many to one with Account"],
            ["Loan", "loan_id, loan_type, amount, interest_rate, tenure_months, emi, remaining_amount, status, purpose, monthly_income",
             "Many to one with User"],
            ["Notification", "title, message, notification_type, is_read", "Many to one with User"],
            ["ChatMessage", "message, response, response_type, provider", "Many to one with User"],
        ],
        [3.2, 8.4, 5.6],
    )

    # -------------------------------------------------------------- appendix D
    doc.add_heading("Appendix D. Deployment notes and future improvements", level=1)
    doc.add_paragraph(
        "The development setup in this document is enough to run and demonstrate the project. The "
        "notes below cover what changes when the application is hosted, and which additions are "
        "worth building next."
    )
    add_bullets(
        doc,
        [
            "Set DJANGO_DEBUG=False, use a long random DJANGO_SECRET_KEY, and list only your real host names in DJANGO_ALLOWED_HOSTS.",
            "Run python manage.py collectstatic and serve the static files through a web server or a static host.",
            "Serve the React bundle produced by npm run build from any static host, and point VITE_API_BASE_URL at the deployed API.",
            "Switch to PostgreSQL with DB_ENGINE=postgres and keep the database credentials in environment variables, never in the repository.",
            "Add refresh token rotation and blacklisting, and enable two factor authentication for employee accounts.",
            "Stream assistant answers, add function calling so the model can query the API directly, and keep the rule based engine as the offline fallback.",
            "Add Celery and Redis for scheduled EMI reminders and monthly spending summaries.",
            "Replace notification polling with WebSockets and add statement export to CSV or PDF.",
            "Add Playwright end to end tests and a GitHub Actions workflow that runs the Django tests and the frontend build on every push.",
        ],
    )

    doc.save(OUTPUT)
    print(f"wrote {OUTPUT}")


# --------------------------------------------------------------------------- #
# file manifest used by Appendix B (path, purpose)
# --------------------------------------------------------------------------- #
MANIFEST = [
    ("backend/requirements.txt", "Pinned backend dependencies"),
    ("backend/.env.example", "Environment variable template"),
    ("backend/.gitignore", "Backend ignore rules"),
    ("backend/manage.py", "Django command line entry point"),
    ("backend/config/settings.py", "Project settings and app registration"),
    ("backend/config/urls.py", "Root URL map"),
    ("backend/config/wsgi.py", "WSGI entry point"),
    ("backend/config/asgi.py", "ASGI entry point"),
    ("backend/users/models.py", "User, role field and CustomerProfile"),
    ("backend/users/signals.py", "Auto creates a profile for new users"),
    ("backend/users/permissions.py", "IsBankStaff permission class"),
    ("backend/users/serializers.py", "Register, profile read and update serializers"),
    ("backend/users/views.py", "Register and profile endpoints"),
    ("backend/users/urls/auth_urls.py", "Register, login and refresh routes"),
    ("backend/users/urls/profile_urls.py", "Profile route"),
    ("backend/users/admin.py", "User and profile admin registration"),
    ("backend/users/tests.py", "Authentication and profile tests"),
    ("backend/banking/models.py", "Account, Transaction, Loan and Notification"),
    ("backend/banking/services.py", "EMI, dashboard, analytics and seed helpers"),
    ("backend/banking/serializers.py", "Banking API serializers"),
    ("backend/banking/views.py", "Customer API views"),
    ("backend/banking/admin_views.py", "Employee API views"),
    ("backend/banking/urls/customer_urls.py", "Customer routes"),
    ("backend/banking/urls/admin_urls.py", "Employee routes"),
    ("backend/banking/admin.py", "Banking model admin registration"),
    ("backend/banking/management/commands/seed_demo.py", "Creates all fictional demo data"),
    ("backend/banking/tests.py", "Banking API tests"),
    ("backend/assistant/models.py", "ChatMessage model"),
    ("backend/assistant/ai_service.py", "Intents, data grounding, rules and LLM hook"),
    ("backend/assistant/serializers.py", "Chat request and message serializers"),
    ("backend/assistant/views.py", "Chat, history, suggestions and monitor views"),
    ("backend/assistant/urls.py", "Assistant routes"),
    ("backend/assistant/admin.py", "Chat message admin registration"),
    ("backend/assistant/tests.py", "Assistant intent tests"),
    ("frontend/package.json", "Frontend scripts and dependencies"),
    ("frontend/vite.config.js", "Vite configuration"),
    ("frontend/index.html", "HTML shell"),
    ("frontend/.env.example", "Frontend environment template"),
    ("frontend/.gitignore", "Frontend ignore rules"),
    ("frontend/public/bankflow.svg", "Favicon"),
    ("frontend/src/index.css", "Global styles"),
    ("frontend/src/theme.js", "Material UI theme"),
    ("frontend/src/main.jsx", "React entry point"),
    ("frontend/src/App.jsx", "Route map"),
    ("frontend/src/services/api.js", "Axios instance, tokens and error mapping"),
    ("frontend/src/services/authService.js", "Authentication calls"),
    ("frontend/src/services/bankingService.js", "Banking calls"),
    ("frontend/src/services/aiService.js", "Assistant calls"),
    ("frontend/src/services/adminService.js", "Employee calls"),
    ("frontend/src/context/AuthContext.jsx", "Authentication state"),
    ("frontend/src/utils/formatCurrency.js", "Formatting helpers and constants"),
    ("frontend/src/utils/calculations.js", "EMI and amortisation helpers"),
    ("frontend/src/components/AppLayout.jsx", "Application shell"),
    ("frontend/src/components/Navbar.jsx", "Top app bar"),
    ("frontend/src/components/Sidebar.jsx", "Navigation drawer"),
    ("frontend/src/components/DashboardCard.jsx", "Statistic card"),
    ("frontend/src/components/TransactionTable.jsx", "Reusable transaction table"),
    ("frontend/src/components/LoanCard.jsx", "Loan summary card"),
    ("frontend/src/components/ChatMessage.jsx", "Chat bubble"),
    ("frontend/src/components/ProtectedRoute.jsx", "Route guard"),
    ("frontend/src/components/Common.jsx", "Shared layout primitives"),
    ("frontend/src/pages/Landing.jsx", "Public landing page"),
    ("frontend/src/pages/Login.jsx", "Login page"),
    ("frontend/src/pages/Register.jsx", "Registration page"),
    ("frontend/src/pages/Dashboard.jsx", "Customer dashboard with charts"),
    ("frontend/src/pages/Account.jsx", "Account details page"),
    ("frontend/src/pages/Transactions.jsx", "Transactions list with filters"),
    ("frontend/src/pages/TransactionDetails.jsx", "Transaction detail page"),
    ("frontend/src/pages/Loans.jsx", "Loans page and application dialog"),
    ("frontend/src/pages/LoanDetails.jsx", "Loan detail page"),
    ("frontend/src/pages/EMICalculator.jsx", "EMI calculator page"),
    ("frontend/src/pages/AIAssistant.jsx", "AI chat page"),
    ("frontend/src/pages/Notifications.jsx", "Notifications page"),
    ("frontend/src/pages/Profile.jsx", "Profile page"),
    ("frontend/src/pages/NotFound.jsx", "404 page"),
    ("frontend/src/pages/admin/AdminDashboard.jsx", "Employee dashboard"),
    ("frontend/src/pages/admin/CustomerManagement.jsx", "Customer management"),
    ("frontend/src/pages/admin/TransactionManagement.jsx", "Transaction management"),
    ("frontend/src/pages/admin/LoanManagement.jsx", "Loan management and decisions"),
    ("frontend/src/pages/admin/AdminAnalytics.jsx", "Analytics dashboard"),
    ("frontend/src/pages/admin/AIMonitor.jsx", "Assistant monitoring"),
]


def main() -> None:
    page_map = {}
    if len(sys.argv) > 1:
        # utf-8-sig tolerates the byte order mark that Windows PowerShell writes.
        page_map = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8-sig"))
    build(page_map)


if __name__ == "__main__":
    main()
```

### tools/build_beginner_docx.py

```python
#!/usr/bin/env python3
"""Build the beginner edition of the BankFlow guide.

Same complete program as the reference guide, but written as numbered lessons that
start with installing VS Code on a brand new laptop. Every lesson ends with a check
so the reader always knows whether the previous step worked before moving on.

Usage: python build_beginner_docx.py [page-map.json]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import build_bankflow_docx as base  # noqa: E402  (helper functions are shared)

from docx import Document  # noqa: E402
from docx.enum.text import WD_TAB_ALIGNMENT, WD_TAB_LEADER  # noqa: E402
from docx.shared import Cm, Pt  # noqa: E402

ROOT = base.ROOT
OUTPUT = ROOT / "BankFlow-Beginner-Step-by-Step-Guide-with-Full-Code.docx"


def add_goal(doc, text: str) -> None:
    paragraph = doc.add_paragraph()
    paragraph.paragraph_format.space_after = Pt(4)
    run = paragraph.add_run("Goal: ")
    run.bold = True
    paragraph.add_run(text)


def add_check(doc, text: str) -> None:
    paragraph = doc.add_paragraph()
    paragraph.paragraph_format.space_before = Pt(2)
    paragraph.paragraph_format.space_after = Pt(8)
    run = paragraph.add_run("Check: ")
    run.bold = True
    paragraph.add_run(text)


def add_note(doc, label: str, text: str) -> None:
    paragraph = doc.add_paragraph()
    paragraph.paragraph_format.space_after = Pt(8)
    run = paragraph.add_run(f"{label}: ")
    run.bold = True
    paragraph.add_run(text)


def add_code_file(doc, rel_path: str, where: str, note: str = "") -> None:
    """Beginner framing: tell the reader where the file goes, then print it in full."""
    doc.add_heading(rel_path, level=3)
    frame = doc.add_paragraph(style="FileNote")
    frame.add_run(where)
    if note:
        doc.add_paragraph(style="FileNote").add_run(note)
    base.add_code(doc, (ROOT / rel_path).read_text(encoding="utf-8"))


def add_command_block(doc, title: str, command: str, expected: str = "") -> None:
    doc.add_paragraph(title).paragraph_format.space_after = Pt(2)
    base.add_code(doc, command)
    if expected:
        doc.add_paragraph("You should see something like this:").paragraph_format.space_after = Pt(2)
        base.add_code(doc, expected)


def build(page_map: dict) -> None:
    doc = Document()
    base.configure_styles(doc)
    doc.styles["Normal"].font.size = Pt(11)
    doc.styles["Normal"].paragraph_format.space_after = Pt(7)
    base.page_setup(doc)

    # ------------------------------------------------------------------- cover
    doc.add_paragraph("BankFlow Beginner Guide Build the Website Step by Step", style="Title")
    doc.add_paragraph(
        "This guide is written for someone who has never built a website before. It starts with an "
        "empty laptop, walks you through installing the tools, and then builds the complete BankFlow "
        "banking application one small lesson at a time. Every lesson tells you what to do, what you "
        "should see, and what to do when something goes wrong."
    )
    doc.add_paragraph(
        "The whole program is inside this document. You do not need to invent any code: each lesson "
        "shows a file and its complete contents, and you copy that file into the folder named above "
        "it. Nothing is left out and nothing is shortened."
    )
    doc.add_paragraph(
        "BankFlow is a practice project that uses pretend money. It has no connection to any real "
        "bank, so you can click anything you like without risk."
    )

    doc.add_heading("How to use this guide", level=1)
    doc.add_paragraph(
        "Read one lesson at a time and finish its check before starting the next one. The lessons are "
        "in order on purpose: the backend lessons must come before the website lessons, because the "
        "website talks to the backend you build first."
    )
    base.add_numbers(
        doc,
        [
            "Do the work on your own laptop rather than reading like a book. Typing and clicking is how the ideas stick.",
            "When a lesson shows code, copy the whole block, including every bracket and comma, and change nothing unless the lesson says to.",
            "Run the check command after each lesson. If the check does not look right, fix it now with the troubleshooting lesson rather than continuing.",
            "Keep two terminals open in the later lessons: one for the backend and one for the website. Both must stay running at the same time.",
            "If you take a break, come back to Lesson 28 to stop and restart everything cleanly.",
        ],
    )

    doc.add_heading("Contents", level=1)
    contents = [
        ("Part 1 Lesson 1. Install Visual Studio Code", "lesson1"),
        ("Part 1 Lesson 2. Install Python", "lesson2"),
        ("Part 1 Lesson 3. Install Node.js", "lesson3"),
        ("Part 1 Lesson 4. Add the helpful VS Code extensions", "lesson4"),
        ("Part 1 Lesson 5. Learn the five VS Code actions you need", "lesson5"),
        ("Part 1 Lesson 6. Create your project folder", "lesson6"),
        ("Part 2 Lesson 7. Set up the backend virtual environment", "lesson7"),
        ("Part 2 Lesson 8. Create the backend configuration files", "lesson8"),
        ("Part 2 Lesson 9. Create the users app for logging in", "lesson9"),
        ("Part 2 Lesson 10. Create the banking models and business logic", "lesson10"),
        ("Part 2 Lesson 11. Create the banking API and the bank employee API", "lesson11"),
        ("Part 2 Lesson 12. Create the demo data command", "lesson12"),
        ("Part 2 Lesson 13. Create the AI assistant app", "lesson13"),
        ("Part 2 Lesson 14. Create the database and load the demo data", "lesson14"),
        ("Part 2 Lesson 15. Run the backend tests", "lesson15"),
        ("Part 2 Lesson 16. Start the backend and see your API working", "lesson16"),
        ("Part 3 Lesson 17. Create the React website project", "lesson17"),
        ("Part 3 Lesson 18. Create the website settings and theme", "lesson18"),
        ("Part 3 Lesson 19. Create the login state and API connection", "lesson19"),
        ("Part 3 Lesson 20. Create the shared components", "lesson20"),
        ("Part 3 Lesson 21. Create the customer pages", "lesson21"),
        ("Part 3 Lesson 22. Create the bank employee pages", "lesson22"),
        ("Part 3 Lesson 23. Start the website and click through it", "lesson23"),
        ("Part 4 Lesson 24. Guided tour of every screen", "lesson24"),
        ("Part 4 Lesson 25. Change something and watch it update", "lesson25"),
        ("Part 4 Lesson 26. How a click becomes a database record", "lesson26"),
        ("Part 4 Lesson 27. Errors you will meet and how to fix them", "lesson27"),
        ("Part 4 Lesson 28. Stop, start and restart everything", "lesson28"),
        ("Part 4 Lesson 29. What to learn next", "lesson29"),
        ("Appendix A. Plain English word list", "appendixa"),
        ("Appendix B. Every file and what it does", "appendixb"),
        ("Appendix C. Logins and the demo script", "appendixc"),
        ("Appendix D. The API in one table", "appendixd"),
    ]
    for index, (label, key) in enumerate(contents, start=1):
        paragraph = doc.add_paragraph()
        paragraph.paragraph_format.space_after = Pt(2)
        paragraph.paragraph_format.tab_stops.add_tab_stop(
            Cm(17.2), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS
        )
        paragraph.add_run(f"{index}. {label}")
        page = page_map.get(key)
        if page:
            paragraph.add_run(f"\t{page}")

    base.page_break(doc)

    # -------------------------------------------------------------- part 1
    doc.add_heading("Part 1. Set up the laptop", level=1)
    doc.add_paragraph(
        "Four programs go onto the laptop before any code is written. Two of them run the backend "
        "and the website, one is the editor where you write and run everything, and one adds helpful "
        "features to that editor. Install them in the order below."
    )

    doc.add_heading("Lesson 1. Install Visual Studio Code", level=1)
    add_goal(doc, "Get a code editor on the laptop so you can create files and run commands in one place.")
    doc.add_paragraph(
        "Visual Studio Code, usually called VS Code, is a free editor from Microsoft. Throughout this "
        "guide it does two jobs: it is the place you write files, and it contains the terminal, which "
        "is the place you type commands."
    )
    base.add_numbers(
        doc,
        [
            "Open a browser and go to code.visualstudio.com.",
            "Click the big Download button for Windows. The site detects your system automatically.",
            "When the download finishes, open the file. It is called something like VSCodeUserSetup-x64.exe.",
            "On the licence screen select I accept the agreement, then click Next.",
            "Keep the default install location and click Next.",
            "On the Select Additional Tasks screen, tick Add to PATH, then tick Open with Code action for both file and directory, then click Next and Install.",
            "When it finishes, leave the Run Visual Studio Code box ticked and click Finish. VS Code opens.",
        ],
    )
    add_note(
        doc,
        "Why the extra ticks matter",
        "Tick Add to PATH so you can start VS Code from a terminal later, and tick the Open with Code "
        "actions so you can right click any folder and open it in VS Code with one click.",
    )
    add_check(
        doc,
        "VS Code is open and you can see the Welcome tab. Close the Welcome tab with the small x on "
        "its tab; the window stays open and empty, which is exactly right for now.",
    )

    doc.add_heading("Lesson 2. Install Python", level=1)
    add_goal(doc, "Install Python, which runs the backend of the application.")
    doc.add_paragraph(
        "Python is the language the server side of BankFlow is written in. One checkbox on the "
        "installer decides whether the command python works everywhere, so read step four closely."
    )
    base.add_numbers(
        doc,
        [
            "Go to python.org/downloads in your browser.",
            "Click the yellow Download Python button for Windows.",
            "Open the downloaded file once it is in your Downloads folder.",
            "On the very first screen, tick the box at the bottom that says Add python.exe to PATH, then click Install Now.",
            "Wait for the progress bar to finish, then click Close.",
        ],
    )
    add_note(
        doc,
        "If you forget the checkbox",
        "Run the installer again, choose Modify, and make sure Add python.exe to PATH is ticked. "
        "Without it you will see the message that python is not recognised in Lesson 5.",
    )
    doc.add_paragraph(
        "Now prove it works. Open a terminal by clicking the Start button, typing cmd, and pressing "
        "Enter. A black window appears. Type this and press Enter."
    )
    base.add_code(doc, "python --version")
    add_check(
        doc,
        "The terminal prints Python followed by a version number, for example Python 3.14.5. If it "
        "instead says python is not recognized, see Lesson 27.",
    )

    doc.add_heading("Lesson 3. Install Node.js", level=1)
    add_goal(doc, "Install Node.js so the website can be created and run.")
    doc.add_paragraph(
        "Node.js runs the tool that builds the React website. Installing Node.js also installs npm, "
        "which is the program that downloads ready made code libraries for the website."
    )
    base.add_numbers(
        doc,
        [
            "Go to nodejs.org in your browser.",
            "Click the button labelled LTS, which stands for long term support. Choose that one, not the Current one.",
            "Open the downloaded file and click Next through the installer.",
            "Accept the licence, keep the default folder, and keep every checkbox as it is.",
            "On the Tools for Native Modules screen you can leave the checkbox empty, then click Next.",
            "Click Install, wait for it to finish, then click Finish.",
        ],
    )
    doc.add_paragraph(
        "Prove it works in the same terminal window you used for Python."
    )
    base.add_code(doc, "node --version\nnpm --version")
    add_check(
        doc,
        "You see two version numbers, for example v24.19.0 and 12.0.2. Two numbers mean both Node.js "
        "and npm are ready.",
    )

    doc.add_heading("Lesson 4. Add the helpful VS Code extensions", level=1)
    add_goal(doc, "Make VS Code understand Python and React, and format your files neatly.")
    doc.add_paragraph(
        "An extension is a small add on for VS Code. The two below are optional in the sense that the "
        "project runs without them, but they colour your code, warn you about mistakes and keep files "
        "tidy, which makes learning much easier."
    )
    base.add_numbers(
        doc,
        [
            "In VS Code, look at the tall icon bar on the far left and click the icon that looks like four squares, or press Ctrl+Shift+X. The Extensions panel opens.",
            "In the search box type Python, and in the results find the one published by Microsoft, then click Install.",
            "Search again for ES7 plus React snippets and install the extension with the most downloads.",
            "Search once more for Prettier Code formatter and install the one by Prettier. It keeps indentation consistent.",
        ],
    )
    add_check(
        doc,
        "The Extensions panel shows the three items with an Installed label and no Install button. "
        "You can close the panel by clicking the squares icon again.",
    )

    doc.add_heading("Lesson 5. Learn the five VS Code actions you need", level=1)
    add_goal(doc, "Learn only the parts of the editor this guide uses, so the screen feels familiar.")
    doc.add_paragraph(
        "VS Code has hundreds of features and you need five of them. Practise them in this lesson "
        "before you create anything."
    )
    base.add_table(
        doc,
        ["What you want to do", "How to do it", "What appears"],
        [
            ["Open a folder in the editor", "Menu File, then Open Folder, then choose the folder",
             "The folder name appears at the top of the left sidebar"],
            ["Create a new file", "Right click in the sidebar, choose New File, type the full name, press Enter",
             "An empty tab opens with the file name on it"],
            ["Save the file", "Press Ctrl+S, or menu File then Save",
             "The dot on the file tab disappears once the file is saved"],
            ["Open the terminal inside VS Code", "Menu Terminal, then New Terminal, or press Ctrl and the backtick key",
             "A panel opens at the bottom with a command prompt"],
            ["Run a command", "Click inside the terminal panel, type the command, press Enter",
             "The terminal prints the result of the command"],
        ],
        [4.6, 6.4, 6.2],
    )
    add_note(
        doc,
        "The most useful habit in this guide",
        "Always run commands in the VS Code terminal that is open in your project folder. The "
        "terminal starts in whatever folder you opened, so you do not have to type long paths.",
    )
    add_check(
        doc,
        "You can open a folder, create a file, save it, open the terminal and run a command without "
        "looking anything up.",
    )

    doc.add_heading("Lesson 6. Create your project folder", level=1)
    add_goal(doc, "Create one folder that will hold the whole project, and open it in VS Code.")
    doc.add_paragraph(
        "Everything you build lives inside a single folder called banking_app, which contains two "
        "sub folders: backend for the server and frontend for the website. Keeping them together "
        "makes it easy to copy the project to another computer later."
    )
    base.add_numbers(
        doc,
        [
            "Open File Explorer and go to the drive where you keep your work, for example drive D or your Documents folder.",
            "Right click in an empty space, choose New then Folder, and name it banking_app.",
            "Open banking_app and create two more folders inside it, one named backend and one named frontend.",
            "Close File Explorer. In VS Code choose File, then Open Folder, select banking_app and click Select Folder.",
            "VS Code may ask whether you trust the authors of the files. Choose Yes, I trust the authors, because these are your own folders.",
        ],
    )
    doc.add_paragraph("Your sidebar should now show the two empty folders like this.")
    base.add_code(
        doc,
        "BANKING_APP\n"
        "    backend\n"
        "    frontend",
    )
    add_check(
        doc,
        "The sidebar shows banking_app with backend and frontend inside it. Part 1 is complete; the "
        "laptop has every tool installed and a home for the project.",
    )

    # -------------------------------------------------------------- part 2
    base.page_break(doc)
    doc.add_heading("Part 2. Build the backend", level=1)
    doc.add_paragraph(
        "The backend is the part that stores the pretend bank data and answers questions from the "
        "website. You build it first because the website needs something to talk to. Every command "
        "in this part is typed in the VS Code terminal, and the terminal must be inside the backend "
        "folder when you run it."
    )

    doc.add_heading("Lesson 7. Set up the backend virtual environment", level=1)
    add_goal(doc, "Create a private box for the backend libraries and install Django inside it.")
    doc.add_paragraph(
        "A virtual environment is a private box of libraries that belongs to this one project. It "
        "stops BankFlow's libraries from interfering with any other Python work on the laptop. You "
        "create it once and then switch it on whenever you work on the project."
    )
    doc.add_paragraph(
        "First move the terminal into the backend folder. In the VS Code terminal type these two "
        "lines, pressing Enter after each one."
    )
    base.add_code(
        doc,
        "cd backend\n"
        "python -m venv venv",
    )
    add_check(
        doc,
        "A new folder named venv appears inside backend in the sidebar. The command finishes with no "
        "error message.",
    )
    doc.add_paragraph(
        "Now switch the environment on and install the libraries. The activation command differs "
        "between Windows and macOS, so use the line that matches your laptop."
    )
    base.add_code(
        doc,
        "# Windows\n"
        "venv\\Scripts\\activate\n"
        "\n"
        "# macOS or Linux\n"
        "source venv/bin/activate",
    )
    add_check(
        doc,
        "The start of the terminal line now shows (venv) in brackets. That tells you the private box "
        "is switched on. Every backend command in this guide assumes you see it.",
    )
    doc.add_paragraph("With (venv) showing, install the backend libraries.")
    base.add_code(
        doc,
        "pip install Django==5.2.6 djangorestframework==3.16.1 djangorestframework-simplejwt==5.5.1 "
        "django-cors-headers==4.9.0 python-dotenv==1.1.1 \"psycopg[binary]==3.2.10\"",
    )
    add_check(
        doc,
        "The last line says Successfully installed followed by the library names. The list includes "
        "Django, djangorestframework, djangorestframework-simplejwt, django-cors-headers, "
        "python-dotenv and psycopg. If pip is not recognised, see Lesson 27.",
    )
    add_note(
        doc,
        "Remember to switch on the box every time",
        "When you open a new terminal for backend work, run venv\\Scripts\\activate first on Windows. "
        "If you forget, commands fail with No module named django.",
    )

    doc.add_heading("Lesson 8. Create the backend configuration files", level=1)
    add_goal(doc, "Create the files that tell Django how the project is set up.")
    doc.add_paragraph(
        "These eight files are the settings and entry points of the backend. Create each one by "
        "right clicking inside the correct folder, choosing New File, and typing the name exactly as "
        "the heading above the code shows. Then paste the whole block and save with Ctrl+S."
    )
    doc.add_paragraph(
        "The settings file is the most important one. It lists which parts of the project are turned "
        "on, where the database lives, how long a login lasts, and which website address is allowed "
        "to call the API. Read the comments in it as you paste; they explain each choice in one line."
    )
    add_code_file(doc, "backend/requirements.txt", "Create this file directly inside backend. It lists the exact library versions from Lesson 7.")
    add_code_file(doc, "backend/.env.example", "Create this file directly inside backend. It is the template for the secrets file.")
    add_code_file(doc, "backend/.gitignore", "Create this file directly inside backend. It keeps private files out of version control.")
    add_code_file(doc, "backend/manage.py", "Create this file directly inside backend. It is the command you type to run backend tasks.")
    add_code_file(doc, "backend/config/__init__.py", "Right click backend, choose New Folder, name it config, then create this empty file inside it.")
    add_code_file(doc, "backend/config/settings.py", "Inside the config folder. This is the main settings file described above.")
    add_code_file(doc, "backend/config/urls.py", "Inside the config folder. It maps each web address to the code that answers it.")
    add_code_file(doc, "backend/config/wsgi.py", "Inside the config folder. It lets a production server start the project.")
    add_code_file(doc, "backend/config/asgi.py", "Inside the config folder. The equivalent entry point for asynchronous servers.")
    doc.add_paragraph(
        "Finally, make your own private copy of the environment file. In the terminal run:"
    )
    base.add_code(doc, "copy .env.example .env      # cp .env.example .env on macOS or Linux")
    add_check(
        doc,
        "The sidebar shows manage.py, requirements.txt, the .env files and a config folder that "
        "contains four files. Now test the settings by asking Django to check itself.",
    )
    base.add_code(doc, "python manage.py check")
    add_check(
        doc,
        "The terminal prints System check identified no issues with a count in brackets. That one "
        "line means every settings file is correct.",
    )

    doc.add_heading("Lesson 9. Create the users app for logging in", level=1)
    add_goal(doc, "Create the part of the backend that handles accounts, logins and customer details.")
    doc.add_paragraph(
        "In Django, an app is a folder that groups related features. The users app owns three ideas: "
        "a user who logs in with an email address instead of a username, a role that says whether the "
        "person is a customer or a bank employee, and a profile that stores the extra details the "
        "bank employee screens display."
    )
    base.add_numbers(
        doc,
        [
            "Inside backend, create a folder named users.",
            "Inside that folder create another folder named urls.",
            "Create every file below using the same New File method, then paste the code and save.",
            "When the files exist, run makemigrations users so Django prepares the database tables for this app.",
        ],
    )
    add_code_file(doc, "backend/users/__init__.py", "An empty file that marks the folder as a Python package.")
    add_code_file(doc, "backend/users/apps.py", "Describes the app and switches on the profile signal.")
    add_code_file(doc, "backend/users/models.py", "The user, the role choices and the customer profile.")
    add_code_file(doc, "backend/users/signals.py", "Creates a profile automatically for every new user.")
    add_code_file(doc, "backend/users/permissions.py", "The check that only bank employees can open employee pages.")
    add_code_file(doc, "backend/users/serializers.py", "Turns user details into JSON and validates registration.")
    add_code_file(doc, "backend/users/views.py", "The code that answers register and profile requests.")
    add_code_file(doc, "backend/users/urls/__init__.py", "Marks the urls folder as a package.")
    add_code_file(doc, "backend/users/urls/auth_urls.py", "The register, login and refresh web addresses.")
    add_code_file(doc, "backend/users/urls/profile_urls.py", "The profile web address.")
    add_code_file(doc, "backend/users/admin.py", "Makes users editable in the built in Django admin site.")
    add_code_file(doc, "backend/users/tests.py", "Automatic tests for registration, login and profile updates.")
    add_check(
        doc,
        "You now have a users folder with twelve files. Nothing needs to run yet; the checks happen "
        "in Lesson 14 once the whole backend exists.",
    )

    doc.add_heading("Lesson 10. Create the banking models and business logic", level=1)
    add_goal(doc, "Create the four banking tables and the file that does all the money arithmetic.")
    doc.add_paragraph(
        "A model is a description of a table in the database. BankFlow has four: accounts, "
        "transactions, loans and notifications. PostgreSQL or SQLite creates the real tables from "
        "these descriptions, so you never write database code by hand."
    )
    doc.add_paragraph(
        "The services file is where the thinking lives. It holds the EMI formula, the monthly totals, "
        "the spending categories, the six month trend and the list of pretend transactions used by "
        "the seed command in Lesson 12. The dashboard, the charts and the AI assistant all call this "
        "one file, which is why the numbers on every screen always agree."
    )
    base.add_numbers(
        doc,
        [
            "Inside backend, create a folder named banking.",
            "Inside banking, create a folder named management, and inside that create a folder named commands.",
            "Inside banking, create a folder named urls.",
            "Create the files below in their shown locations, then run makemigrations banking.",
        ],
    )
    add_code_file(doc, "backend/banking/__init__.py", "Marks the banking folder as a package.")
    add_code_file(doc, "backend/banking/apps.py", "Describes the banking app.")
    add_code_file(doc, "backend/banking/models.py", "The four tables: account, transaction, loan, notification.")
    add_code_file(doc, "backend/banking/services.py", "EMI maths, totals, categories, trends and the demo transaction list.")
    add_code_file(doc, "backend/banking/serializers.py", "Prepares banking data as JSON for the website.")
    add_code_file(doc, "backend/banking/views.py", "The customer web addresses such as dashboard and transactions.")
    add_code_file(doc, "backend/banking/admin_views.py", "The bank employee web addresses that see every customer.")
    add_code_file(doc, "backend/banking/urls/__init__.py", "Marks the urls folder as a package.")
    add_code_file(doc, "backend/banking/urls/customer_urls.py", "Customer web addresses.")
    add_code_file(doc, "backend/banking/urls/admin_urls.py", "Bank employee web addresses.")
    add_code_file(doc, "backend/banking/admin.py", "Shows the banking tables in the Django admin site.")
    add_code_file(doc, "backend/banking/tests.py", "Automatic tests for the banking endpoints.")
    add_check(
        doc,
        "The banking folder contains the files above and two sub folders. The services file is long, "
        "so paste it in one go rather than retyping it.",
    )

    doc.add_heading("Lesson 11. Create the banking API and the bank employee API", level=1)
    add_goal(doc, "Confirm how the web addresses in the banking app are wired to the code.")
    doc.add_paragraph(
        "You already pasted these files in Lesson 10, so this lesson is about understanding them "
        "rather than creating anything new. Read the two url files now: they are the map that turns a "
        "web address such as /api/transactions/ into the exact function that answers it."
    )
    base.add_table(
        doc,
        ["Address the website calls", "Which file answers it", "What comes back"],
        [
            ["/api/dashboard/", "banking/views.py", "Balances, income, expenses and chart data"],
            ["/api/transactions/", "banking/views.py", "A page of transactions after filtering"],
            ["/api/loans/", "banking/views.py", "The customer's loans, or a new application"],
            ["/api/emi/", "banking/views.py", "The EMI calculation for the numbers you typed"],
            ["/api/admin/analytics/", "banking/admin_views.py", "Totals for the whole pretend bank"],
            ["/api/admin/loans/<id>/", "banking/admin_views.py", "The loan after approving or rejecting it"],
        ],
        [5.4, 5.4, 6.4],
    )
    add_check(
        doc,
        "You can point at any address in the table and say which file answers it. That is the single "
        "most useful skill for reading any backend.",
    )

    doc.add_heading("Lesson 12. Create the demo data command", level=1)
    add_goal(doc, "Create the command that fills the pretend bank with three customers and their history.")
    doc.add_paragraph(
        "Typing test data by hand is slow, so Django lets you write a command you can run any time. "
        "This command creates the three customers, their accounts, twenty-eight transactions spread "
        "over three months, six loan applications, the notification list and one saved AI "
        "conversation."
    )
    doc.add_paragraph(
        "It is written so the demo numbers always match the script you will demonstrate: the balance "
        "is 85,450 rupees, monthly income is 45,000, monthly spending is 18,450, and the largest "
        "category is Shopping at 7,200. Running the command again with the flush option returns the "
        "project to exactly this state."
    )
    add_code_file(doc, "backend/banking/management/__init__.py", "An empty file inside the management folder.")
    add_code_file(doc, "backend/banking/management/commands/__init__.py", "An empty file inside the commands folder.")
    add_code_file(
        doc,
        "backend/banking/management/commands/seed_demo.py",
        "Inside the commands folder. This is the file you run to create all the pretend data.",
    )
    add_check(
        doc,
        "The path backend/banking/management/commands/seed_demo.py exists. The folder names matter: "
        "Django only finds commands placed exactly here.",
    )

    doc.add_heading("Lesson 13. Create the AI assistant app", level=1)
    add_goal(doc, "Create the chat feature and the service that answers banking questions.")
    doc.add_paragraph(
        "The AI assistant is the part of BankFlow that answers questions such as what is my balance. "
        "It works in three moves: it works out what you are asking, it looks up your own pretend "
        "data, and it writes a sentence from that data."
    )
    doc.add_paragraph(
        "The design decision that matters is that the wording and the numbers are separate. The "
        "numbers always come from the database, so the assistant can never invent a balance. If you "
        "later add an external AI key, the model only rephrases the same numbers; if you do not, the "
        "rule based answers you are about to paste handle everything offline."
    )
    base.add_numbers(
        doc,
        [
            "Inside backend, create a folder named assistant.",
            "Create the six files below, then run makemigrations assistant.",
        ],
    )
    add_code_file(doc, "backend/assistant/__init__.py", "Marks the assistant folder as a package.")
    add_code_file(doc, "backend/assistant/apps.py", "Describes the assistant app.")
    add_code_file(doc, "backend/assistant/models.py", "The chat message table that stores history.")
    add_code_file(
        doc,
        "backend/assistant/ai_service.py",
        "The heart of the feature: intents, data lookups, the rule based answers and the optional model call.",
    )
    add_code_file(doc, "backend/assistant/serializers.py", "Validates the question and formats saved messages.")
    add_code_file(doc, "backend/assistant/views.py", "The chat, history, suggestion and monitoring endpoints.")
    add_code_file(doc, "backend/assistant/urls.py", "The assistant web addresses.")
    add_code_file(doc, "backend/assistant/admin.py", "Shows saved conversations in the Django admin site.")
    add_code_file(doc, "backend/assistant/tests.py", "Automatic tests for every kind of question.")
    add_check(
        doc,
        "You now have three apps: users, banking and assistant. If any file is in the wrong folder, "
        "Django will report it in the next lesson.",
    )

    doc.add_heading("Lesson 14. Create the database and load the demo data", level=1)
    add_goal(doc, "Turn the models into real database tables and fill them with pretend bank data.")
    doc.add_paragraph(
        "Three commands finish the backend. The first prepares the instructions that build the "
        "tables, the second builds them, and the third fills them with the three fictional customers."
    )
    base.add_code(
        doc,
        "python manage.py makemigrations users banking assistant\n"
        "python manage.py migrate\n"
        "python manage.py seed_demo --flush",
    )
    doc.add_paragraph("The seed command ends by printing the logins you will use for the rest of the guide.")
    base.add_code(
        doc,
        "Seeded customer Mohammed Adnan\n"
        "Seeded customer Aisha Khan\n"
        "Seeded customer Rahul Verma\n"
        "\n"
        "Demo data ready.\n"
        "Admin    : admin@bankflow.com / Admin@12345\n"
        "Customer : mohammed@bankflow.com / Demo@12345\n"
        "Customer : aisha@bankflow.com / Demo@12345\n"
        "Customer : rahul@bankflow.com / Demo@12345",
    )
    add_check(
        doc,
        "You see those logins, and a file named db.sqlite3 appears inside backend. That file is your "
        "pretend bank. Write the logins down or leave this page open.",
    )

    doc.add_heading("Lesson 15. Run the backend tests", level=1)
    add_goal(doc, "Prove the backend behaves correctly with twenty-five automatic tests.")
    doc.add_paragraph(
        "Tests are small programs that check your work for you. BankFlow ships with twenty-five of "
        "them: they create their own temporary data, try the endpoints, and compare the answers with "
        "what should happen. Running them takes about half a minute and is the fastest way to know "
        "the backend is healthy."
    )
    base.add_code(doc, "python manage.py test")
    doc.add_paragraph("A healthy run ends like this.")
    base.add_code(
        doc,
        "Found 25 test(s).\n"
        "System check identified no issues (0 silenced).\n"
        ".........................\n"
        "----------------------------------------------------------------------\n"
        "Ran 25 tests in 31.331s\n"
        "\n"
        "OK",
    )
    add_note(
        doc,
        "If you see failures",
        "The most common cause is a file that was pasted with a missing line. Open the file named in "
        "the error message, compare it with the code in this guide, and run the tests again.",
    )
    add_check(
        doc,
        "The word OK appears at the end. This is a big moment: your backend is complete and correct, "
        "and you have not written a line of code yourself.",
    )

    doc.add_heading("Lesson 16. Start the backend and see your API working", level=1)
    add_goal(doc, "Run the backend server and watch it answer a real request.")
    doc.add_paragraph(
        "The API is now complete. Start the server and leave this terminal running for the rest of "
        "the guide."
    )
    base.add_code(doc, "python manage.py runserver 127.0.0.1:8000")
    doc.add_paragraph(
        "The terminal stops returning to the prompt and shows a line about watching for file changes. "
        "That means the server is running. Open your browser and visit these two addresses to see it "
        "answer."
    )
    base.add_code(
        doc,
        "http://127.0.0.1:8000/api/dashboard/\n"
        "http://127.0.0.1:8000/admin/",
    )
    add_note(
        doc,
        "Why the first address shows a login error",
        "The dashboard endpoint only answers someone who is logged in, and a browser tab is not "
        "logged in yet. That is the correct behaviour, and it proves the security is working. You "
        "will see the real data in the website in Lesson 23 and you can log into the admin address "
        "with admin@bankflow.com and Admin@12345.",
    )
    doc.add_paragraph(
        "To stop the server later, click in the terminal and press Ctrl+C. To run it again, type the "
        "same command. For now, keep it running."
    )
    add_check(
        doc,
        "The browser shows the Django admin login page at the second address, and you can log in with "
        "the admin account and see the three customers under Users.",
    )

    # -------------------------------------------------------------- part 3
    base.page_break(doc)
    doc.add_heading("Part 3. Build the website", level=1)
    doc.add_paragraph(
        "The website is the part your customer sees. It is built with React, which means the page "
        "runs in the browser and asks the backend for data when it needs it. Open a second terminal "
        "in VS Code for this part: click the plus sign at the top right of the terminal panel. Keep "
        "the backend terminal from Lesson 16 running in the first tab."
    )

    doc.add_heading("Lesson 17. Create the React website project", level=1)
    add_goal(doc, "Create the website project and download the ready made building blocks.")
    doc.add_paragraph(
        "The command below creates a React project with Vite inside your frontend folder. Vite is the "
        "tool that runs the website while you work and packages it at the end."
    )
    base.add_code(
        doc,
        "cd ..\n"
        "cd frontend\n"
        "npm create vite@latest . -- --template react\n"
        "npm install",
    )
    add_note(
        doc,
        "If the terminal asks about the current directory",
        "Answer yes to continue in the current folder. If it asks for a package name, press Enter to "
        "accept the default.",
    )
    doc.add_paragraph(
        "Now install the libraries BankFlow uses. Material UI provides the buttons, cards and tables; "
        "Recharts draws the charts; Axios talks to the backend; and React Router switches between "
        "pages."
    )
    base.add_code(
        doc,
        "npm install @mui/material @mui/icons-material @emotion/react @emotion/styled\n"
        "npm install axios react-router-dom recharts react-icons",
    )
    add_check(
        doc,
        "The terminal reports added packages with no error, and the sidebar now shows a frontend "
        "folder containing src, public and package.json. If npm is not recognised, see Lesson 27.",
    )

    doc.add_heading("Lesson 18. Create the website settings and theme", level=1)
    add_goal(doc, "Replace the starter files with the BankFlow settings, theme and page routes.")
    doc.add_paragraph(
        "Vite created a starter project with a demonstration page. You replace those files with the "
        "ones below. Two of them are worth a second look: the theme file holds every colour and "
        "font, so the whole website can be restyled from one place, and App.jsx lists every page and "
        "which web address shows it."
    )
    doc.add_paragraph(
        "When a lesson names a file that already exists, open it in the sidebar and replace all of "
        "its contents with the block shown, then save."
    )
    add_code_file(doc, "frontend/package.json", "Open the existing package.json and replace everything with this version.")
    add_code_file(doc, "frontend/vite.config.js", "Replace the existing file in the frontend folder.")
    add_code_file(doc, "frontend/index.html", "Replace the existing file in the frontend folder.")
    add_code_file(doc, "frontend/.env.example", "Create this new file in the frontend folder.")
    add_code_file(doc, "frontend/.gitignore", "Replace the existing file in the frontend folder.")
    add_code_file(doc, "frontend/public/bankflow.svg", "Replace the icon in the public folder.")
    add_code_file(doc, "frontend/src/index.css", "Replace the existing file in the src folder.")
    add_code_file(doc, "frontend/src/theme.js", "Create this new file in the src folder. It holds every colour and text style.")
    add_code_file(doc, "frontend/src/main.jsx", "Replace the existing file in the src folder.")
    add_code_file(doc, "frontend/src/App.jsx", "Replace the existing file in the src folder. It lists every page and address.")
    doc.add_paragraph("Copy the environment file so the website knows where the backend is.")
    base.add_code(doc, "copy .env.example .env      # cp .env.example .env on macOS or Linux")
    add_note(
        doc,
        "Delete the starter files you no longer need",
        "The React starter includes src/App.css and a folder called src/assets with a logo. You can "
        "delete both: right click them in the sidebar and choose Delete. BankFlow does not use them.",
    )
    add_check(
        doc,
        "The src folder contains main.jsx, App.jsx, theme.js and index.css, and the frontend folder "
        "contains index.html, vite.config.js, package.json, .env and the public folder.",
    )

    doc.add_heading("Lesson 19. Create the login state and API connection", level=1)
    add_goal(doc, "Create the single place that talks to the backend and remembers who is logged in.")
    doc.add_paragraph(
        "Every request in the website goes through one file, api.js. It attaches the login token to "
        "each request, renews the token automatically when it expires, and turns any failure into a "
        "sentence the screen can show. The auth context beside it remembers which user is logged in, "
        "so any page can ask who you are and whether you are a bank employee."
    )
    base.add_numbers(
        doc,
        [
            "Inside frontend/src, make sure these folders exist: services, context and utils. Create each one with a right click and New Folder.",
            "Create the files below in their shown folders, pasting the code and saving each one.",
        ],
    )
    add_code_file(doc, "frontend/src/services/api.js", "Inside src/services. The single connection to the backend.")
    add_code_file(doc, "frontend/src/services/authService.js", "Inside src/services. Register, login and profile calls.")
    add_code_file(doc, "frontend/src/services/bankingService.js", "Inside src/services. Dashboard, transactions, loans and notifications.")
    add_code_file(doc, "frontend/src/services/aiService.js", "Inside src/services. Assistant chat and history calls.")
    add_code_file(doc, "frontend/src/services/adminService.js", "Inside src/services. Bank employee data calls.")
    add_code_file(doc, "frontend/src/context/AuthContext.jsx", "Inside src/context. Remembers the logged in user.")
    add_code_file(doc, "frontend/src/utils/formatCurrency.js", "Inside src/utils. Formats rupees and dates the same way everywhere.")
    add_code_file(doc, "frontend/src/utils/calculations.js", "Inside src/utils. Calculates EMI instantly as you move a slider.")
    add_check(
        doc,
        "src now contains the three new folders. Nothing to run yet; the next lesson adds the visible "
        "parts of the pages.",
    )

    doc.add_heading("Lesson 20. Create the shared components", level=1)
    add_goal(doc, "Create the reusable pieces that appear on many pages.")
    doc.add_paragraph(
        "A component is a piece of a page you write once and reuse. The sidebar, the top bar, the "
        "statistic cards, the transaction table and the chat bubble are all components, which is why "
        "every page looks consistent and why changing one file updates the whole website."
    )
    base.add_numbers(
        doc,
        [
            "Inside frontend/src, create a folder named components.",
            "Create the nine files below inside it, pasting and saving each one.",
        ],
    )
    add_code_file(doc, "frontend/src/components/AppLayout.jsx", "The frame around every private page: sidebar, top bar and content area.")
    add_code_file(doc, "frontend/src/components/Navbar.jsx", "The top bar with the page title, notifications and your profile menu.")
    add_code_file(doc, "frontend/src/components/Sidebar.jsx", "The navigation list, which collapses on small screens.")
    add_code_file(doc, "frontend/src/components/DashboardCard.jsx", "One statistic card, used four times on the dashboard.")
    add_code_file(doc, "frontend/src/components/TransactionTable.jsx", "The transaction table, used by customers and employees.")
    add_code_file(doc, "frontend/src/components/LoanCard.jsx", "One loan summary card with a repayment progress bar.")
    add_code_file(doc, "frontend/src/components/ChatMessage.jsx", "One chat bubble, used for your question and the assistant's reply.")
    add_code_file(doc, "frontend/src/components/ProtectedRoute.jsx", "Sends visitors to the login page when a page needs a login.")
    add_code_file(doc, "frontend/src/components/Common.jsx", "Small helpers used everywhere: loader, error message, empty state, status label.")
    add_check(
        doc,
        "The components folder holds nine files. If any file name has a capital letter missing, the "
        "next lesson will fail to find it, so check the names now.",
    )

    doc.add_heading("Lesson 21. Create the customer pages", level=1)
    add_goal(doc, "Create the fourteen pages your customer can visit.")
    doc.add_paragraph(
        "These pages turn API data into screens. The table shows what each page is for and which "
        "backend address it calls, which is the pattern to notice: a page fetches data in the "
        "background, stores it in state, and renders it."
    )
    base.add_table(
        doc,
        ["Page file", "What the customer sees", "Backend address it calls"],
        [
            ["Landing.jsx", "The public introduction page with the hero and features", "none"],
            ["Login.jsx", "The login form with the demo accounts", "/api/auth/login/"],
            ["Register.jsx", "The registration form", "/api/auth/register/"],
            ["Dashboard.jsx", "Balance, income, expenses, loans and four charts", "/api/dashboard/"],
            ["Account.jsx", "Account number with the middle hidden, type and status", "/api/account/"],
            ["Transactions.jsx", "The searchable, filterable transaction list", "/api/transactions/"],
            ["TransactionDetails.jsx", "One transaction in full", "/api/transactions/<id>/"],
            ["Loans.jsx", "Loans and the application form with a live EMI preview", "/api/loans/"],
            ["LoanDetails.jsx", "One loan with its repayment schedule", "/api/loans/<id>/"],
            ["EMICalculator.jsx", "Slider based EMI calculator", "/api/emi/"],
            ["AIAssistant.jsx", "The chat screen with history", "/api/assistant/chat/"],
            ["Notifications.jsx", "Alerts, read and unread", "/api/notifications/"],
            ["Profile.jsx", "Your details, editable", "/api/profile/"],
            ["NotFound.jsx", "A friendly message for unknown addresses", "none"],
        ],
        [4.0, 7.4, 5.8],
    )
    base.add_numbers(
        doc,
        [
            "Inside frontend/src, create a folder named pages.",
            "Create the fourteen files below inside it.",
        ],
    )
    add_code_file(doc, "frontend/src/pages/Landing.jsx", "The first page a visitor sees.")
    add_code_file(doc, "frontend/src/pages/Login.jsx", "Logging in and remembering the token.")
    add_code_file(doc, "frontend/src/pages/Register.jsx", "Creating a new pretend customer.")
    add_code_file(doc, "frontend/src/pages/Dashboard.jsx", "The main screen after logging in.")
    add_code_file(doc, "frontend/src/pages/Account.jsx", "The account details page.")
    add_code_file(doc, "frontend/src/pages/Transactions.jsx", "The transaction list with filters.")
    add_code_file(doc, "frontend/src/pages/TransactionDetails.jsx", "A single transaction.")
    add_code_file(doc, "frontend/src/pages/Loans.jsx", "Loans and the application form.")
    add_code_file(doc, "frontend/src/pages/LoanDetails.jsx", "A single loan and its schedule.")
    add_code_file(doc, "frontend/src/pages/EMICalculator.jsx", "The EMI calculator.")
    add_code_file(doc, "frontend/src/pages/AIAssistant.jsx", "The chat assistant.")
    add_code_file(doc, "frontend/src/pages/Notifications.jsx", "The alerts page.")
    add_code_file(doc, "frontend/src/pages/Profile.jsx", "The profile page.")
    add_code_file(doc, "frontend/src/pages/NotFound.jsx", "The page for unknown addresses.")
    add_check(
        doc,
        "The pages folder holds fourteen files. Landing.jsx, Dashboard.jsx and AIAssistant.jsx are "
        "the longest; paste them in one go and save.",
    )

    doc.add_heading("Lesson 22. Create the bank employee pages", level=1)
    add_goal(doc, "Create the six pages that only the bank employee account can open.")
    doc.add_paragraph(
        "These pages read the employee endpoints, which return data for every customer. The route "
        "guard from Lesson 20 sends ordinary customers back to their own dashboard if they try to "
        "open an employee address, and the backend refuses the request as well, so the protection "
        "exists in both places."
    )
    base.add_numbers(
        doc,
        [
            "Inside frontend/src/pages, create a folder named admin.",
            "Create the six files below inside that folder.",
        ],
    )
    add_code_file(doc, "frontend/src/pages/admin/AdminDashboard.jsx", "Six totals, portfolio charts and the top customers table.")
    add_code_file(doc, "frontend/src/pages/admin/CustomerManagement.jsx", "The customer table and the customer detail dialog.")
    add_code_file(doc, "frontend/src/pages/admin/TransactionManagement.jsx", "Every customer's transactions with filters.")
    add_code_file(doc, "frontend/src/pages/admin/LoanManagement.jsx", "Approve, activate or reject a loan application.")
    add_code_file(doc, "frontend/src/pages/admin/AdminAnalytics.jsx", "The charts that summarise the whole pretend bank.")
    add_code_file(doc, "frontend/src/pages/admin/AIMonitor.jsx", "What customers asked the assistant and how it answered.")
    add_check(
        doc,
        "All twenty pages now exist, fourteen in pages and six in pages/admin. Part 3 is nearly done.",
    )

    doc.add_heading("Lesson 23. Start the website and click through it", level=1)
    add_goal(doc, "Run the website and confirm it really works.")
    doc.add_paragraph(
        "In your second terminal, which should be inside the frontend folder, start the website."
    )
    base.add_code(doc, "npm run dev")
    doc.add_paragraph(
        "The terminal prints a Local address. Open it in your browser; it is usually "
        "http://localhost:5173. Keep both terminals running: one serves the backend, one serves the "
        "website."
    )
    base.add_numbers(
        doc,
        [
            "The landing page appears with the headline Your Smarter Digital Banking Experience.",
            "Click Login, then click the demo customer line to fill the form, and press Login.",
            "The dashboard appears with a balance of 85,450 rupees, income of 45,000 and spending of 18,450.",
            "Open the AI Assistant from the sidebar and ask: What is my balance?",
            "The assistant answers with the same 85,450 figure, because it reads the same database.",
        ],
    )
    add_check(
        doc,
        "The dashboard shows four cards and four charts, and the assistant answers your question. "
        "Congratulations: you have built and run a complete full stack application.",
    )
    add_note(
        doc,
        "If the page loads but every request fails",
        "Make sure the backend terminal from Lesson 16 is still running. The website cannot show data "
        "without it.",
    )

    # -------------------------------------------------------------- part 4
    base.page_break(doc)
    doc.add_heading("Part 4. Learn by doing", level=1)
    doc.add_paragraph(
        "The application now works. This part turns it into a learning tool: you will walk every "
        "screen, change things and watch the result, and trace what happens between a click and a "
        "database record."
    )

    doc.add_heading("Lesson 24. Guided tour of every screen", level=1)
    add_goal(doc, "See every feature the project contains, in the order you would demonstrate it.")
    base.add_table(
        doc,
        ["Screen", "What to do there", "What it teaches"],
        [
            ["Landing page", "Scroll through the hero, features, assistant preview and security sections",
             "How a public page is composed from components"],
            ["Login", "Click the demo customer line to autofill, then log in",
             "Tokens, form validation and redirects by role"],
            ["Dashboard", "Read the four cards, then switch the chart tabs",
             "Turning one API response into cards and charts"],
            ["Account", "Look at the hidden middle of the account number",
             "Never showing the full number, even in a demo"],
            ["Transactions", "Search for Swiggy, then filter to Shopping",
             "Filtering, paging and totals on the server"],
            ["Transaction details", "Open any row",
             "Passing an id in the address and loading one record"],
            ["Loans", "Open the application form and watch the EMI change as you type",
             "Calculating on the spot and saving a new record"],
            ["Loan details", "Read the repayment schedule table",
             "Turning a loan into an instalment plan"],
            ["EMI calculator", "Move the sliders",
             "Maths in the browser, verified by the backend"],
            ["AI assistant", "Ask three questions, then open the history panel",
             "Intents, saved conversations and grounded answers"],
            ["Notifications", "Mark one as read, then mark all as read",
             "Updating a single record from the interface"],
            ["Profile", "Change your phone number and save",
             "Editing your own data with permission checks"],
            ["Admin dashboard", "Log in as admin@bankflow.com and open it",
             "Role based access and portfolio level totals"],
            ["Loan management", "Approve the pending loan",
             "An action that changes data and notifies the customer"],
            ["AI monitoring", "Read the questions saved from your own chat",
             "How a feature can be observed by an operator"],
        ],
        [3.6, 7.4, 6.2],
    )
    add_check(
        doc,
        "You have visited every screen once. You now know the whole application, not just the parts "
        "this guide made you paste.",
    )

    doc.add_heading("Lesson 25. Change something and watch it update", level=1)
    add_goal(doc, "Make four small changes so you feel how the pieces connect.")
    doc.add_paragraph(
        "Change one thing at a time, save the file, and look at the browser. The website reloads by "
        "itself when you save a frontend file, and the backend reloads when you save a backend file."
    )
    doc.add_paragraph("Exercise 1. Change the brand colour. Open frontend/src/theme.js.")
    base.add_code(
        doc,
        "// find this line inside palette.primary\n"
        "main: \"#1b3a8f\",\n"
        "\n"
        "// replace the colour with another one, for example\n"
        "main: \"#0f766e\",",
    )
    add_check(doc, "Save the file and watch the buttons, sidebar highlights and chart accents turn teal within a second.")

    doc.add_paragraph(
        "Exercise 2. Change the demo balance. Open "
        "backend/banking/management/commands/seed_demo.py and find the line shown below near the "
        "beginning of the transaction section."
    )
    base.add_code(doc, "target_balance = 85450.0      # change to 100000.0 and save")
    doc.add_paragraph(
        "Now rebuild the demo data in the backend terminal and refresh the dashboard."
    )
    base.add_code(doc, "python manage.py seed_demo --flush")
    add_check(
        doc,
        "The dashboard balance changes to 100,000 rupees, and the assistant answers with the same "
        "new figure. That is the single source of truth working: one number, many screens.",
    )

    doc.add_paragraph(
        "Exercise 3. Teach the assistant a new word. Open backend/assistant/ai_service.py and find "
        "the account_balance entry in INTENT_KEYWORDS."
    )
    base.add_code(
        doc,
        "\"account_balance\": [\"balance\", \"how much money\", \"account balance\", \"available amount\"],\n"
        "\n"
        "// add one more phrase inside the list, for example\n"
        "\"account_balance\": [\"balance\", \"how much money\", \"account balance\", \"available amount\", \"kitna paisa\"],",
    )
    add_check(
        doc,
        "Save, then ask the assistant kitna paisa in the chat. It now understands the phrase and "
        "answers with your balance.",
    )

    doc.add_paragraph(
        "Exercise 4. Change a welcome message. Open frontend/src/pages/Dashboard.jsx and find the "
        "PageHeader title line near the top of the returned page."
    )
    base.add_code(doc, "title={`${greeting()}, ${firstName}`}", )
    doc.add_paragraph(
        "Change it to a message of your own, for example title={`Welcome back, ${firstName}`}, save, "
        "and look at the dashboard heading."
    )
    add_check(
        doc,
        "All four changes worked. You have now edited the theme, the data, the AI behaviour and a "
        "page, which are the four places most changes in a project like this happen.",
    )

    doc.add_heading("Lesson 26. How a click becomes a database record", level=1)
    add_goal(doc, "Follow one request from the button you click to the data that comes back.")
    doc.add_paragraph(
        "Understanding this chain is the difference between copying code and being able to build your "
        "own features. Follow the numbers in the diagram below, then read the walkthrough."
    )
    base.add_code(
        doc,
        "1  You click View Transactions in the browser\n"
        "2  React Router shows the pages/Transactions.jsx component for the address /transactions\n"
        "3  The component runs its useEffect and calls bankingService.getTransactions(filters)\n"
        "4  services/api.js attaches your login token and sends the request to the backend\n"
        "5  Django matches /api/transactions/ in banking/urls/customer_urls.py\n"
        "6  TransactionListView in banking/views.py reads the filters, builds a database query\n"
        "7  Django's ORM turns the query into SQL and SQLite returns the matching rows\n"
        "8  TransactionSerializer turns each row into JSON\n"
        "9  The JSON travels back and React stores it in state with setData\n"
        "10 The table on screen re-renders with your rows",
    )
    base.add_numbers(
        doc,
        [
            "Front end means the code running in the browser: React, the pages, the components and the charts.",
            "Back end means the code running in Python: the views, the serializers, the models and the database.",
            "The API is the agreement between them: fixed web addresses that accept and return JSON.",
            "A model describes a table; a serializer shapes it; a view decides who may see it. Almost every feature you build later follows the same three steps.",
            "To add a new screen, you add a view, a web address, a service call and a page. Nothing else changes.",
        ],
    )
    add_check(
        doc,
        "You can explain to somebody else what happens between clicking a filter and seeing fewer "
        "rows.",
    )

    doc.add_heading("Lesson 27. Errors you will meet and how to fix them", level=1)
    add_goal(doc, "Recognise the most common beginner errors and repair them quickly.")
    doc.add_paragraph(
        "Every developer meets these messages. They are not a sign that you are doing something "
        "wrong; they are the tools telling you exactly what to fix."
    )
    base.add_table(
        doc,
        ["Message you see", "What it means", "How to fix it"],
        [
            ["python is not recognized", "Python is not on the system path", "Reinstall Python and tick Add python.exe to PATH"],
            ["pip is not recognized", "The virtual environment is not switched on", "Run venv\\Scripts\\activate, then try again"],
            ["npm is not recognized", "Node.js is not installed or needs a new terminal", "Reinstall Node.js LTS and open a fresh terminal"],
            ["running scripts is disabled on this system", "Windows blocks the activation script", "Run: Set-ExecutionPolicy RemoteSigned -Scope CurrentUser, answer Yes, then activate again"],
            ["No module named django", "The environment is off or packages are missing", "Activate venv, then pip install -r requirements.txt"],
            ["manage.py not found", "The terminal is in the wrong folder", "Run cd backend and try again"],
            ["No such table: banking_transaction", "The database tables were never created", "Run python manage.py migrate, then seed_demo --flush"],
            ["Port 8000 is already in use", "The backend is already running elsewhere", "Use the running one, or runserver 127.0.0.1:8001 and update frontend/.env"],
            ["EADDRINUSE port 5173", "The website is already running in another terminal", "Use the existing window, or stop it with Ctrl+C first"],
            ["Cannot find module or Failed to resolve import", "A file name or folder does not match", "Check the capitals and the folder path against this guide"],
            ["Red banner saying the API cannot be reached", "The backend terminal is not running", "Start the backend with runserver and refresh the page"],
            ["CORS policy error in the browser", "The website address is not allowed by the backend", "Check CORS_ALLOWED_ORIGINS in backend/.env includes http://localhost:5173"],
            ["401 Unauthorized on every request", "The login token has expired", "Log out and log in again"],
            ["The page is blank with an error in the terminal", "A syntax error in the last file you edited", "Read the file name and line number in the message and compare that file with this guide"],
            ["npm install stops with a blocked scripts warning", "The package manager blocked esbuild", "Run npm install-scripts approve esbuild, then npm install"],
        ],
        [5.0, 5.2, 7.0],
    )
    add_note(
        doc,
        "The habit that fixes most problems",
        "Read the first line of the error message, then look at the file name it mentions. Nine times "
        "out of ten the answer is a missing line, a wrong folder or a server that is not running.",
    )
    add_check(doc, "You know where to look when something breaks instead of starting again from scratch.")

    doc.add_heading("Lesson 28. Stop, start and restart everything", level=1)
    add_goal(doc, "Keep the project easy to pick up after a break.")
    doc.add_paragraph("Use these commands whenever you return to the project on a new day.")
    base.add_code(
        doc,
        "# stop anything running: click in the terminal and press\n"
        "Ctrl + C\n"
        "\n"
        "# start the backend (terminal 1)\n"
        "cd banking_app/backend\n"
        "venv\\Scripts\\activate\n"
        "python manage.py runserver 127.0.0.1:8000\n"
        "\n"
        "# start the website (terminal 2)\n"
        "cd banking_app/frontend\n"
        "npm run dev\n"
        "\n"
        "# if the demo data ever looks wrong\n"
        "cd banking_app/backend\n"
        "venv\\Scripts\\activate\n"
        "python manage.py seed_demo --flush",
    )
    base.add_table(
        doc,
        ["Address", "What it shows", "Who can open it"],
        [
            ["http://localhost:5173", "The website", "Everyone"],
            ["http://127.0.0.1:8000/api/", "The API", "Logged in accounts only"],
            ["http://127.0.0.1:8000/admin/", "Django admin for the pretend data", "The admin account"],
        ],
        [5.4, 6.6, 5.2],
    )
    add_check(
        doc,
        "You can start, stop and reset the project without re-reading the whole guide.",
    )

    doc.add_heading("Lesson 29. What to learn next", level=1)
    add_goal(doc, "Turn this project into a learning path.")
    base.add_numbers(
        doc,
        [
            "Change one screen at a time. Pick the notifications page, add a filter for the notification type, and follow the chain from view to serializer to service to page.",
            "Add a new field. Add a nickname to the customer profile in backend/users/models.py, run makemigrations and migrate, expose it in the serializer, then show it on the profile page.",
            "Add a new endpoint. Build /api/spending-by-month/ that returns one number per month, then draw it as a new chart on the dashboard.",
            "Improve the assistant. Add intents for questions such as which month did I spend the most, and reuse the helpers in services.py instead of writing new maths.",
            "Learn Git. Put the project in a repository so you can see your own history and try changes safely.",
            "Learn testing. Add a test for every new feature you build, following the style of the existing tests.",
            "Learn deployment. Put the backend on a host such as Render or Railway and the website on a static host such as Netlify or Vercel, then update VITE_API_BASE_URL.",
            "Read the code you already have. Every file in this guide is written to be read, and the comments explain the decisions rather than repeating the code.",
        ],
    )
    add_check(
        doc,
        "You have a project you understand, a habit of checking your work, and a list of next steps. "
        "That is what finishing a first full stack project looks like.",
    )

    # ------------------------------------------------------------- appendices
    base.page_break(doc)
    doc.add_heading("Appendix A. Plain English word list", level=1)
    doc.add_paragraph(
        "Every word below appears in this guide. Keep this page nearby when a term feels unfamiliar."
    )
    base.add_table(
        doc,
        ["Word", "What it means in plain English"],
        [
            ["Terminal", "The text window where you type commands. In VS Code it opens at the bottom of the screen."],
            ["Command", "One line of instruction typed in the terminal and run with Enter."],
            ["Folder and path", "A folder stores files; a path is the address of a file, such as backend/config/settings.py."],
            ["VS Code", "The free editor from Microsoft where you create files and run commands."],
            ["Extension", "An add on for VS Code that adds features such as Python support."],
            ["Virtual environment", "A private box of Python libraries belonging to one project."],
            ["Package or library", "Ready made code written by somebody else that your project uses."],
            ["pip", "The Python tool that downloads packages."],
            ["npm", "The Node.js tool that downloads packages for the website."],
            ["Node.js", "The program that runs the website building tools."],
            ["Django", "The Python framework that provides the backend structure."],
            ["React", "The JavaScript library that builds the screens in the browser."],
            ["Vite", "The tool that runs the website while you work and builds the final version."],
            ["Component", "A reusable piece of a screen, such as a button or a card."],
            ["Prop", "A value you pass into a component so it can display something."],
            ["State", "Data a screen keeps in memory while it is open, such as the list of transactions."],
            ["Hook", "A React function that lets a component remember things or run code at the right moment."],
            ["API", "The set of web addresses your backend answers, and the JSON it exchanges."],
            ["Endpoint", "One of those web addresses, for example /api/dashboard/."],
            ["Request and response", "The message the website sends and the message the backend sends back."],
            ["JSON", "A simple text format for structured data, which both sides understand."],
            ["JWT or token", "A signed pass that proves you are logged in; the website sends it with each request."],
            ["Model", "A description of a database table, written in Python."],
            ["Migration", "A file that tells the database how to create or change tables."],
            ["ORM", "The part of Django that lets you work with database rows using Python instead of SQL."],
            ["Serializer", "The code that turns database rows into JSON and checks incoming data."],
            ["View", "The function that decides what to answer for one web address."],
            ["CORS", "The browser rule that decides which website addresses may call the backend."],
            ["Seed data", "Pretend rows created by a command so the app has something to show."],
            ["Build", "Packaging the website into final files for hosting."],
            ["localhost and port", "Your own computer, and the numbered channel such as 8000 or 5173 that a program listens on."],
        ],
        [4.0, 13.2],
    )

    doc.add_heading("Appendix B. Every file and what it does", level=1)
    doc.add_paragraph(
        "The manifest lists all ninety-two files in the project with their purpose and length, "
        "including the generated ones explained in the note below the table."
    )
    manifest = []
    for rel_path, purpose in base.MANIFEST:
        path = ROOT / rel_path
        lines = len(path.read_text(encoding="utf-8").splitlines()) if path.exists() else 0
        manifest.append([rel_path, purpose, str(lines)])
    base.add_table(
        doc,
        ["Path", "What it does", "Lines"],
        manifest,
        [6.4, 9.0, 1.8],
        font_size=Pt(8.5),
        header_size=Pt(8.5),
    )
    doc.add_paragraph(
        "Generated files that you never paste by hand: db.sqlite3 is the database created by "
        "migrate, the migrations folders are created by makemigrations, node_modules and "
        "package-lock.json are created by npm install, and dist is created by npm run build. The two "
        "environment files are copies of the .env.example files."
    )

    doc.add_heading("Appendix C. Logins and the demo script", level=1)
    base.add_table(
        doc,
        ["Role", "Email", "Password", "What it shows"],
        [
            ["Customer", "mohammed@bankflow.com", "Demo@12345", "Balance 85,450, income 45,000, spending 18,450, two loans"],
            ["Customer", "aisha@bankflow.com", "Demo@12345", "A second customer with different loans"],
            ["Customer", "rahul@bankflow.com", "Demo@12345", "A third customer with a pending loan"],
            ["Bank employee", "admin@bankflow.com", "Admin@12345", "The employee area and monitoring"],
        ],
        [3.0, 5.2, 3.0, 6.0],
    )
    doc.add_paragraph("Use this sequence when you show the project to somebody else.")
    base.add_numbers(
        doc,
        [
            "Landing page: the hero, the six features and the assistant preview.",
            "Log in as the demo customer and land on the dashboard.",
            "Read the four cards, then switch the chart tabs.",
            "Open the account page and point out the hidden account number.",
            "Filter the transactions, then open one transaction in full.",
            "Open the loans page and submit an application with the live EMI preview.",
            "Open the EMI calculator and move the sliders.",
            "Ask the assistant five questions, then open the history panel.",
            "Mark a notification as read.",
            "Log in as the bank employee, approve the pending loan, then open analytics and AI monitoring.",
        ],
    )

    doc.add_heading("Appendix D. The API in one table", level=1)
    doc.add_paragraph(
        "Every address below returns JSON. All of them need a login token except register, login and "
        "refresh, and the employee addresses also require the bank employee role."
    )
    base.add_table(
        doc,
        ["Method", "Address", "What it does"],
        [
            ["POST", "/api/auth/register/", "Create a new pretend customer"],
            ["POST", "/api/auth/login/", "Log in and receive your tokens"],
            ["POST", "/api/auth/refresh/", "Renew an expired token"],
            ["GET, PUT", "/api/profile/", "Read or update your details"],
            ["GET", "/api/dashboard/", "Everything the dashboard shows"],
            ["GET", "/api/account/", "Your masked account details"],
            ["GET", "/api/transactions/", "Your transactions with filters and paging"],
            ["GET", "/api/transactions/<id>/", "One transaction"],
            ["GET, POST", "/api/loans/", "Your loans, or a new application"],
            ["GET", "/api/loans/<id>/", "One loan"],
            ["POST", "/api/emi/", "Calculate an EMI"],
            ["GET", "/api/notifications/", "Your notifications"],
            ["PUT", "/api/notifications/<id>/", "Mark one as read"],
            ["POST", "/api/notifications/read-all/", "Mark all as read"],
            ["POST", "/api/assistant/chat/", "Ask the assistant a question"],
            ["GET, DELETE", "/api/assistant/history/", "Read or clear your chat history"],
            ["GET", "/api/admin/analytics/", "Employee totals and charts"],
            ["GET", "/api/admin/customers/", "Employee customer table"],
            ["GET", "/api/admin/transactions/", "Employee transaction table"],
            ["GET", "/api/admin/loans/", "Employee loan table"],
            ["PATCH", "/api/admin/loans/<id>/", "Approve, activate or reject a loan"],
            ["GET", "/api/assistant/monitor/", "Assistant monitoring for employees"],
        ],
        [2.4, 6.4, 8.4],
    )

    doc.save(OUTPUT)
    print(f"wrote {OUTPUT}")


def main() -> None:
    page_map = {}
    if len(sys.argv) > 1:
        page_map = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8-sig"))
    build(page_map)


if __name__ == "__main__":
    main()
```

### tools/build_easy_docx.py

```python
#!/usr/bin/env python3
"""Build the very easy edition of the BankFlow guide.

Written for a first-time learner: short sentences, one action per numbered step,
a plain language reason for every step, and a check after each lesson. The complete
program is included, exactly as in the other editions.

Usage: python build_easy_docx.py [page-map.json]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import build_bankflow_docx as base  # noqa: E402

from docx import Document  # noqa: E402
from docx.enum.text import WD_TAB_ALIGNMENT, WD_TAB_LEADER  # noqa: E402
from docx.shared import Cm, Pt  # noqa: E402

ROOT = base.ROOT
OUTPUT = ROOT / "BankFlow-Very-Easy-Guide-with-Full-Code.docx"


# --------------------------------------------------------------------------- #
# small helpers that keep every lesson looking the same
# --------------------------------------------------------------------------- #
def one_line(doc, text: str) -> None:
    paragraph = doc.add_paragraph()
    paragraph.paragraph_format.space_after = Pt(6)
    run = paragraph.add_run("In one line: ")
    run.bold = True
    paragraph.add_run(text)


def needs(doc, text: str) -> None:
    paragraph = doc.add_paragraph()
    paragraph.paragraph_format.space_after = Pt(8)
    run = paragraph.add_run("What you need: ")
    run.bold = True
    paragraph.add_run(text)


def steps(doc, items) -> None:
    for index, item in enumerate(items, start=1):
        paragraph = doc.add_paragraph()
        paragraph.paragraph_format.space_after = Pt(4)
        paragraph.paragraph_format.left_indent = Cm(0.6)
        paragraph.paragraph_format.first_line_indent = Cm(-0.6)
        run = paragraph.add_run(f"{index}. ")
        run.bold = True
        paragraph.add_run(item)


def see(doc, text: str) -> None:
    paragraph = doc.add_paragraph()
    paragraph.paragraph_format.space_before = Pt(2)
    paragraph.paragraph_format.space_after = Pt(6)
    run = paragraph.add_run("You should see: ")
    run.bold = True
    paragraph.add_run(text)


def done(doc, text: str) -> None:
    paragraph = doc.add_paragraph()
    paragraph.paragraph_format.space_before = Pt(2)
    paragraph.paragraph_format.space_after = Pt(10)
    run = paragraph.add_run("Done when: ")
    run.bold = True
    paragraph.add_run(text)


def problems(doc, text: str) -> None:
    paragraph = doc.add_paragraph()
    paragraph.paragraph_format.space_after = Pt(10)
    run = paragraph.add_run("If it does not work: ")
    run.bold = True
    paragraph.add_run(text)


def new_words(doc, items) -> None:
    paragraph = doc.add_paragraph()
    paragraph.paragraph_format.space_after = Pt(4)
    paragraph.add_run("New words in this lesson:").bold = True
    for word, meaning in items:
        line = doc.add_paragraph(style="List Bullet")
        line.paragraph_format.space_after = Pt(2)
        run = line.add_run(f"{word} - ")
        run.bold = True
        line.add_run(meaning)


def command(doc, text: str, what: str = "") -> None:
    if what:
        paragraph = doc.add_paragraph()
        paragraph.paragraph_format.space_after = Pt(2)
        paragraph.add_run(what).italic = True
    base.add_code(doc, text)


def code_file(doc, rel_path: str, where: str, what: str) -> None:
    doc.add_heading(rel_path, level=3)
    line = doc.add_paragraph(style="FileNote")
    line.add_run("Where it goes: ")
    line.add_run(where)
    line2 = doc.add_paragraph(style="FileNote")
    line2.add_run("What it does: ")
    line2.add_run(what)
    line3 = doc.add_paragraph(style="FileNote")
    line3.add_run(
        "Copy the whole block below without changing anything. In VS Code click at the start of the "
        "first line, drag to the last line, press Ctrl+C, then paste it into your new file with Ctrl+V."
    )
    base.add_code(doc, (ROOT / rel_path).read_text(encoding="utf-8"))


def build(page_map: dict) -> None:
    doc = Document()
    base.configure_styles(doc)
    doc.styles["Normal"].font.size = Pt(12)
    doc.styles["Normal"].paragraph_format.space_after = Pt(8)
    doc.styles["Normal"].paragraph_format.line_spacing = 1.2
    code_style = doc.styles["CodeBlock"]
    code_style.font.size = Pt(8)
    code_style.paragraph_format.line_spacing = Pt(9.6)
    base.page_setup(doc)

    # -------------------------------------------------------------------- cover
    doc.add_paragraph("BankFlow Very Easy Guide Build Your First Website", style="Title")
    doc.add_paragraph(
        "This guide is for someone who has never made a website. It uses short sentences and one "
        "action at a time. If you can click, copy and paste, you can finish it."
    )
    doc.add_paragraph(
        "You will build a pretend bank called BankFlow. It has a login page, a dashboard with "
        "charts, a list of transactions, a loan form, an EMI calculator and a chat assistant that "
        "answers questions about your pretend money."
    )
    doc.add_paragraph(
        "The whole program is inside this book. You never write new code. You copy the code shown "
        "and you run the commands shown. That is how everyone starts."
    )

    doc.add_heading("The whole project in one picture", level=1)
    doc.add_paragraph(
        "Think of a bank branch. Customers stand in the lobby. Behind a counter, staff do the real "
        "work. Behind the staff there is a record room full of files."
    )
    base.add_table(
        doc,
        ["In the bank branch", "In our project", "What it is"],
        [
            ["The lobby customers see", "The website, called the frontend",
             "Pages and buttons that run inside your browser"],
            ["The counter where you ask", "The API",
             "Fixed web addresses that accept questions and give answers"],
            ["The staff behind the counter", "The backend, written in Python with Django",
             "It checks who you are and decides what to send back"],
            ["The record room", "The database, a file called db.sqlite3",
             "It stores the customers, transactions and loans"],
            ["A helpful clerk who reads your file", "The AI assistant",
             "It reads your own pretend data and answers in words"],
        ],
        [4.6, 5.8, 6.8],
    )
    doc.add_paragraph(
        "That is the whole idea. The website cannot see the record room directly. It must ask the "
        "counter, and the staff check that you are allowed to see the answer. Everything else in "
        "this book is detail."
    )

    doc.add_heading("Two ways to build this project", level=1)
    doc.add_paragraph(
        "Read both options and pick one. Both are honest ways to learn, and you can switch later."
    )
    doc.add_paragraph().add_run("Path A, the fast path.").bold = True
    doc.add_paragraph(
        "You already have a ready made folder of the project. Copy it to your laptop, install the "
        "tools in Lessons 1 to 6, then jump to Lesson 16 to start the backend and Lesson 24 to "
        "start the website. Use the rest of the book as a dictionary when you want to understand a "
        "file. This path takes about an hour and is the best choice if your goal is to see it work."
    )
    doc.add_paragraph().add_run("Path B, the learning path.").bold = True
    doc.add_paragraph(
        "You do every lesson in order and create all ninety-two files by copying them from this "
        "book. This takes longer, perhaps two or three evenings, but at the end you will have typed "
        "every part yourself and you will understand how a real project is put together. This is "
        "the path the book is written for."
    )

    doc.add_heading("Seven rules that make this easy", level=1)
    steps(
        doc,
        [
            "Do one lesson, then stop and do its check. Never continue with a red error on your screen.",
            "Copy code exactly, including brackets, commas and empty lines. Small typing differences cause most errors.",
            "Keep your folders matching the headings in this book. A file in the wrong folder is the second most common error.",
            "Use the terminal inside VS Code. It already knows which folder you are working in.",
            "When a command finishes, read its last line. That line tells you if it worked.",
            "Two programs must run at the same time later: the backend and the website. Keep both windows open.",
            "When you feel lost, look at the picture above and ask yourself: am I working on the lobby, the counter, the staff, or the record room?",
        ],
    )

    doc.add_heading("Contents", level=1)
    contents = [
        ("Part 1 Lesson 1. Install Visual Studio Code", "lesson1"),
        ("Part 1 Lesson 2. Install Python", "lesson2"),
        ("Part 1 Lesson 3. Install Node.js", "lesson3"),
        ("Part 1 Lesson 4. Add two VS Code extensions", "lesson4"),
        ("Part 1 Lesson 5. Learn five things in VS Code", "lesson5"),
        ("Part 1 Lesson 6. Make your folders", "lesson6"),
        ("Part 2 Lesson 7. What a backend is and which files it needs", "lesson7"),
        ("Part 2 Lesson 8. Turn on your private Python box", "lesson8"),
        ("Part 2 Lesson 9. Create four simple backend files", "lesson9"),
        ("Part 2 Lesson 10. Create the settings folder", "lesson10"),
        ("Part 2 Lesson 11. Create the users app for logging in", "lesson11"),
        ("Part 2 Lesson 12. Create the banking tables and the maths file", "lesson12"),
        ("Part 2 Lesson 13. Create the banking web addresses", "lesson13"),
        ("Part 2 Lesson 14. Create the pretend data command", "lesson14"),
        ("Part 2 Lesson 15. Create the AI assistant app", "lesson15"),
        ("Part 2 Lesson 16. Build the database and fill it with pretend data", "lesson16"),
        ("Part 2 Lesson 17. Run the tests and start the backend", "lesson17"),
        ("Part 3 Lesson 18. What a website is and how to create the project", "lesson18"),
        ("Part 3 Lesson 19. Create the website settings files", "lesson19"),
        ("Part 3 Lesson 20. Create the files that talk to the backend", "lesson20"),
        ("Part 3 Lesson 21. Create the shared pieces of every page", "lesson21"),
        ("Part 3 Lesson 22. Create the customer pages", "lesson22"),
        ("Part 3 Lesson 23. Create the bank employee pages", "lesson23"),
        ("Part 3 Lesson 24. Start the website and log in", "lesson24"),
        ("Part 4 Lesson 25. A tour of every screen", "lesson25"),
        ("Part 4 Lesson 26. Four easy changes you can make", "lesson26"),
        ("Part 4 Lesson 27. How a click becomes data", "lesson27"),
        ("Part 4 Lesson 28. When something goes wrong", "lesson28"),
        ("Part 4 Lesson 29. Stop, start and start again", "lesson29"),
        ("Part 4 Lesson 30. What to learn next", "lesson30"),
        ("Appendix A. Words explained simply", "appendixa"),
        ("Appendix B. Every file and what it does", "appendixb"),
        ("Appendix C. Logins and the demo script", "appendixc"),
        ("Appendix D. All the commands in one place", "appendixd"),
    ]
    for index, (label, key) in enumerate(contents, start=1):
        paragraph = doc.add_paragraph()
        paragraph.paragraph_format.space_after = Pt(2)
        paragraph.paragraph_format.tab_stops.add_tab_stop(
            Cm(17.2), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS
        )
        paragraph.add_run(f"{index}. {label}")
        page = page_map.get(key)
        if page:
            paragraph.add_run(f"\t{page}")

    base.page_break(doc)

    # ============================================================ part 1
    doc.add_heading("Part 1. Get your laptop ready", level=1)
    doc.add_paragraph(
        "You will install four programs. Two of them make the project run, one is the editor where "
        "you work, and one adds helpful features to that editor. Do them in this order."
    )
    doc.add_paragraph(
        "Each lesson takes ten to fifteen minutes. You only install these once. After today you "
        "will never repeat Part 1 on this laptop."
    )

    doc.add_heading("Lesson 1. Install Visual Studio Code", level=1)
    one_line(doc, "Put the editor on your laptop. This is where you write files and run commands.")
    needs(doc, "An internet connection and about ten minutes.")
    doc.add_paragraph(
        "Visual Studio Code is free. People call it VS Code. It has two parts you will use: a side "
        "list of your files, and a black panel at the bottom called the terminal."
    )
    steps(
        doc,
        [
            "Open your browser and go to code.visualstudio.com.",
            "Click the blue Download button for Windows.",
            "Open the file that was downloaded. Its name starts with VSCodeUserSetup.",
            "Click I accept the agreement, then click Next.",
            "Leave the folder as it is and click Next.",
            "Tick Add to PATH. Tick both boxes that start with Open with Code.",
            "Click Next, then Install, then Finish.",
            "VS Code opens. Close the Welcome tab with its small x.",
        ],
    )
    new_words(
        doc,
        [
            ("Editor", "The program where you write files. VS Code is your editor."),
            ("PATH", "A list that lets you start a program by typing its name in the terminal."),
        ],
    )
    see(doc, "An empty VS Code window with a Welcome tab, and a tall icon bar on the left.")
    done(doc, "VS Code is installed and open.")
    problems(doc, "Install it again and make sure Add to PATH is ticked.")

    doc.add_heading("Lesson 2. Install Python", level=1)
    one_line(doc, "Install the language that runs the backend, the staff behind the counter.")
    needs(doc, "About ten minutes. Read step 4 carefully, it matters.")
    steps(
        doc,
        [
            "Go to python.org/downloads.",
            "Click the yellow Download Python button.",
            "Open the downloaded file.",
            "On the first screen, tick the box at the bottom that says Add python.exe to PATH.",
            "Click Install Now and wait.",
            "Click Close when it finishes.",
            "Press the Windows key, type cmd, and press Enter. A black window opens.",
            "Type python --version and press Enter.",
        ],
    )
    command(doc, "python --version", "Type this in the black window.")
    see(doc, "A line like Python 3.14.5. The number can be newer.")
    done(doc, "Python prints a version number.")
    problems(
        doc,
        "If the window says python is not recognized, run the installer again, choose Modify, tick "
        "Add python.exe to PATH, and open a new black window.",
    )
    new_words(
        doc,
        [
            ("Python", "The language the backend is written in."),
            ("Terminal or command prompt", "The black text window where you type commands."),
        ],
    )

    doc.add_heading("Lesson 3. Install Node.js", level=1)
    one_line(doc, "Install the tool that builds the website in the browser.")
    needs(doc, "About ten minutes.")
    steps(
        doc,
        [
            "Go to nodejs.org.",
            "Click the button marked LTS. Do not pick Current.",
            "Open the downloaded file.",
            "Click Next through every screen. Keep the default folder.",
            "Leave the checkbox on the Tools for Native Modules screen empty.",
            "Click Install, wait, then click Finish.",
            "In the same black window type node --version and press Enter.",
            "Then type npm --version and press Enter.",
        ],
    )
    command(doc, "node --version\nnpm --version")
    see(doc, "Two version numbers, one after the other, such as v24.19.0 and 12.0.2.")
    done(doc, "Both commands print a number.")
    problems(doc, "Install Node.js again, then close the black window and open a new one.")
    new_words(
        doc,
        [
            ("Node.js", "A program that runs the tools which build the website."),
            ("npm", "The tool that downloads ready made code for the website."),
        ],
    )

    doc.add_heading("Lesson 4. Add two VS Code extensions", level=1)
    one_line(doc, "Teach VS Code about Python and about React, so it can highlight your code.")
    needs(doc, "VS Code open. About five minutes.")
    doc.add_paragraph(
        "Extensions are add ons. They colour your code, warn you about mistakes and keep the "
        "spacing tidy. The project works without them, but they make everything easier to read."
    )
    steps(
        doc,
        [
            "In VS Code press Ctrl+Shift+X. The Extensions panel opens on the left.",
            "Type Python in the search box. Find the one made by Microsoft and click Install.",
            "Clear the search box and type ES7 React snippets. Install the one with the most downloads.",
            "Clear the box again and type Prettier. Install the one made by Prettier.",
            "Press Ctrl+Shift+X again to close the panel.",
        ],
    )
    see(doc, "Each installed extension shows the word Installed and no Install button.")
    done(doc, "Three extensions are installed.")
    problems(doc, "Check your internet connection and try again.")

    doc.add_heading("Lesson 5. Learn five things in VS Code", level=1)
    one_line(doc, "Practise the only five actions this whole book needs.")
    needs(doc, "VS Code open. About ten minutes.")
    base.add_table(
        doc,
        ["What you want", "How to do it", "What happens"],
        [
            ["Open a folder", "Click File, then Open Folder, then choose your folder",
             "The folder name appears at the top of the left sidebar"],
            ["Make a new file", "Right click in the sidebar, click New File, type the name, press Enter",
             "A blank tab opens with that file name"],
            ["Save your work", "Press Ctrl+S",
             "The little dot on the file tab disappears"],
            ["Open the terminal", "Click Terminal, then New Terminal",
             "A panel opens at the bottom with a command line"],
            ["Run a command", "Click in the terminal, type the command, press Enter",
             "The terminal prints the result"],
        ],
        [4.2, 6.6, 6.4],
    )
    steps(
        doc,
        [
            "Open the folder you will create in the next lesson, using File then Open Folder.",
            "Right click in the sidebar and make a file called practice.txt.",
            "Type the word hello inside it and press Ctrl+S.",
            "Open the terminal with Terminal then New Terminal.",
            "Type dir and press Enter.",
        ],
    )
    see(doc, "The terminal lists your files, including practice.txt. You can delete that file afterwards.")
    done(doc, "You can open a folder, make a file, save it, open the terminal and run a command.")
    problems(doc, "Make sure you clicked inside the terminal panel before typing.")
    new_words(
        doc,
        [
            ("Sidebar", "The left list of files and folders in VS Code."),
            ("Terminal", "The panel at the bottom where commands are typed."),
        ],
    )

    doc.add_heading("Lesson 6. Make your folders", level=1)
    one_line(doc, "Create one main folder with two folders inside it.")
    needs(doc, "Two minutes.")
    steps(
        doc,
        [
            "Open File Explorer from the taskbar.",
            "Go to the place you keep your work, for example Documents.",
            "Right click an empty space, click New, then Folder, and name it banking_app.",
            "Open banking_app. Inside it make two folders: backend and frontend.",
            "Close File Explorer.",
            "In VS Code click File, then Open Folder, choose banking_app, and click Select Folder.",
            "If VS Code asks whether you trust the folder, click Yes, I trust the authors.",
        ],
    )
    doc.add_paragraph("Your sidebar should look like this.")
    base.add_code(doc, "BANKING_APP\n    backend\n    frontend")
    see(doc, "The sidebar shows banking_app with backend and frontend inside it.")
    done(doc, "Part 1 is finished. Your laptop now has every tool you need.")
    problems(doc, "Use File then Open Folder again and pick banking_app, not backend.")
    new_words(
        doc,
        [
            ("Folder", "A container for files. Ours is called banking_app."),
            ("backend and frontend", "The staff room and the lobby, in folder form."),
        ],
    )

    # ============================================================ part 2
    base.page_break(doc)
    doc.add_heading("Part 2. Build the backend", level=1)
    doc.add_paragraph(
        "The backend is the staff behind the counter. It stores the pretend money data and answers "
        "questions from the website. You build it first, because the website needs something to "
        "talk to."
    )
    doc.add_paragraph(
        "Everything in Part 2 happens in the VS Code terminal, and the terminal must be inside the "
        "backend folder. There are eight lessons. Each one is short."
    )

    doc.add_heading("Lesson 7. What a backend is and which files it needs", level=1)
    one_line(doc, "Understand the shape of the backend before you create it.")
    needs(doc, "Ten minutes of reading. No typing yet.")
    doc.add_paragraph(
        "Django is a ready made backend. It gives you a structure so you do not invent one. Inside "
        "the backend folder you will create three groups of files, called apps, plus one settings "
        "folder."
    )
    base.add_table(
        doc,
        ["Folder", "In plain words", "What it holds"],
        [
            ["config", "The instructions for the whole building",
             "Settings, web addresses and the start up files"],
            ["users", "The staff who check identity",
             "Logging in, roles, and customer details"],
            ["banking", "The staff who handle money records",
             "Accounts, transactions, loans and notifications"],
            ["assistant", "The helpful clerk who answers questions",
             "Saved conversations and the answering logic"],
        ],
        [3.2, 6.6, 7.4],
    )
    doc.add_paragraph(
        "A file named models.py describes a table in the record room. A file named views.py decides "
        "what to answer when somebody asks. A file named serializers.py turns a database row into "
        "text the website can read. Every app has these, which is why the same pattern repeats."
    )
    doc.add_paragraph(
        "Two files do the thinking. services.py holds the money maths, such as EMI and monthly "
        "totals. ai_service.py holds the question answering. Everything else is plumbing."
    )
    done(doc, "You can say what config, users, banking and assistant are for.")
    new_words(
        doc,
        [
            ("Django", "A ready made backend structure written in Python."),
            ("App", "A folder that groups related backend features."),
            ("Model", "A description of one table in the database."),
            ("View", "The code that answers one web address."),
        ],
    )

    doc.add_heading("Lesson 8. Turn on your private Python box", level=1)
    one_line(doc, "Create a private space for the project's Python libraries and install them.")
    needs(doc, "The backend folder open in VS Code. About fifteen minutes.")
    doc.add_paragraph(
        "Your laptop may have other Python projects. A virtual environment is a private box of "
        "libraries used only by BankFlow, so nothing clashes. You create it once."
    )
    doc.add_paragraph("Open the terminal in VS Code and type these two lines, pressing Enter after each.")
    command(doc, "cd backend\npython -m venv venv", "The first line moves you into the backend folder.")
    see(doc, "A new folder named venv appears inside backend in the sidebar.")
    doc.add_paragraph(
        "Now switch the box on. On Windows type the line below. On macOS or Linux type "
        "source venv/bin/activate instead. Type only one of them, never both."
    )
    command(doc, "venv\\Scripts\\activate", "The Windows line. Ignore the (venv) text in the explanation; you type only this line.")
    see(doc, "The start of the terminal line now shows (venv).")
    doc.add_paragraph("With (venv) showing, install the backend libraries. This downloads them from the internet.")
    command(
        doc,
        "pip install Django==5.2.6 djangorestframework==3.16.1 djangorestframework-simplejwt==5.5.1 "
        "django-cors-headers==4.9.0 python-dotenv==1.1.1 \"psycopg[binary]==3.2.10\"",
        "One long line. Copy it whole.",
    )
    see(doc, "The last line starts with Successfully installed.")
    done(doc, "The terminal shows (venv) and the libraries are installed.")
    problems(
        doc,
        "If it says pip is not recognized, the box is off. Run the activate line again. If it says "
        "No module named django later, run activate again in that terminal.",
    )
    new_words(
        doc,
        [
            ("Virtual environment", "A private box of libraries for one project. Ours is called venv."),
            ("pip", "The tool that downloads Python libraries."),
            ("Library", "Ready made code written by other people."),
        ],
    )

    doc.add_heading("Lesson 9. Create four simple backend files", level=1)
    one_line(doc, "Make the small files that sit directly inside the backend folder.")
    needs(doc, "About fifteen minutes.")
    doc.add_paragraph(
        "For every file in this book: right click the folder named in Where it goes, click New File, "
        "type the name exactly, press Enter, paste the code, then press Ctrl+S."
    )
    code_file(doc, "backend/requirements.txt", "inside the backend folder",
              "A shopping list of the libraries, so another computer can install the same ones.")
    code_file(doc, "backend/.env.example", "inside the backend folder",
              "A template for settings and secrets. You copy it to .env in a moment.")
    code_file(doc, "backend/.gitignore", "inside the backend folder",
              "Tells Git to ignore private files. Nothing to run.")
    code_file(doc, "backend/manage.py", "inside the backend folder",
              "The command file. Every backend command starts with python manage.py.")
    doc.add_paragraph("Now make your own copy of the settings file.")
    command(
        doc,
        "copy .env.example .env",
        "Type this in the terminal. On macOS or Linux the same command is: cp .env.example .env",
    )
    see(doc, "The sidebar shows a new file named .env next to .env.example.")
    done(doc, "Four files plus the .env copy exist inside backend.")
    problems(doc, "If a file looks empty, you forgot to paste. Open it again and paste.")
    new_words(
        doc,
        [
            (".env", "A private file with settings and secrets. Never share it."),
            ("manage.py", "The file you run to give the backend instructions."),
        ],
    )

    doc.add_heading("Lesson 10. Create the settings folder", level=1)
    one_line(doc, "Create the config folder that holds the instructions for the whole backend.")
    needs(doc, "About twenty minutes.")
    steps(
        doc,
        [
            "Right click backend in the sidebar, click New Folder, and name it config.",
            "Create the five files below inside the config folder.",
            "After the last file, run the check command at the end of this lesson.",
        ],
    )
    code_file(doc, "backend/config/__init__.py", "inside the config folder",
              "An empty file that tells Python this folder contains code.")
    code_file(doc, "backend/config/settings.py", "inside the config folder",
              "The most important file. It lists what is switched on, where the database lives and "
              "how long a login lasts. This is the best file in the project to read slowly.")
    code_file(doc, "backend/config/urls.py", "inside the config folder",
              "The address book. It sends each web address to the right app.")
    code_file(doc, "backend/config/wsgi.py", "inside the config folder",
              "Used by hosting companies when the site goes online. Nothing to change.")
    code_file(doc, "backend/config/asgi.py", "inside the config folder",
              "A second start up file for newer servers. Nothing to change.")
    command(doc, "python manage.py check", "Ask Django to test your settings.")
    see(doc, "The words System check identified no issues, with a number in brackets.")
    done(doc, "The check passes, which means your settings are correct.")
    problems(
        doc,
        "If it says manage.py not found, your terminal is not in the backend folder. Type cd backend "
        "and try again.",
    )
    new_words(
        doc,
        [
            ("Settings", "The file that controls how the whole backend behaves."),
            ("URL", "A web address, such as /api/dashboard/."),
        ],
    )

    doc.add_heading("Lesson 11. Create the users app for logging in", level=1)
    one_line(doc, "Create the files that handle accounts, logins and customer details.")
    needs(doc, "About forty minutes, because there are twelve files.")
    doc.add_paragraph(
        "In most systems a user logs in with a username. BankFlow is more like a real bank, so "
        "people log in with their email address. Every user also has a role: customer, or bank "
        "employee. That role decides which pages they can open."
    )
    steps(
        doc,
        [
            "Right click backend and create a folder named users.",
            "Right click the new users folder and create a folder named urls.",
            "Create the twelve files below, pasting each one and pressing Ctrl+S.",
        ],
    )
    code_file(doc, "backend/users/__init__.py", "inside users", "Marks the folder as code.")
    code_file(doc, "backend/users/apps.py", "inside users", "Tells Django about this app and switches on the profile rule.")
    code_file(doc, "backend/users/models.py", "inside users",
              "The user table, the role choices, and the customer profile table.")
    code_file(doc, "backend/users/signals.py", "inside users",
              "Creates an empty profile automatically whenever a user is created.")
    code_file(doc, "backend/users/permissions.py", "inside users",
              "The rule that only bank employees may open employee pages.")
    code_file(doc, "backend/users/serializers.py", "inside users",
              "Checks the register form and shapes user data as text for the website.")
    code_file(doc, "backend/users/views.py", "inside users", "Answers the register and profile requests.")
    code_file(doc, "backend/users/urls/__init__.py", "inside users/urls", "Marks the folder as code.")
    code_file(doc, "backend/users/urls/auth_urls.py", "inside users/urls",
              "The register, login and refresh addresses.")
    code_file(doc, "backend/users/urls/profile_urls.py", "inside users/urls", "The profile address.")
    code_file(doc, "backend/users/admin.py", "inside users",
              "Lets you see and edit users in the built in admin page.")
    code_file(doc, "backend/users/tests.py", "inside users",
              "Automatic checks for logging in and updating a profile.")
    done(doc, "The users folder holds twelve files, including the small urls folder.")
    problems(doc, "Check the spelling and the capital letters of every file name.")
    new_words(
        doc,
        [
            ("Role", "Whether somebody is a customer or a bank employee."),
            ("Serializer", "The file that turns a database row into text for the website."),
            ("Test", "A small program that checks your work for you."),
        ],
    )

    doc.add_heading("Lesson 12. Create the banking tables and the maths file", level=1)
    one_line(doc, "Create the four money tables and the file that does all the calculations.")
    needs(doc, "About forty minutes. The maths file is long, so copy it in one piece.")
    doc.add_paragraph(
        "A model is a description of a table. Four tables cover this project: accounts, "
        "transactions, loans and notifications. You do not write database code; Django reads these "
        "descriptions and creates the tables for you."
    )
    doc.add_paragraph(
        "The file called services.py is where all the money maths lives. It knows how to work out "
        "an EMI, how much you spent this month, which category is biggest, and what the last six "
        "months look like. The dashboard, the charts and the AI assistant all call this one file, "
        "which is why every screen shows the same numbers."
    )
    steps(
        doc,
        [
            "Right click backend and create a folder named banking.",
            "Inside banking, create a folder named urls.",
            "Create the six files below, then continue to the next lesson for the rest of this app.",
        ],
    )
    code_file(doc, "backend/banking/__init__.py", "inside banking", "Marks the folder as code.")
    code_file(doc, "backend/banking/apps.py", "inside banking", "Tells Django about this app.")
    code_file(doc, "backend/banking/models.py", "inside banking",
              "The four tables: account, transaction, loan and notification.")
    code_file(doc, "backend/banking/services.py", "inside banking",
              "All the money maths and the list of pretend transactions. The most interesting file "
              "in the backend.")
    code_file(doc, "backend/banking/serializers.py", "inside banking",
              "Turns banking rows into text the website can display.")
    code_file(doc, "backend/banking/urls/__init__.py", "inside banking/urls", "Marks the folder as code.")
    done(doc, "The banking folder holds these six files, and the maths file is saved without errors.")
    problems(doc, "If the file looks shorter than the book, you missed a section. Paste it again.")
    new_words(
        doc,
        [
            ("Transaction", "One movement of money, either in or out."),
            ("EMI", "The fixed amount you pay every month for a loan."),
        ],
    )

    doc.add_heading("Lesson 13. Create the banking web addresses", level=1)
    one_line(doc, "Create the files that answer the website's questions.")
    needs(doc, "About forty minutes.")
    doc.add_paragraph(
        "A view is the code that answers one web address. Some views are for customers and only "
        "show your own data. Others are for bank employees and show everybody's data. The two url "
        "files decide which address reaches which view."
    )
    base.add_table(
        doc,
        ["Address the website asks for", "Which file answers", "What comes back"],
        [
            ["/api/dashboard/", "banking/views.py", "Balance, income, spending and chart numbers"],
            ["/api/transactions/", "banking/views.py", "A page of transactions after filtering"],
            ["/api/loans/", "banking/views.py", "Your loans, or a new application"],
            ["/api/emi/", "banking/views.py", "The EMI for the numbers you typed"],
            ["/api/admin/analytics/", "banking/admin_views.py", "Totals for the whole pretend bank"],
            ["/api/admin/loans/<id>/", "banking/admin_views.py", "The loan after approving or rejecting"],
        ],
        [5.2, 5.0, 7.0],
    )
    code_file(doc, "backend/banking/views.py", "inside banking",
              "Customer addresses such as dashboard, transactions and loans.")
    code_file(doc, "backend/banking/admin_views.py", "inside banking",
              "Bank employee addresses that can see every customer.")
    code_file(doc, "backend/banking/urls/customer_urls.py", "inside banking/urls",
              "The list of customer addresses.")
    code_file(doc, "backend/banking/urls/admin_urls.py", "inside banking/urls",
              "The list of employee addresses.")
    code_file(doc, "backend/banking/admin.py", "inside banking",
              "Shows the four tables in the built in admin page.")
    code_file(doc, "backend/banking/tests.py", "inside banking",
              "Automatic checks for the banking addresses.")
    done(doc, "You can point at any address in the table above and say which file answers it.")
    problems(doc, "Make sure the two url files are inside the urls folder, not loose in banking.")
    new_words(
        doc,
        [
            ("Endpoint", "One web address your backend answers, such as /api/dashboard/."),
            ("JSON", "The simple text format both sides use to exchange data."),
        ],
    )

    doc.add_heading("Lesson 14. Create the pretend data command", level=1)
    one_line(doc, "Create the command that fills the record room with three pretend customers.")
    needs(doc, "About thirty minutes.")
    doc.add_paragraph(
        "Typing test data by hand would take hours. Instead you write a command once and run it "
        "whenever you want. It creates the three customers, their accounts, twenty-eight "
        "transactions across three months, six loans, some notifications and one saved chat."
    )
    doc.add_paragraph(
        "The numbers are chosen to match the demo you will show: balance 85,450 rupees, monthly "
        "income 45,000, monthly spending 18,450, and the biggest category Shopping at 7,200."
    )
    steps(
        doc,
        [
            "Right click banking and create a folder named management.",
            "Inside management, create a folder named commands.",
            "Create the three files below. The two __init__.py files are empty, but they must exist.",
        ],
    )
    code_file(doc, "backend/banking/management/__init__.py", "inside banking/management", "Marks the folder as code.")
    code_file(doc, "backend/banking/management/commands/__init__.py", "inside banking/management/commands", "Marks the folder as code.")
    code_file(doc, "backend/banking/management/commands/seed_demo.py", "inside banking/management/commands",
              "The command that creates all the pretend data. You run it in Lesson 16.")
    done(doc, "The path banking/management/commands/seed_demo.py exists exactly as written.")
    problems(
        doc,
        "Django only finds commands in that exact folder. If the name is different, the command "
        "will not appear later.",
    )
    new_words(
        doc,
        [
            ("Command", "A task you run by typing, such as seed_demo."),
            ("Seed data", "Pretend rows created so the app has something to show."),
        ],
    )

    doc.add_heading("Lesson 15. Create the AI assistant app", level=1)
    one_line(doc, "Create the chat feature that answers banking questions in sentences.")
    needs(doc, "About forty minutes.")
    doc.add_paragraph(
        "The assistant works in three moves. First it works out what you asked. Then it looks up "
        "your own pretend data. Then it writes a sentence from that data."
    )
    doc.add_paragraph(
        "The important idea is that the numbers always come from the database. The assistant is "
        "never allowed to invent a balance. If you later add a paid AI key, the robot only rephrases "
        "the same numbers. If you do not add one, the built in answers handle everything."
    )
    steps(
        doc,
        [
            "Right click backend and create a folder named assistant.",
            "Create the nine files below, pasting each one.",
        ],
    )
    code_file(doc, "backend/assistant/__init__.py", "inside assistant", "Marks the folder as code.")
    code_file(doc, "backend/assistant/apps.py", "inside assistant", "Tells Django about this app.")
    code_file(doc, "backend/assistant/models.py", "inside assistant",
              "The chat table that stores every question and answer.")
    code_file(doc, "backend/assistant/ai_service.py", "inside assistant",
              "The heart of the feature: it recognises the question, reads your data and writes the "
              "answer. Read this file after the project works.")
    code_file(doc, "backend/assistant/serializers.py", "inside assistant",
              "Checks that the question is sensible and formats saved chats.")
    code_file(doc, "backend/assistant/views.py", "inside assistant",
              "The chat, history and monitoring addresses.")
    code_file(doc, "backend/assistant/urls.py", "inside assistant", "The assistant address list.")
    code_file(doc, "backend/assistant/admin.py", "inside assistant",
              "Shows saved chats in the built in admin page.")
    code_file(doc, "backend/assistant/tests.py", "inside assistant",
              "Automatic checks for every kind of question.")
    done(doc, "All three apps exist: users, banking and assistant. The backend is complete.")
    problems(doc, "If Django complains about a missing file later, it names the app in the message.")
    new_words(
        doc,
        [
            ("Intent", "What the assistant thinks you are asking about."),
            ("Fallback", "The built in answers used when no paid AI service is connected."),
        ],
    )

    doc.add_heading("Lesson 16. Build the database and fill it with pretend data", level=1)
    one_line(doc, "Turn your file descriptions into real tables, then fill them.")
    needs(doc, "About ten minutes.")
    doc.add_paragraph(
        "Three commands finish the backend. The first prepares the table instructions. The second "
        "creates the tables. The third fills them with the three pretend customers."
    )
    command(
        doc,
        "python manage.py makemigrations users banking assistant\n"
        "python manage.py migrate\n"
        "python manage.py seed_demo --flush",
        "Run these three lines one at a time, waiting for each to finish.",
    )
    doc.add_paragraph("The last command prints the logins you will use for the rest of the book.")
    base.add_code(
        doc,
        "Seeded customer Mohammed Adnan\n"
        "Seeded customer Aisha Khan\n"
        "Seeded customer Rahul Verma\n"
        "\n"
        "Demo data ready.\n"
        "Admin    : admin@bankflow.com / Admin@12345\n"
        "Customer : mohammed@bankflow.com / Demo@12345\n"
        "Customer : aisha@bankflow.com / Demo@12345\n"
        "Customer : rahul@bankflow.com / Demo@12345",
    )
    see(doc, "Those three logins, and a new file named db.sqlite3 inside backend.")
    done(doc, "The pretend bank exists. db.sqlite3 is your record room.")
    problems(
        doc,
        "If it says No such table, you skipped the migrate command. Run it again, then run seed_demo.",
    )
    new_words(
        doc,
        [
            ("Migration", "An instruction that creates or changes database tables."),
            ("db.sqlite3", "The database file. It is your pretend bank's record room."),
        ],
    )

    doc.add_heading("Lesson 17. Run the tests and start the backend", level=1)
    one_line(doc, "Check the backend with twenty-five automatic tests, then switch it on.")
    needs(doc, "About ten minutes.")
    doc.add_paragraph(
        "Tests are small programs that check your work. BankFlow has twenty-five of them. They "
        "create their own temporary data, try every important address, and compare the answers with "
        "what should happen. This is the fastest way to know your backend is healthy."
    )
    command(doc, "python manage.py test")
    doc.add_paragraph("A healthy run ends like this.")
    base.add_code(
        doc,
        "Found 25 test(s).\n"
        "System check identified no issues (0 silenced).\n"
        ".........................\n"
        "----------------------------------------------------------------------\n"
        "Ran 25 tests in 31.331s\n"
        "\n"
        "OK",
    )
    see(doc, "The word OK at the end.")
    done(doc, "All twenty-five tests pass. Your backend is correct.")
    problems(
        doc,
        "The message names the file with the problem. Open that file, compare it with the code in "
        "this book, save it, and run the tests again.",
    )
    doc.add_paragraph("Now start the backend and leave it running.")
    command(doc, "python manage.py runserver 127.0.0.1:8000")
    doc.add_paragraph(
        "The terminal stops returning to the prompt and shows a line about watching for file "
        "changes. That means the server is on. Leave this terminal running and do not close it."
    )
    steps(
        doc,
        [
            "Open your browser and go to http://127.0.0.1:8000/admin/",
            "Log in with admin@bankflow.com and the password Admin@12345.",
            "Click Users on the left. You will see the three pretend customers.",
        ],
    )
    see(doc, "A page listing Mohammed Adnan, Aisha Khan and Rahul Verma.")
    done(doc, "Your backend is running and holds real data. Part 2 is finished.")
    problems(
        doc,
        "If the browser cannot open the page, the server is not running. Run the start command "
        "again. To stop the server later, click in the terminal and press Ctrl+C.",
    )
    new_words(
        doc,
        [
            ("Port", "The numbered channel a program listens on, here 8000."),
            ("localhost or 127.0.0.1", "Your own computer."),
        ],
    )

    # ============================================================ part 3
    base.page_break(doc)
    doc.add_heading("Part 3. Build the website", level=1)
    doc.add_paragraph(
        "The website is the lobby. It runs inside the browser and asks the backend for data when it "
        "needs it. You already have the staff working; now you build the room customers walk into."
    )
    doc.add_paragraph(
        "Open a second terminal for this part: in VS Code click the plus sign at the top right of "
        "the terminal panel. Keep the backend running in the first tab."
    )

    doc.add_heading("Lesson 18. What a website is and how to create the project", level=1)
    one_line(doc, "Understand the frontend, then create the project and download its libraries.")
    needs(doc, "About twenty minutes.")
    doc.add_paragraph(
        "A website is made of pages. Each page is built from pieces called components, such as a "
        "button, a card or a table. When you click something, the page asks the backend for data "
        "and then redraws itself. That is all that is happening on every screen you will build."
    )
    doc.add_paragraph(
        "React is the tool that builds these pages. Vite is the tool that runs the website while you "
        "work and packs it up at the end. You will create the project with two commands."
    )
    steps(
        doc,
        [
            "In your second terminal, move into the frontend folder.",
            "Create the React project inside it.",
            "Install the starter libraries.",
            "Install the four extra libraries BankFlow uses.",
        ],
    )
    command(
        doc,
        "cd ..\ncd frontend\nnpm create vite@latest . -- --template react\nnpm install",
        "Wait for each command to finish before typing the next.",
    )
    doc.add_paragraph(
        "If the terminal asks whether to continue in the current folder, answer yes. If it asks for "
        "a package name, just press Enter."
    )
    command(
        doc,
        "npm install @mui/material @mui/icons-material @emotion/react @emotion/styled\n"
        "npm install axios react-router-dom recharts react-icons",
        "These add the buttons, cards, charts and the connection to your backend.",
    )
    see(doc, "Messages about added packages, with no red errors.")
    done(doc, "The frontend folder contains src, public and package.json.")
    problems(
        doc,
        "If npm is not recognized, install Node.js again from Lesson 3 and open a fresh terminal.",
    )
    new_words(
        doc,
        [
            ("React", "The tool that builds the pages you see in the browser."),
            ("Component", "A reusable piece of a page, such as a card."),
            ("npm", "The tool that downloads website libraries."),
        ],
    )

    doc.add_heading("Lesson 19. Create the website settings files", level=1)
    one_line(doc, "Replace the starter files with the BankFlow versions.")
    needs(doc, "About forty minutes.")
    doc.add_paragraph(
        "The starter project comes with a demonstration page. You replace those files with ours. "
        "When a file already exists, open it and replace everything inside it, then press Ctrl+S."
    )
    doc.add_paragraph(
        "Two of these files are worth knowing. theme.js holds every colour and font, so you can "
        "restyle the whole website from one file. App.jsx lists every page and the address that "
        "shows it."
    )
    code_file(doc, "frontend/package.json", "frontend folder, replacing the existing file",
              "The list of libraries and the commands you can run.")
    code_file(doc, "frontend/vite.config.js", "frontend folder, replacing the existing file",
              "Tells Vite which port to use and how to build the site.")
    code_file(doc, "frontend/index.html", "frontend folder, replacing the existing file",
              "The outer page that loads everything else.")
    code_file(doc, "frontend/.env.example", "frontend folder, a new file",
              "A template that says where your backend is.")
    code_file(doc, "frontend/.gitignore", "frontend folder, replacing the existing file",
              "Tells Git to ignore downloaded files.")
    code_file(doc, "frontend/public/bankflow.svg", "public folder, replacing the existing icon",
              "The small picture shown on the browser tab.")
    code_file(doc, "frontend/src/index.css", "src folder, replacing the existing file",
              "A few global styles.")
    code_file(doc, "frontend/src/theme.js", "src folder, a new file",
              "Every colour, font and rounded corner in the website.")
    code_file(doc, "frontend/src/main.jsx", "src folder, replacing the existing file",
              "Starts the website and switches on the theme and login state.")
    code_file(doc, "frontend/src/App.jsx", "src folder, replacing the existing file",
              "The list of pages and their addresses.")
    command(doc, "copy .env.example .env", "In the terminal, inside the frontend folder.")
    doc.add_paragraph(
        "The starter project also contains src/App.css and a folder called src/assets with a logo. "
        "Right click each of them in the sidebar and click Delete. BankFlow does not use them."
    )
    see(doc, "The src folder holds main.jsx, App.jsx, theme.js and index.css.")
    done(doc, "Every settings file is saved, and the starter leftovers are deleted.")
    problems(doc, "If a page shows an import error later, the file name is probably misspelled.")
    new_words(
        doc,
        [
            ("Theme", "The file that decides colours, fonts and spacing."),
            ("Route", "A web address inside the website, such as /dashboard."),
        ],
    )

    doc.add_heading("Lesson 20. Create the files that talk to the backend", level=1)
    one_line(doc, "Create one connection file, five call files, the login memory and two helpers.")
    needs(doc, "About forty minutes.")
    doc.add_paragraph(
        "When the website needs data, it calls one file called api.js. That file adds your login "
        "pass to the request, renews the pass automatically when it expires, and turns any error "
        "into a sentence the page can show. Because every request goes through it, you only write "
        "this logic once."
    )
    doc.add_paragraph(
        "Beside it, AuthContext.jsx remembers who is logged in, so any page can ask who you are and "
        "whether you are a bank employee."
    )
    steps(
        doc,
        [
            "Inside frontend/src, create three folders: services, context and utils.",
            "Create the eight files below in their folders.",
        ],
    )
    code_file(doc, "frontend/src/services/api.js", "src/services",
              "The single connection to the backend, with the login pass attached to every request.")
    code_file(doc, "frontend/src/services/authService.js", "src/services",
              "Register, log in and read your profile.")
    code_file(doc, "frontend/src/services/bankingService.js", "src/services",
              "Dashboard, transactions, loans, EMI and notifications.")
    code_file(doc, "frontend/src/services/aiService.js", "src/services",
              "Chat with the assistant and read saved history.")
    code_file(doc, "frontend/src/services/adminService.js", "src/services",
              "The bank employee calls.")
    code_file(doc, "frontend/src/context/AuthContext.jsx", "src/context",
              "Remembers who is logged in while the website is open.")
    code_file(doc, "frontend/src/utils/formatCurrency.js", "src/utils",
              "Writes rupees and dates the same way everywhere.")
    code_file(doc, "frontend/src/utils/calculations.js", "src/utils",
              "Works out an EMI instantly as you move a slider.")
    done(doc, "The three folders exist with their eight files saved.")
    problems(doc, "Folder names must be lowercase: services, context, utils.")
    new_words(
        doc,
        [
            ("Axios", "The small library that sends requests to your backend."),
            ("Token", "The signed pass that proves you are logged in."),
            ("State", "Data a page keeps in memory while it is open."),
        ],
    )

    doc.add_heading("Lesson 21. Create the shared pieces of every page", level=1)
    one_line(doc, "Create the nine components that appear on many pages.")
    needs(doc, "About forty minutes.")
    doc.add_paragraph(
        "A component is a piece of a page you write once and reuse. The sidebar, the top bar, the "
        "statistic cards, the transaction table and the chat bubble are all components. That is why "
        "every page has the same look, and why changing one file updates the whole website."
    )
    steps(
        doc,
        [
            "Inside frontend/src, create a folder named components.",
            "Create the nine files below inside it.",
        ],
    )
    code_file(doc, "frontend/src/components/AppLayout.jsx", "src/components",
              "The frame around every private page: sidebar, top bar and content.")
    code_file(doc, "frontend/src/components/Navbar.jsx", "src/components",
              "The top bar with the page title, notifications and your name.")
    code_file(doc, "frontend/src/components/Sidebar.jsx", "src/components",
              "The list of pages on the left. It folds away on small screens.")
    code_file(doc, "frontend/src/components/DashboardCard.jsx", "src/components",
              "One statistic card, used four times on the dashboard.")
    code_file(doc, "frontend/src/components/TransactionTable.jsx", "src/components",
              "The transaction table, used by both customer and employee pages.")
    code_file(doc, "frontend/src/components/LoanCard.jsx", "src/components",
              "One loan summary with a repayment bar.")
    code_file(doc, "frontend/src/components/ChatMessage.jsx", "src/components",
              "One chat bubble, used for your question and the assistant's answer.")
    code_file(doc, "frontend/src/components/ProtectedRoute.jsx", "src/components",
              "Sends you to the login page when a page needs a login.")
    code_file(doc, "frontend/src/components/Common.jsx", "src/components",
              "Small helpers used everywhere: loading spinner, error message, empty state, status label.")
    done(doc, "The components folder holds nine files.")
    problems(doc, "Capital letters matter. AppLayout.jsx is not the same as applayout.jsx.")
    new_words(
        doc,
        [
            ("Prop", "A value you pass into a component so it can display something."),
            ("Layout", "The outer frame that stays the same while pages change inside it."),
        ],
    )

    doc.add_heading("Lesson 22. Create the customer pages", level=1)
    one_line(doc, "Create the fourteen pages a customer can visit.")
    needs(doc, "About two hours. This is the biggest lesson, so take it slowly.")
    doc.add_paragraph(
        "Each page follows the same pattern: it asks the backend for data, keeps the answer in "
        "memory, and draws it on screen. The table shows which address each page calls."
    )
    base.add_table(
        doc,
        ["Page file", "What the customer sees", "It calls this address"],
        [
            ["Landing.jsx", "The public introduction with the big headline", "nothing"],
            ["Login.jsx", "The login form with the demo accounts", "/api/auth/login/"],
            ["Register.jsx", "The sign up form", "/api/auth/register/"],
            ["Dashboard.jsx", "Balance, income, spending, loans and four charts", "/api/dashboard/"],
            ["Account.jsx", "Your account details, with the middle hidden", "/api/account/"],
            ["Transactions.jsx", "The list with search and filters", "/api/transactions/"],
            ["TransactionDetails.jsx", "One transaction in full", "/api/transactions/<id>/"],
            ["Loans.jsx", "Loans and the application form", "/api/loans/"],
            ["LoanDetails.jsx", "One loan and its repayment plan", "/api/loans/<id>/"],
            ["EMICalculator.jsx", "The EMI calculator with sliders", "/api/emi/"],
            ["AIAssistant.jsx", "The chat screen", "/api/assistant/chat/"],
            ["Notifications.jsx", "Your alerts", "/api/notifications/"],
            ["Profile.jsx", "Your details, which you can edit", "/api/profile/"],
            ["NotFound.jsx", "A friendly message for unknown addresses", "nothing"],
        ],
        [3.8, 7.4, 6.0],
    )
    steps(
        doc,
        [
            "Inside frontend/src, create a folder named pages.",
            "Create the fourteen files below inside it.",
        ],
    )
    code_file(doc, "frontend/src/pages/Landing.jsx", "src/pages", "The first page a visitor sees.")
    code_file(doc, "frontend/src/pages/Login.jsx", "src/pages", "Logging in and remembering the pass.")
    code_file(doc, "frontend/src/pages/Register.jsx", "src/pages", "Creating a new pretend customer.")
    code_file(doc, "frontend/src/pages/Dashboard.jsx", "src/pages", "The main screen after logging in.")
    code_file(doc, "frontend/src/pages/Account.jsx", "src/pages", "Account details.")
    code_file(doc, "frontend/src/pages/Transactions.jsx", "src/pages", "The transaction list with filters.")
    code_file(doc, "frontend/src/pages/TransactionDetails.jsx", "src/pages", "A single transaction.")
    code_file(doc, "frontend/src/pages/Loans.jsx", "src/pages", "Loans and the application form.")
    code_file(doc, "frontend/src/pages/LoanDetails.jsx", "src/pages", "A single loan and its schedule.")
    code_file(doc, "frontend/src/pages/EMICalculator.jsx", "src/pages", "The EMI calculator.")
    code_file(doc, "frontend/src/pages/AIAssistant.jsx", "src/pages", "The chat assistant.")
    code_file(doc, "frontend/src/pages/Notifications.jsx", "src/pages", "The alerts page.")
    code_file(doc, "frontend/src/pages/Profile.jsx", "src/pages", "The profile page.")
    code_file(doc, "frontend/src/pages/NotFound.jsx", "src/pages", "The page for addresses that do not exist.")
    done(doc, "The pages folder holds fourteen files.")
    problems(doc, "Landing, Dashboard and AIAssistant are long. Copy them in one piece and save.")
    new_words(
        doc,
        [
            ("Page", "A screen the user can open, such as the dashboard."),
            ("Chart", "A picture of numbers, drawn by the Recharts library."),
        ],
    )

    doc.add_heading("Lesson 23. Create the bank employee pages", level=1)
    one_line(doc, "Create the six pages only a bank employee can open.")
    needs(doc, "About forty five minutes.")
    doc.add_paragraph(
        "These pages read the employee addresses, which return data for every customer. The route "
        "guard sends ordinary customers back to their own dashboard, and the backend refuses the "
        "request too, so the door is locked in two places."
    )
    steps(
        doc,
        [
            "Inside frontend/src/pages, create a folder named admin.",
            "Create the six files below inside it.",
        ],
    )
    code_file(doc, "frontend/src/pages/admin/AdminDashboard.jsx", "src/pages/admin",
              "Six totals, portfolio charts and the top customers table.")
    code_file(doc, "frontend/src/pages/admin/CustomerManagement.jsx", "src/pages/admin",
              "The customer table and the detail window.")
    code_file(doc, "frontend/src/pages/admin/TransactionManagement.jsx", "src/pages/admin",
              "Every customer's transactions with filters.")
    code_file(doc, "frontend/src/pages/admin/LoanManagement.jsx", "src/pages/admin",
              "Approve, activate or reject a loan application.")
    code_file(doc, "frontend/src/pages/admin/AdminAnalytics.jsx", "src/pages/admin",
              "The charts that summarise the whole pretend bank.")
    code_file(doc, "frontend/src/pages/admin/AIMonitor.jsx", "src/pages/admin",
              "What customers asked the assistant and how it answered.")
    done(doc, "All twenty pages exist: fourteen in pages, six in pages/admin.")
    problems(doc, "The admin folder must be inside the pages folder, not beside it.")
    new_words(
        doc,
        [
            ("Access", "Who is allowed to open a page."),
            ("Monitoring", "A page that lets staff watch how a feature is being used."),
        ],
    )

    doc.add_heading("Lesson 24. Start the website and log in", level=1)
    one_line(doc, "Run the website and click through it for the first time.")
    needs(doc, "Both the backend and the frontend. About ten minutes.")
    doc.add_paragraph(
        "Your backend should still be running in the first terminal tab. In the second tab, make "
        "sure you are inside the frontend folder, then start the website."
    )
    command(doc, "npm run dev")
    doc.add_paragraph(
        "The terminal prints a Local address, usually http://localhost:5173. Open that address in "
        "your browser. Keep both terminals running."
    )
    steps(
        doc,
        [
            "The landing page appears with the headline Your Smarter Digital Banking Experience.",
            "Click Login.",
            "Click the line with mohammed@bankflow.com to fill the form, then click Login.",
            "The dashboard appears with a balance of 85,450 rupees.",
            "Click AI Assistant in the left list and ask: What is my balance?",
            "The assistant answers with the same 85,450 rupees, because it reads the same database.",
        ],
    )
    see(doc, "Four statistic cards, four charts, and an assistant that answers your question.")
    done(doc, "The website and the backend are talking to each other. You built both of them.")
    problems(
        doc,
        "If the page loads but every message says the API cannot be reached, the backend terminal "
        "has stopped. Go to that tab and run the start command again.",
    )
    new_words(
        doc,
        [
            ("local address", "The address of the website running on your own computer."),
            ("Refresh", "Pressing F5 to load the page again."),
        ],
    )

    # ============================================================ part 4
    base.page_break(doc)
    doc.add_heading("Part 4. Practise and understand", level=1)
    doc.add_paragraph(
        "The hard work is done. This part turns the finished project into your own learning ground. "
        "You will walk every screen, change things on purpose, and trace how a click becomes data."
    )

    doc.add_heading("Lesson 25. A tour of every screen", level=1)
    one_line(doc, "See every feature in the order you would show it to somebody.")
    needs(doc, "Twenty minutes of clicking.")
    base.add_table(
        doc,
        ["Screen", "What to do", "What it teaches"],
        [
            ["Landing page", "Scroll down slowly", "How a public page is built from sections"],
            ["Login", "Click the demo line, then log in", "How a login is checked and remembered"],
            ["Dashboard", "Read the four cards, then switch chart tabs", "Turning one answer into cards and charts"],
            ["Account", "Look at the hidden middle of the number", "Never showing a full account number"],
            ["Transactions", "Search Swiggy, then filter Shopping", "Filtering and paging on the backend"],
            ["Transaction details", "Open any row", "How one record is loaded by its number"],
            ["Loans", "Open the form and watch the EMI change", "Instant maths and saving a new record"],
            ["Loan details", "Read the instalment table", "Turning a loan into a monthly plan"],
            ["EMI calculator", "Move the sliders", "Browser maths checked by the backend"],
            ["AI assistant", "Ask three questions, open history", "How questions are understood and saved"],
            ["Notifications", "Mark one read, then mark all read", "Changing one row from the screen"],
            ["Profile", "Change your phone and save", "Editing your own data safely"],
            ["Admin dashboard", "Log in as admin@bankflow.com", "Different pages for different roles"],
            ["Loan management", "Approve the pending loan", "An action that changes data and notifies somebody"],
            ["AI monitoring", "Read the questions from your own chat", "How staff can watch a feature"],
        ],
        [3.6, 7.2, 6.4],
    )
    done(doc, "You have visited every screen once.")

    doc.add_heading("Lesson 26. Four easy changes you can make", level=1)
    one_line(doc, "Change one small thing at a time and watch the result.")
    needs(doc, "Thirty minutes. Change only one thing before looking at the result.")
    doc.add_paragraph(
        "Change 1. The colour of the whole website. Open frontend/src/theme.js and find the line "
        "that sets the main colour. Change the colour code and save."
    )
    base.add_code(doc, "main: \"#1b3a8f\",        // change this to main: \"#0f766e\", and save")
    see(doc, "Every button and highlight turns teal within a second, without restarting anything.")
    doc.add_paragraph(
        "Change 2. The demo balance. Open backend/banking/management/commands/seed_demo.py and "
        "find this line."
    )
    base.add_code(doc, "target_balance = 85450.0      # change this number and save")
    doc.add_paragraph("Then run the seed command again in the backend terminal and refresh the dashboard.")
    base.add_code(doc, "python manage.py seed_demo --flush")
    see(doc, "The dashboard balance becomes 100,000 rupees, and the assistant gives the same new number.")
    doc.add_paragraph(
        "Change 3. Teach the assistant a new phrase. Open backend/assistant/ai_service.py, find "
        "account_balance in the INTENT_KEYWORDS list, and add a phrase of your own to that list."
    )
    see(doc, "After saving, you can ask the assistant using your new phrase and it answers with your balance.")
    doc.add_paragraph(
        "Change 4. The dashboard greeting. Open frontend/src/pages/Dashboard.jsx, find the PageHeader "
        "title near the top, and change the wording."
    )
    base.add_code(doc, "title={`${greeting()}, ${firstName}`}      // change the words inside the braces")
    see(doc, "The dashboard heading shows your own wording after you save.")
    done(doc, "You have edited the theme, the data, the assistant and a page. Those are the four places "
              "most changes happen in a project like this.")
    problems(doc, "If something breaks, press Ctrl+Z in that file to undo, then save again.")

    doc.add_heading("Lesson 27. How a click becomes data", level=1)
    one_line(doc, "Follow one click from the button to the record and back.")
    needs(doc, "Ten minutes of reading.")
    doc.add_paragraph(
        "This is the most useful thing in the whole book. Read the ten steps below slowly. Once you "
        "can follow this path, you can build any feature."
    )
    base.add_code(
        doc,
        "1  You click View Transactions in the browser\n"
        "2  The website shows the Transactions page for the address /transactions\n"
        "3  That page asks the bank service for a list of transactions\n"
        "4  The connection file adds your login pass and sends the request\n"
        "5  Django matches the address /api/transactions/ to a view\n"
        "6  The view reads your filters and asks the database for matching rows\n"
        "7  The database returns the rows of your pretend account\n"
        "8  The serializer turns each row into simple text\n"
        "9  The text travels back and the page stores it in memory\n"
        "10 The table on your screen redraws with those rows",
    )
    doc.add_paragraph("Four sentences to remember:")
    steps(
        doc,
        [
            "The lobby is the website: pages, buttons and charts in your browser.",
            "The counter is the API: fixed addresses that accept questions and return answers.",
            "The staff are the backend: they check who you are and decide what to send.",
            "The record room is the database: it stores every customer, transaction and loan.",
        ],
    )
    done(doc, "You can explain this path to somebody else without reading it again.")

    doc.add_heading("Lesson 28. When something goes wrong", level=1)
    one_line(doc, "Fix the twenty messages beginners see most often.")
    needs(doc, "Keep this lesson open while you work.")
    base.add_table(
        doc,
        ["What you see", "What it means", "What to do"],
        [
            ["python is not recognized", "Python is not on the PATH", "Reinstall Python and tick Add python.exe to PATH"],
            ["pip is not recognized", "Your private box is switched off", "Run venv\\Scripts\\activate, then try again"],
            ["npm is not recognized", "Node.js is missing, or the terminal is old", "Reinstall Node.js LTS, then open a new terminal"],
            ["running scripts is disabled", "Windows blocks the activate line", "Run Set-ExecutionPolicy RemoteSigned -Scope CurrentUser, answer Yes, then activate again"],
            ["No module named django", "The box is off or libraries are missing", "Activate venv, then pip install -r requirements.txt"],
            ["manage.py not found", "The terminal is in the wrong folder", "Type cd backend and try again"],
            ["No such table", "The tables were never created", "Run python manage.py migrate, then seed_demo --flush"],
            ["Port 8000 is already in use", "The backend is already running", "Use the running one, or start it on 8001 and change the website setting"],
            ["EADDRINUSE port 5173", "The website is already running", "Use the window that is already open, or press Ctrl+C first"],
            ["Cannot find module", "A file name or folder is wrong", "Compare the capitals and the folder with this book"],
            ["The API cannot be reached", "The backend terminal stopped", "Start the backend again and refresh the page"],
            ["CORS policy error", "The backend does not allow your website address", "Check CORS_ALLOWED_ORIGINS in backend/.env includes http://localhost:5173"],
            ["401 Unauthorized", "Your login pass expired", "Log out and log in again"],
            ["Blank page with an error in the terminal", "The last file you edited has a mistake", "Open that file, compare it with this book, press Ctrl+Z to undo if unsure"],
            ["npm install stops with a blocked scripts warning", "The package manager blocked esbuild", "Run npm install-scripts approve esbuild, then npm install again"],
            ["The rupee sign looks strange", "Your code font is different", "Ignore it; the website itself is not affected"],
        ],
        [4.8, 5.2, 7.2],
    )
    doc.add_paragraph(
        "One habit solves most of these: read the first line of the message, look at the file name it "
        "mentions, and ask whether the terminal is in the right folder and whether the backend is "
        "still running."
    )
    done(doc, "You know where to look instead of starting over.")

    doc.add_heading("Lesson 29. Stop, start and start again", level=1)
    one_line(doc, "Keep the project easy to open on any day.")
    needs(doc, "Five minutes.")
    doc.add_paragraph(
        "To stop anything that is running, click inside that terminal and press the Ctrl and C keys "
        "together. Then start each side again with its own commands."
    )
    doc.add_paragraph().add_run("Start the backend in the first terminal:").bold = True
    command(
        doc,
        "cd banking_app/backend\n"
        "venv\\Scripts\\activate\n"
        "python manage.py runserver 127.0.0.1:8000",
    )
    doc.add_paragraph().add_run("Start the website in the second terminal:").bold = True
    command(doc, "cd banking_app/frontend\nnpm run dev")
    doc.add_paragraph().add_run("If the pretend data ever looks wrong, reset it:").bold = True
    command(
        doc,
        "cd banking_app/backend\n"
        "venv\\Scripts\\activate\n"
        "python manage.py seed_demo --flush",
    )
    see(doc, "The backend prints a line about watching for file changes, and the website prints a Local address.")
    done(doc, "You can start and stop the project without re-reading the book.")
    problems(doc, "Always activate the private box before backend commands. The terminal shows (venv) when it is on.")

    doc.add_heading("Lesson 30. What to learn next", level=1)
    one_line(doc, "Use your own project as the next textbook.")
    needs(doc, "No new tools. Just the project you built.")
    steps(
        doc,
        [
            "Change one screen at a time. Open the notifications page and add a filter for the type of message.",
            "Add one new field. Give the customer profile a nickname, then show it on the profile page.",
            "Add one new address. Build a monthly spending address and draw it as a new chart.",
            "Teach the assistant two more questions, reusing the maths that already exists in services.py.",
            "Learn Git so you can save versions of your work and try changes safely.",
            "Write a test for every new feature, copying the style of the tests you already have.",
            "Put the backend online with a hosting company and the website on a static host, then change the website setting to the new address.",
            "Read your own code. Every file in this book explains its decisions in comments.",
        ],
    )
    done(doc, "You have a working project, a habit of checking your work, and a list of next steps. "
              "That is what finishing your first full stack project looks like.")

    # ============================================================ appendices
    base.page_break(doc)
    doc.add_heading("Appendix A. Words explained simply", level=1)
    doc.add_paragraph("Keep this page near you. Every technical word in the book appears here in plain language.")
    base.add_table(
        doc,
        ["Word", "Plain meaning"],
        [
            ["Terminal", "The text panel where you type commands. It is at the bottom of VS Code."],
            ["Command", "One line you type and run by pressing Enter."],
            ["Folder and path", "A folder holds files. A path is the address of a file, such as backend/config/settings.py."],
            ["VS Code", "The free editor where you create files and run commands."],
            ["Extension", "An add on for VS Code that adds features."],
            ["Virtual environment", "A private box of Python libraries for one project. Ours is venv."],
            ["Library", "Ready made code written by other people."],
            ["pip", "The tool that downloads Python libraries."],
            ["npm", "The tool that downloads website libraries."],
            ["Node.js", "The program that runs the website building tools."],
            ["Django", "A ready made backend structure written in Python."],
            ["React", "The tool that builds the pages you see in the browser."],
            ["Vite", "The tool that runs the website while you work and packs it up at the end."],
            ["Component", "A reusable piece of a page, such as a card or a table."],
            ["Prop", "A value passed into a component so it can display something."],
            ["State", "Data a page keeps in memory while it is open."],
            ["Hook", "A React helper that lets a component remember things or run code at the right time."],
            ["API", "The counter: fixed web addresses your backend answers."],
            ["Endpoint", "One of those addresses, such as /api/dashboard/."],
            ["Request and response", "The question the website sends and the answer it gets back."],
            ["JSON", "A simple text format for data, understood by both sides."],
            ["Token", "A signed pass that proves you are logged in."],
            ["Model", "A description of one database table."],
            ["Migration", "An instruction that creates or changes database tables."],
            ["Serializer", "The code that turns a database row into text for the website."],
            ["View", "The code that answers one web address."],
            ["CORS", "The browser rule that decides which website may call your backend."],
            ["Seed data", "Pretend rows created by a command so the app has something to show."],
            ["Build", "Packing the website into final files for hosting."],
            ["localhost and port", "Your own computer, and the numbered channel such as 8000 or 5173."],
        ],
        [4.2, 13.0],
    )

    doc.add_heading("Appendix B. Every file and what it does", level=1)
    doc.add_paragraph(
        "Ninety-two files make up the project. The list below gives each one a purpose and its "
        "length. The files created by commands are explained after the table."
    )
    manifest = []
    for rel_path, purpose in base.MANIFEST:
        path = ROOT / rel_path
        lines = len(path.read_text(encoding="utf-8").splitlines()) if path.exists() else 0
        manifest.append([rel_path, purpose, str(lines)])
    base.add_table(
        doc,
        ["Path", "What it does", "Lines"],
        manifest,
        [6.4, 9.0, 1.8],
        font_size=Pt(8.5),
        header_size=Pt(8.5),
    )
    doc.add_paragraph(
        "Created by commands, so you never paste them: db.sqlite3 comes from migrate, the migrations "
        "folders come from makemigrations, node_modules and package-lock.json come from npm install, "
        "and dist comes from npm run build. The two .env files are copies of the .env.example files."
    )

    doc.add_heading("Appendix C. Logins and the demo script", level=1)
    base.add_table(
        doc,
        ["Who", "Email", "Password", "What it shows"],
        [
            ["Customer", "mohammed@bankflow.com", "Demo@12345", "Balance 85,450, income 45,000, spending 18,450, two loans"],
            ["Customer", "aisha@bankflow.com", "Demo@12345", "Another customer with different loans"],
            ["Customer", "rahul@bankflow.com", "Demo@12345", "A third customer with a pending loan"],
            ["Bank employee", "admin@bankflow.com", "Admin@12345", "The employee pages and monitoring"],
        ],
        [3.0, 5.2, 3.0, 6.0],
    )
    doc.add_paragraph("Show the project in this order when somebody asks to see it.")
    steps(
        doc,
        [
            "The landing page, scrolled slowly.",
            "Log in as the customer and show the dashboard.",
            "Open the account page and point out the hidden account number.",
            "Filter the transactions, then open one.",
            "Apply for a loan and show the EMI changing as you type.",
            "Move the sliders in the EMI calculator.",
            "Ask the assistant five questions, then open the history.",
            "Mark a notification as read.",
            "Log in as the bank employee, approve the pending loan, then open analytics and AI monitoring.",
        ],
    )

    doc.add_heading("Appendix D. All the commands in one place", level=1)
    doc.add_paragraph(
        "Every command in this book, in the order you use them. Type one group at a time and wait "
        "for it to finish before typing the next group."
    )
    doc.add_paragraph().add_run("Once only, prepare the backend:").bold = True
    command(
        doc,
        "cd banking_app/backend\n"
        "python -m venv venv\n"
        "venv\\Scripts\\activate\n"
        "pip install Django==5.2.6 djangorestframework==3.16.1 djangorestframework-simplejwt==5.5.1 "
        "django-cors-headers==4.9.0 python-dotenv==1.1.1 \"psycopg[binary]==3.2.10\"\n"
        "copy .env.example .env\n"
        "python manage.py check",
    )
    doc.add_paragraph().add_run("Once only, build the pretend bank:").bold = True
    command(
        doc,
        "python manage.py makemigrations users banking assistant\n"
        "python manage.py migrate\n"
        "python manage.py seed_demo --flush\n"
        "python manage.py test",
    )
    doc.add_paragraph().add_run("Once only, prepare the website:").bold = True
    command(
        doc,
        "cd ..\n"
        "cd frontend\n"
        "npm create vite@latest . -- --template react\n"
        "npm install\n"
        "npm install @mui/material @mui/icons-material @emotion/react @emotion/styled\n"
        "npm install axios react-router-dom recharts react-icons\n"
        "copy .env.example .env",
    )
    doc.add_paragraph().add_run("Every day, start the backend in the first terminal:").bold = True
    command(
        doc,
        "cd banking_app/backend\n"
        "venv\\Scripts\\activate\n"
        "python manage.py runserver 127.0.0.1:8000",
    )
    doc.add_paragraph().add_run("Every day, start the website in the second terminal:").bold = True
    command(doc, "cd banking_app/frontend\nnpm run dev")
    doc.add_paragraph().add_run("Useful extras:").bold = True
    command(
        doc,
        "python manage.py seed_demo --flush      (reset the pretend data)\n"
        "python manage.py test                   (check the backend)\n"
        "npm run build                           (pack the website for hosting)",
    )
    doc.add_paragraph(
        "Press the Ctrl and C keys together in a terminal to stop whatever is running in it. On "
        "macOS or Linux, use source venv/bin/activate instead of the activate line, and cp instead "
        "of copy."
    )

    doc.save(OUTPUT)
    print(f"wrote {OUTPUT}")


def main() -> None:
    page_map = {}
    if len(sys.argv) > 1:
        page_map = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8-sig"))
    build(page_map)


if __name__ == "__main__":
    main()
```

### tools/check_styles.py

```python
#!/usr/bin/env python3
"""Inspect the DOCX styles to confirm formatting rules (black headings, no title border)."""
from __future__ import annotations

import sys
import zipfile

from lxml import etree

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}


def main() -> None:
    path = sys.argv[1]
    with zipfile.ZipFile(path) as archive:
        root = etree.fromstring(archive.read("word/styles.xml"))

    for style_id in ("Title", "Heading1", "Heading2", "Heading3", "CodeBlock", "Normal"):
        found = root.xpath(f'//w:style[@w:styleId="{style_id}"]', namespaces=NS)
        if not found:
            print(f"{style_id}: not found")
            continue
        style = found[0]
        colors = style.xpath(".//w:rPr/w:color", namespaces=NS)
        borders = style.xpath(".//w:pPr/w:pBdr", namespaces=NS)
        fonts = style.xpath(".//w:rPr/w:rFonts", namespaces=NS)
        sizes = style.xpath(".//w:rPr/w:sz", namespaces=NS)
        color_desc = etree.tostring(colors[0]).decode() if colors else "none"
        font_desc = fonts[0].get(f"{{{W}}}ascii") if fonts else "none"
        size_desc = sizes[0].get(f"{{{W}}}val") if sizes else "none"
        print(
            f"{style_id}: color={color_desc} | paragraph_borders={len(borders)} "
            f"| font={font_desc} | half_points={size_desc}"
        )


if __name__ == "__main__":
    main()
```

### tools/github_push.ps1

```powershell
# Create the GitHub repository (if needed) and push the current branch to it.
#
#   powershell -ExecutionPolicy Bypass -File tools\github_push.ps1
#   powershell -ExecutionPolicy Bypass -File tools\github_push.ps1 -RepoName other-name -Private
#
# The script uses the GitHub credential that Git Credential Manager already stores on
# this machine. The token is never printed and never written to a file.
param(
    [string]$RepoName = "bankflow-ai-banking-assistant",
    [string]$Description = "BankFlow - AI Banking Assistant: full stack demo banking app built with React, Vite, Material UI and Django REST Framework, with JWT authentication, Recharts analytics and a rule based AI assistant.",
    [switch]$Private,
    [string]$ProjectPath = (Split-Path -Parent $PSScriptRoot)
)

$ErrorActionPreference = "Stop"
$env:GIT_TERMINAL_PROMPT = "0"
$env:GCM_INTERACTIVE = "never"

# ---------------------------------------------------------------- credential
$raw = "protocol=https`nhost=github.com`n`n" | git credential fill 2>$null
$cred = @{}
foreach ($line in ($raw | Where-Object { $_ -match "=" })) {
    $parts = $line -split "=", 2
    $cred[$parts[0]] = $parts[1]
}
$token = $cred["password"]
if (-not $token) {
    throw "No GitHub credential found. Sign in once with Git Credential Manager, then run this script again."
}
$headers = @{
    Authorization          = "token $token"
    Accept                 = "application/vnd.github+json"
    "User-Agent"           = "BankFlow-Push"
}

# ------------------------------------------------------------------- account
$me = Invoke-RestMethod -Uri "https://api.github.com/user" -Headers $headers
Write-Output "Signed in to GitHub as $($me.login)"
$owner = $me.login

# ------------------------------------------------------------------ create
$repoUrl = "https://api.github.com/repos/$owner/$RepoName"
$exists = $true
try {
    $repo = Invoke-RestMethod -Uri $repoUrl -Headers $headers
} catch {
    $exists = $false
}

if ($exists) {
    Write-Output "Repository $owner/$RepoName already exists - pushing into it."
} else {
    $body = @{
        name        = $RepoName
        description = $Description
        private     = [bool]$Private
        has_issues  = $true
        has_wiki    = $false
    } | ConvertTo-Json
    $repo = Invoke-RestMethod -Method Post -Uri "https://api.github.com/user/repos" `
        -Headers $headers -ContentType "application/json" -Body $body
    Write-Output "Created repository $($repo.full_name) ($($repo.visibility))"
}

$topics = @("react", "django", "django-rest-framework", "jwt", "material-ui", "recharts",
            "banking-app", "full-stack", "demo-application")
try {
    Invoke-RestMethod -Method Put -Uri "$repoUrl/topics" -Headers $headers `
        -ContentType "application/json" -Body (@{ names = $topics } | ConvertTo-Json) | Out-Null
    Write-Output "Topics updated."
} catch {
    Write-Output "Topics could not be set (not important)."
}

# -------------------------------------------------------------------- push
Push-Location $ProjectPath
try {
    $remote = "https://github.com/$owner/$RepoName.git"
    if ((git remote) -contains "origin") {
        git remote remove origin | Out-Null
    }
    git remote add origin $remote
    Write-Output "Pushing to $remote"
    # git writes progress to stderr, so read it as text instead of letting it stop the script.
    $pushOutput = & git push -u origin HEAD 2>&1 | Out-String
    Write-Output $pushOutput.Trim()
    if ($LASTEXITCODE -ne 0) {
        throw "git push failed with exit code $LASTEXITCODE"
    }
} finally {
    Pop-Location
}

# ------------------------------------------------------------------ verify
$final = Invoke-RestMethod -Uri $repoUrl -Headers $headers
Write-Output ""
Write-Output "Repository: $($final.html_url)"
Write-Output "Visibility: $($final.visibility)"
Write-Output "Default branch: $($final.default_branch)"
Write-Output "Size on GitHub: $([math]::Round($final.size / 1024, 1)) MB"
```

### tools/pdf_to_png.py

```python
#!/usr/bin/env python3
"""Rasterize a PDF into page PNGs for visual QA (pypdfium2 based).

Usage: python pdf_to_png.py input.pdf out_dir [dpi] [first] [last]
"""
from __future__ import annotations

import sys
from pathlib import Path

import pypdfium2 as pdfium


def main() -> None:
    pdf_path = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 110
    first = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    last = int(sys.argv[5]) if len(sys.argv) > 5 else 0

    out_dir.mkdir(parents=True, exist_ok=True)
    pdf = pdfium.PdfDocument(str(pdf_path))
    total = len(pdf)
    stop = last if last else total
    scale = dpi / 72

    for index in range(first - 1, min(stop, total)):
        page = pdf[index]
        image = page.render(scale=scale).to_pil()
        target = out_dir / f"page-{index + 1:04d}.png"
        image.save(target)
    print(f"pdf pages: {total}; wrote {max(0, min(stop, total) - first + 1)} png(s) to {out_dir}")


if __name__ == "__main__":
    main()
```

### tools/qa_docx_pdf.py

```python
#!/usr/bin/env python3
"""Programmatic layout QA for the rendered BankFlow guide PDF.

Checks performed:
  1. page count and per-page word counts (blank page detection)
  2. text that runs past the printable area (clipping risk)
  3. missing glyph markers and characters outside the expected set
  4. every source file starts and ends inside the rendered document
  5. contents page numbers match the actual heading pages

Usage: python qa_docx_pdf.py rendered.pdf page_map.json
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pdfplumber

# The project root: override with BANKFLOW_ROOT, otherwise use the parent of tools/.
ROOT = Path(os.environ.get("BANKFLOW_ROOT") or Path(__file__).resolve().parents[1])
RIGHT_MARGIN_PT = 53.9 * 0.6  # tolerated right edge (points, generous)
BOTTOM_TOLERANCE_PT = 8


def norm(text: str) -> str:
    return " ".join(text.replace("\u00a0", " ").split())


def main() -> None:
    pdf_path = Path(sys.argv[1])
    page_map = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8-sig"))

    over_right = []
    over_bottom = []
    blank_pages = []
    bad_chars = {}
    page_texts = []
    rupee_fonts = {}

    with pdfplumber.open(pdf_path) as pdf:
        page_width, page_height = pdf.pages[0].width, pdf.pages[0].height
        for index, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            page_texts.append(text)
            if len(norm(text)) < 20:
                blank_pages.append(index)
            for char in page.chars:
                if not char.get("text"):
                    continue
                if char["x1"] > page_width - RIGHT_MARGIN_PT + 40:
                    over_right.append((index, round(char["x1"], 1), char["text"]))
                if char["bottom"] > page_height - BOTTOM_TOLERANCE_PT:
                    over_bottom.append((index, round(char["bottom"], 1), char["text"]))
                if char["text"] == "\u20b9":
                    rupee_fonts[char["fontname"]] = rupee_fonts.get(char["fontname"], 0) + 1
                if char["text"] in {"\ufffd", "\u25a1", "\u25af"}:
                    bad_chars[char["text"]] = bad_chars.get(char["text"], 0) + 1

    full_text = norm("\n".join(page_texts))

    manifest = [
        "backend/requirements.txt", "backend/.env.example", "backend/.gitignore", "backend/manage.py",
        "backend/config/settings.py", "backend/config/urls.py", "backend/config/wsgi.py",
        "backend/config/asgi.py", "backend/users/models.py", "backend/users/signals.py",
        "backend/users/permissions.py", "backend/users/serializers.py", "backend/users/views.py",
        "backend/users/urls/auth_urls.py", "backend/users/urls/profile_urls.py",
        "backend/users/admin.py", "backend/users/tests.py", "backend/banking/models.py",
        "backend/banking/services.py", "backend/banking/serializers.py", "backend/banking/views.py",
        "backend/banking/admin_views.py", "backend/banking/urls/customer_urls.py",
        "backend/banking/urls/admin_urls.py", "backend/banking/admin.py",
        "backend/banking/management/commands/seed_demo.py", "backend/banking/tests.py",
        "backend/assistant/models.py", "backend/assistant/ai_service.py",
        "backend/assistant/serializers.py", "backend/assistant/views.py",
        "backend/assistant/urls.py", "backend/assistant/admin.py", "backend/assistant/tests.py",
        "frontend/package.json", "frontend/vite.config.js", "frontend/index.html",
        "frontend/.env.example", "frontend/.gitignore", "frontend/public/bankflow.svg",
        "frontend/src/index.css",
        "frontend/src/theme.js", "frontend/src/main.jsx", "frontend/src/App.jsx",
        "frontend/src/services/api.js", "frontend/src/services/authService.js",
        "frontend/src/services/bankingService.js", "frontend/src/services/aiService.js",
        "frontend/src/services/adminService.js", "frontend/src/context/AuthContext.jsx",
        "frontend/src/utils/formatCurrency.js", "frontend/src/utils/calculations.js",
        "frontend/src/components/AppLayout.jsx", "frontend/src/components/Navbar.jsx",
        "frontend/src/components/Sidebar.jsx", "frontend/src/components/DashboardCard.jsx",
        "frontend/src/components/TransactionTable.jsx", "frontend/src/components/LoanCard.jsx",
        "frontend/src/components/ChatMessage.jsx", "frontend/src/components/ProtectedRoute.jsx",
        "frontend/src/components/Common.jsx", "frontend/src/pages/Landing.jsx",
        "frontend/src/pages/Login.jsx", "frontend/src/pages/Register.jsx",
        "frontend/src/pages/Dashboard.jsx", "frontend/src/pages/Account.jsx",
        "frontend/src/pages/Transactions.jsx", "frontend/src/pages/TransactionDetails.jsx",
        "frontend/src/pages/Loans.jsx", "frontend/src/pages/LoanDetails.jsx",
        "frontend/src/pages/EMICalculator.jsx", "frontend/src/pages/AIAssistant.jsx",
        "frontend/src/pages/Notifications.jsx", "frontend/src/pages/Profile.jsx",
        "frontend/src/pages/NotFound.jsx", "frontend/src/pages/admin/AdminDashboard.jsx",
        "frontend/src/pages/admin/CustomerManagement.jsx",
        "frontend/src/pages/admin/TransactionManagement.jsx",
        "frontend/src/pages/admin/LoanManagement.jsx",
        "frontend/src/pages/admin/AdminAnalytics.jsx", "frontend/src/pages/admin/AIMonitor.jsx",
    ]

    missing_files = []
    for rel in manifest:
        path = ROOT / rel
        if not path.exists():
            missing_files.append(f"{rel} (missing on disk)")
            continue
        if norm(rel) not in full_text:
            missing_files.append(f"{rel} (file heading not found in PDF)")
            continue
        lines = [ln for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
        first, last = norm(lines[0]), norm(lines[-1])
        if first and first not in full_text:
            missing_files.append(f"{rel} (first line not rendered)")
        if last and last not in full_text:
            missing_files.append(f"{rel} (last line not rendered)")

    contents_ok = []
    for key, page in page_map.items():
        if key == "contents":
            continue
        needle = None
        if key.startswith("step"):
            needle = f"Step {key[4:]}."
        elif key.startswith("lesson"):
            needle = f"Lesson {key[6:]}."
        elif key.startswith("appendix"):
            needle = f"Appendix {key[-1].upper()}."
        if needle:
            index = page - 1
            hit = index < len(page_texts) and needle in page_texts[index]
            contents_ok.append((key, page, hit))

    print(f"pages: {len(page_texts)}")
    print(f"blank pages: {blank_pages or 'none'}")
    print(f"chars past right edge: {len(over_right)}")
    if over_right[:5]:
        print("  samples:", over_right[:5])
    print(f"chars past bottom edge: {len(over_bottom)}")
    if over_bottom[:5]:
        print("  samples:", over_bottom[:5])
    print(f"missing glyph markers: {bad_chars or 'none'}")
    print(f"rupee glyph fonts: {rupee_fonts}")
    print(f"file check failures: {missing_files or 'none'}")
    print(f"contents page mismatches: {[c for c in contents_ok if not c[2]] or 'none'}")


if __name__ == "__main__":
    main()
```

### tools/word_export.ps1

```powershell
# Export a DOCX to PDF with Microsoft Word and record the page number of every
# Heading 1 (used to build an accurate contents page in the BankFlow guide).
param(
    [Parameter(Mandatory = $true)][string]$Docx,
    [Parameter(Mandatory = $true)][string]$Pdf,
    [string]$PageMapJson = ""
)

$ErrorActionPreference = "Stop"

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0

$doc = $null
try {
    $doc = $word.Documents.Open($Docx, $false, $true)

    if ($PageMapJson -ne "") {
        $map = [ordered]@{}
        $count = $doc.Paragraphs.Count
        for ($i = 1; $i -le $count; $i++) {
            $paragraph = $doc.Paragraphs.Item($i)
            $styleName = $paragraph.Style.NameLocal
            if ($styleName -notmatch '^Heading 1') { continue }  # "Heading 1" / "Heading 1,Heading 1"

            $text = ($paragraph.Range.Text -replace "`r", "" -replace "`a", "").Trim()
            if ($text -eq "") { continue }

            $page = $paragraph.Range.Information(3)   # wdActiveEndPageNumber

            if ($text -match '^(Step|Lesson)\s+(\d+)\.') {
                $prefix = $Matches[1].ToLower()
                $map["$prefix$($Matches[2])"] = [int]$page
            }
            elseif ($text -match '^Appendix\s+([A-D])\.') {
                $map["appendix$($Matches[1].ToLower())"] = [int]$page
            }
            elseif ($text -match '^Contents$') {
                $map["contents"] = [int]$page
            }
        }
        ($map | ConvertTo-Json) | Set-Content -LiteralPath $PageMapJson -Encoding UTF8
        Write-Output "Page map entries: $($map.Keys.Count)"
    }

    $doc.ExportAsFixedFormat($Pdf, 17)   # wdExportFormatPDF
    Write-Output "PDF pages: $($doc.ComputeStatistics(2))"   # wdStatisticPages
}
finally {
    if ($doc) { $doc.Close($false) }
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}
```

