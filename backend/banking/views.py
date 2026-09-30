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


class LoanWithdrawView(APIView):
    """DELETE /api/loans/<id>/withdraw/ - cancel your own pending application."""

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        loan = Loan.objects.filter(pk=pk, user=request.user).first()
        if not loan:
            return Response({"detail": "Loan application not found."},
                            status=status.HTTP_404_NOT_FOUND)
        if loan.status != Loan.Status.PENDING:
            return Response(
                {"detail": "Only an application that is still pending can be withdrawn."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        loan_id = loan.loan_id
        loan.delete()
        return Response({"message": f"Application {loan_id} was withdrawn."})


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
