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
