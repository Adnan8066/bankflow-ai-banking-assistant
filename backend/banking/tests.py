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
