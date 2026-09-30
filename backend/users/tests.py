from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

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


class RefreshTokenTests(APITestCase):
    """A token for a deleted account must answer 401, never a server error."""

    def test_refresh_after_the_account_is_deleted_returns_401(self):
        user = User.objects.create_user(
            email="deleted@bankflow.com", password="Demo@12345", name="Deleted User"
        )
        refresh = RefreshToken.for_user(user)
        user.delete()

        response = self.client.post(reverse("token_refresh"), {"refresh": str(refresh)})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)

    def test_refresh_with_a_nonsense_token_returns_401(self):
        response = self.client.post(reverse("token_refresh"), {"refresh": "not-a-real-token"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PasswordResetTests(APITestCase):
    """The whole forgot password journey, from the request to logging in again."""

    def setUp(self):
        self.user = User.objects.create_user(
            email="forgot@bankflow.com", password="Demo@12345", name="Forgot Password"
        )

    def test_request_for_a_known_email_returns_a_reset_link(self):
        response = self.client.post(reverse("password-reset"), {"email": "forgot@bankflow.com"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("reset", response.data)
        self.assertTrue(response.data["reset"]["token"])
        self.assertTrue(response.data["reset"]["uid"])

    def test_request_for_an_unknown_email_stays_generic(self):
        response = self.client.post(reverse("password-reset"), {"email": "nobody@bankflow.com"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn("reset", response.data)
        self.assertIn("message", response.data)

    def test_confirm_replaces_the_password_and_allows_login(self):
        request = self.client.post(reverse("password-reset"), {"email": "forgot@bankflow.com"})
        reset = request.data["reset"]

        confirm = self.client.post(reverse("password-reset-confirm"), {
            "uid": reset["uid"], "token": reset["token"],
            "new_password": "Fresh@2026Pass", "confirm_password": "Fresh@2026Pass",
        })
        self.assertEqual(confirm.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("Fresh@2026Pass"))

        login = self.client.post(reverse("login"), {
            "email": "forgot@bankflow.com", "password": "Fresh@2026Pass",
        })
        self.assertEqual(login.status_code, status.HTTP_200_OK)
        self.assertIn("access", login.data)

    def test_confirm_rejects_a_tampered_token(self):
        request = self.client.post(reverse("password-reset"), {"email": "forgot@bankflow.com"})
        reset = request.data["reset"]

        confirm = self.client.post(reverse("password-reset-confirm"), {
            "uid": reset["uid"], "token": "not-the-right-token",
            "new_password": "Fresh@2026Pass", "confirm_password": "Fresh@2026Pass",
        })
        self.assertEqual(confirm.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("Demo@12345"))

    def test_confirm_rejects_mismatched_passwords(self):
        request = self.client.post(reverse("password-reset"), {"email": "forgot@bankflow.com"})
        reset = request.data["reset"]

        confirm = self.client.post(reverse("password-reset-confirm"), {
            "uid": reset["uid"], "token": reset["token"],
            "new_password": "Fresh@2026Pass", "confirm_password": "Different@2026",
        })
        self.assertEqual(confirm.status_code, status.HTTP_400_BAD_REQUEST)
