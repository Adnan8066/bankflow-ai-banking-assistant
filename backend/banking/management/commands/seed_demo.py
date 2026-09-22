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
