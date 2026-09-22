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
