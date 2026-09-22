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
