"""Business logic for BankFlow.

Views stay thin; every calculation that is reused by the dashboard, the EMI
calculator and the AI assistant lives here.
"""
import random
from datetime import date, datetime, timedelta

from django.utils import timezone

from .models import Account, Loan, Notification, Transaction, account_balance

CATEGORY_COLORS = {
    "Salary": "#16a34a",
    "Food": "#f97316",
    "Shopping": "#8b5cf6",
    "Travel": "#0ea5e9",
    "Bills": "#ef4444",
    "Entertainment": "#ec4899",
    "Transfer": "#64748b",
    "Other": "#94a3b8",
}


# ------------------------------------------------------------------ helpers --
def to_float(value):
    return float(value or 0)


def aware(value):
    """Turn a `date` or naive `datetime` into a timezone-aware datetime."""
    if isinstance(value, datetime):
        return value if timezone.is_aware(value) else timezone.make_aware(value)
    return timezone.make_aware(datetime.combine(value, datetime.min.time()))


def format_inr(value):
    """Format a number the Indian way: 18450 -> '18,450'."""
    value = float(value or 0)
    whole = f"{abs(value):,.0f}"
    return f"{'-' if value < 0 else ''}{whole}"


def calculate_emi(principal, annual_rate, months):
    """Standard reducing-balance EMI formula."""
    principal = float(principal)
    annual_rate = float(annual_rate)
    months = int(months) or 1
    monthly_rate = annual_rate / 12 / 100
    if monthly_rate == 0:
        emi = principal / months
    else:
        factor = (1 + monthly_rate) ** months
        emi = principal * monthly_rate * factor / (factor - 1)
    total_payment = emi * months
    return {
        "monthly_emi": round(emi, 2),
        "total_interest": round(total_payment - principal, 2),
        "total_payment": round(total_payment, 2),
        "principal": round(principal, 2),
        "tenure_months": months,
        "interest_rate": annual_rate,
    }


def month_bounds(reference=None):
    reference = reference or timezone.localdate()
    start = reference.replace(day=1)
    next_month = (start + timedelta(days=32)).replace(day=1)
    return start, next_month


def previous_month_bounds(reference=None):
    start, _ = month_bounds(reference)
    last_day_previous = start - timedelta(days=1)
    return month_bounds(last_day_previous)


def customer_transactions(user):
    return Transaction.objects.filter(account__user=user)


def period_totals(user, start, end):
    qs = customer_transactions(user).filter(date__gte=aware(start), date__lt=aware(end),
                                            status=Transaction.Status.COMPLETED)
    income = sum(to_float(t.amount) for t in qs if t.transaction_type == Transaction.Type.CREDIT)
    expense = sum(to_float(t.amount) for t in qs if t.transaction_type == Transaction.Type.DEBIT)
    return {"income": round(income, 2), "expense": round(expense, 2),
            "count": qs.count()}


# ---------------------------------------------------- dashboard + analytics --
def get_account(user):
    return Account.objects.filter(user=user).order_by("created_at").first()


def get_dashboard(user):
    """Everything the customer dashboard and the AI need in one place."""
    start, end = month_bounds()
    prev_start, prev_end = previous_month_bounds()
    current = period_totals(user, start, end)
    previous = period_totals(user, prev_start, prev_end)

    categories = category_breakdown(user, start, end)
    loans = Loan.objects.filter(user=user)
    active_loans = loans.filter(status__in=[Loan.Status.ACTIVE, Loan.Status.APPROVED])

    return {
        "balance": round(account_balance(user), 2),
        "monthly_income": current["income"],
        "monthly_expenses": current["expense"],
        "monthly_savings": round(current["income"] - current["expense"], 2),
        "previous_month_income": previous["income"],
        "previous_month_expenses": previous["expense"],
        "expense_change_percent": percent_change(previous["expense"], current["expense"]),
        "transaction_count": current["count"],
        "active_loans": active_loans.count(),
        "total_loans": loans.count(),
        "total_outstanding": round(sum(to_float(l.remaining_amount) for l in active_loans), 2),
        "monthly_emi_total": round(sum(to_float(l.emi) for l in active_loans), 2),
        "unread_notifications": Notification.unread_count(user),
        "top_category": categories[0] if categories else None,
        "spending_categories": categories,
        "monthly_trend": monthly_trend(user, months=6),
        "loan_status_breakdown": loan_status_breakdown(user),
        "recent_transactions": [
            {
                "id": t.id,
                "transaction_id": t.transaction_id,
                "date": t.date.isoformat(),
                "description": t.description,
                "category": t.category,
                "transaction_type": t.transaction_type,
                "amount": to_float(t.amount),
                "status": t.status,
            }
            for t in customer_transactions(user).select_related("account")[:5]
        ],
    }


def percent_change(old, new):
    old = float(old or 0)
    new = float(new or 0)
    if old == 0:
        return 0 if new == 0 else 100.0
    return round((new - old) / old * 100, 1)


def category_breakdown(user, start=None, end=None):
    start = start or month_bounds()[0]
    end = end or month_bounds()[1]
    qs = customer_transactions(user).filter(
        transaction_type=Transaction.Type.DEBIT,
        status=Transaction.Status.COMPLETED,
        date__gte=aware(start),
        date__lt=aware(end),
    )
    totals = {}
    for txn in qs:
        totals[txn.category] = totals.get(txn.category, 0) + to_float(txn.amount)
    data = [
        {"category": category, "amount": round(amount, 2),
         "color": CATEGORY_COLORS.get(category, "#94a3b8")}
        for category, amount in totals.items()
    ]
    return sorted(data, key=lambda item: item["amount"], reverse=True)


def category_total(user, category_names, start=None, end=None):
    breakdown = category_breakdown(user, start, end)
    wanted = [name.lower() for name in category_names]
    return round(
        sum(item["amount"] for item in breakdown if item["category"].lower() in wanted), 2
    )


def big_category_names():
    """All categories a customer can ask the assistant about."""
    return [category for category, _ in Transaction.Category.choices]


def monthly_trend(user, months=6):
    today = timezone.localdate()
    series = []
    cursor = today.replace(day=1)
    for _ in range(months):
        start, end = month_bounds(cursor)
        totals = period_totals(user, start, end)
        series.append({
            "month": start.strftime("%b %Y"),
            "short_month": start.strftime("%b"),
            "income": totals["income"],
            "expense": totals["expense"],
            "savings": round(totals["income"] - totals["expense"], 2),
            "transactions": totals["count"],
        })
        cursor = (start - timedelta(days=1)).replace(day=1)
    return list(reversed(series))


def loan_status_breakdown(user=None):
    qs = Loan.objects.all() if user is None else Loan.objects.filter(user=user)
    counts = {}
    for loan in qs:
        counts[loan.status] = counts.get(loan.status, 0) + 1
    return [{"status": status, "label": label, "count": counts.get(status, 0)}
            for status, label in Loan.Status.choices]


def biggest_expense(user, start=None, end=None):
    start = start or month_bounds()[0]
    end = end or month_bounds()[1]
    txn = customer_transactions(user).filter(
        transaction_type=Transaction.Type.DEBIT,
        status=Transaction.Status.COMPLETED,
        date__gte=aware(start),
        date__lt=aware(end),
    ).order_by("-amount").first()
    if not txn:
        return None
    return {
        "description": txn.description,
        "category": txn.category,
        "amount": to_float(txn.amount),
        "date": txn.date.isoformat(),
        "transaction_id": txn.transaction_id,
    }


# --------------------------------------------------------------- bootstrapping -
def random_account_number():
    return "5" + "".join(random.choices("0123456789", k=11))


def record_transaction(account, *, amount, description, category,
                       transaction_type, when=None, status="COMPLETED"):
    """Create a transaction and keep the account balance consistent."""
    when = when or timezone.now()
    amount = float(amount)
    if transaction_type == Transaction.Type.CREDIT:
        account.balance = to_float(account.balance) + amount
    else:
        account.balance = to_float(account.balance) - amount
    account.save(update_fields=["balance"])
    return Transaction.objects.create(
        account=account,
        date=when,
        description=description,
        category=category,
        transaction_type=transaction_type,
        amount=amount,
        status=status,
        balance_after=account.balance,
    )


def bootstrap_customer(user):
    """New demo customers immediately get an account + welcome notification."""
    account, _ = Account.objects.get_or_create(
        user=user,
        defaults={"account_number": random_account_number(), "balance": 0},
    )
    Notification.objects.get_or_create(
        user=user,
        title="Welcome to BankFlow",
        defaults={
            "message": (
                "Your demo savings account is ready. Explore the dashboard, the AI "
                "assistant and the EMI calculator with completely fictional data."
            ),
            "notification_type": Notification.NotificationType.SYSTEM,
        },
    )
    return account


def month_start_offset(offset=0):
    """First day of the current month, minus `offset` months."""
    start = timezone.localdate().replace(day=1)
    for _ in range(offset):
        start = (start - timedelta(days=1)).replace(day=1)
    return start


def demo_month_datetime(month_offset, day, hour=11, minute=30):
    """A safe date inside a month (never in the future, never past month end)."""
    start = month_start_offset(month_offset)
    next_month = (start + timedelta(days=32)).replace(day=1)
    last_day = (next_month - timedelta(days=1)).day
    day = min(day, last_day)
    if month_offset == 0:
        day = min(day, timezone.localdate().day)
    return timezone.make_aware(
        datetime.combine(start.replace(day=day), datetime.min.time())
    ) + timedelta(hours=hour, minutes=minute)


# (month offset, day, amount, description, category, type)
DEMO_LEDGER = [
    # ---------------------------------------------------- two months ago ----
    (2, 1, 45000, "Monthly salary credited - Infosys Ltd", "Salary", "CREDIT"),
    (2, 4, 8900, "Reliance Digital - headphones and speaker", "Shopping", "DEBIT"),
    (2, 7, 3600, "BigBasket monthly groceries", "Food", "DEBIT"),
    (2, 10, 2400, "Mobile postpaid bill - Airtel", "Bills", "DEBIT"),
    (2, 13, 1800, "Ola and Uber rides", "Travel", "DEBIT"),
    (2, 16, 1200, "PVR Cinemas and Netflix", "Entertainment", "DEBIT"),
    (2, 20, 2500, "Transfer to savings", "Transfer", "DEBIT"),
    (2, 25, 21500, "Credit card bill payment - BankFlow demo card", "Bills", "DEBIT"),
    # -------------------------------------------------------- last month ----
    (1, 1, 45000, "Monthly salary credited - Infosys Ltd", "Salary", "CREDIT"),
    (1, 3, 5600, "Myntra - festive shopping", "Shopping", "DEBIT"),
    (1, 5, 2100, "BigBasket groceries", "Food", "DEBIT"),
    (1, 8, 1400, "Water bill - BWSSB", "Bills", "DEBIT"),
    (1, 11, 2600, "Weekend trip fuel", "Travel", "DEBIT"),
    (1, 14, 700, "Spotify and Audible subscriptions", "Entertainment", "DEBIT"),
    (1, 18, 1900, "Restaurant - family dinner", "Food", "DEBIT"),
    (1, 22, 1900, "Transfer to savings", "Transfer", "DEBIT"),
    (1, 26, 12000, "Freelance project payment", "Other", "CREDIT"),
    # ------------------------------------------------------ this month -----
    (0, 1, 45000, "Monthly salary credited - Infosys Ltd", "Salary", "CREDIT"),
    (0, 2, 2450, "Amazon - electronics order", "Shopping", "DEBIT"),
    (0, 3, 1200, "Zomato - dinner order", "Food", "DEBIT"),
    (0, 4, 1500, "Electricity bill - BESCOM", "Bills", "DEBIT"),
    (0, 5, 2000, "IRCTC train tickets", "Travel", "DEBIT"),
    (0, 6, 800, "PVR Cinemas - movie tickets", "Entertainment", "DEBIT"),
    (0, 7, 4750, "Croma - new laptop accessories", "Shopping", "DEBIT"),
    (0, 8, 950, "Swiggy - lunch order", "Food", "DEBIT"),
    (0, 9, 1800, "UPI transfer to friend", "Transfer", "DEBIT"),
    (0, 10, 3000, "Insurance premium - demo policy", "Other", "DEBIT"),
]


def demo_transaction_seed():
    """28 fictional transactions across three months.

    This month: income ₹45,000, expenses ₹18,450, biggest category Shopping ₹7,200.
    """
    entries = []
    for month_offset, day, amount, description, category, txn_type in DEMO_LEDGER:
        entries.append({
            "when": demo_month_datetime(month_offset, day),
            "amount": amount,
            "description": description,
            "category": category,
            "transaction_type": txn_type,
        })
    return entries
