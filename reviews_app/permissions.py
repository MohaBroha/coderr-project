from rest_framework.permissions import BasePermission


class IsCustomerUser(BasePermission):
    def has_permission(self, request, view):
        return (
            hasattr(request.user, "profile") and request.user.profile.type == "customer"
        )
