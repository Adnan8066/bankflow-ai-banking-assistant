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
