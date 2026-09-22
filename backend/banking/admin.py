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
