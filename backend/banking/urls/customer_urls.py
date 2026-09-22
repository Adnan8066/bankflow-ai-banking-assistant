from django.urls import path

from banking.views import (
    AccountView,
    DashboardView,
    EMICalculatorView,
    LoanDetailView,
    LoanListCreateView,
    MarkAllNotificationsReadView,
    NotificationListView,
    NotificationUpdateView,
    TransactionDetailView,
    TransactionListView,
)

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("account/", AccountView.as_view(), name="account"),
    path("transactions/", TransactionListView.as_view(), name="transaction-list"),
    path("transactions/<int:pk>/", TransactionDetailView.as_view(), name="transaction-detail"),
    path("loans/", LoanListCreateView.as_view(), name="loan-list"),
    path("loans/<int:pk>/", LoanDetailView.as_view(), name="loan-detail"),
    path("emi/", EMICalculatorView.as_view(), name="emi-calculator"),
    path("notifications/", NotificationListView.as_view(), name="notification-list"),
    path("notifications/read-all/", MarkAllNotificationsReadView.as_view(),
         name="notification-read-all"),
    path("notifications/<int:pk>/", NotificationUpdateView.as_view(), name="notification-update"),
]
