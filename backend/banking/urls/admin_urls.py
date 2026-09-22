from django.urls import path

from banking.admin_views import (
    AdminAnalyticsView,
    AdminCustomerDetailView,
    AdminCustomerListView,
    AdminLoanListView,
    AdminLoanUpdateView,
    AdminOverviewView,
    AdminTransactionListView,
    AdminUserListView,
)

urlpatterns = [
    path("analytics/", AdminAnalyticsView.as_view(), name="admin-analytics"),
    path("analytics/overview/", AdminOverviewView.as_view(), name="admin-overview"),
    path("customers/", AdminCustomerListView.as_view(), name="admin-customers"),
    path("customers/<int:pk>/", AdminCustomerDetailView.as_view(), name="admin-customer-detail"),
    path("transactions/", AdminTransactionListView.as_view(), name="admin-transactions"),
    path("loans/", AdminLoanListView.as_view(), name="admin-loans"),
    path("loans/<int:pk>/", AdminLoanUpdateView.as_view(), name="admin-loan-update"),
    path("users/", AdminUserListView.as_view(), name="admin-users"),
]
