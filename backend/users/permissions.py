from rest_framework.permissions import BasePermission


class IsBankStaff(BasePermission):
    """Only bank employees / admins can reach the admin API."""

    message = "You do not have permission to access the bank employee area."

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.is_admin_role)
