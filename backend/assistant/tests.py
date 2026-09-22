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
