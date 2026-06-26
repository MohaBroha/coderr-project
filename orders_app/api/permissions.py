from rest_framework.permissions import BasePermission


class IsCustomerUser(BasePermission):
    """
    Permission that allows access only to authenticated customer users.
    """

    def has_permission(self, request, view):
        """
        Check whether the requesting user is an authenticated customer.
        """
        return request.user.is_authenticated and request.user.profile.type == "customer"


class IsBusinessUser(BasePermission):
    """
    Permission that allows access only to authenticated business users.
    """

    def has_permission(self, request, view):
        """
        Check whether the requesting user is an authenticated business user.
        """
        if not request.user.is_authenticated:
            return False

        profile = getattr(
            request.user,
            "profile",
            None,
        )

        return profile is not None and profile.type == "business"


class IsOrderBusinessOwner(BasePermission):
    """
    Permission that allows access only to the business user who owns the order.
    """

    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):
        """
        Check whether the requesting user owns the requested order.
        """
        return obj.business_user == request.user


class IsStaffUser(BasePermission):
    """
    Permission that allows access only to authenticated staff users.
    """

    def has_permission(
        self,
        request,
        view,
    ):
        """
        Check whether the requesting user is an authenticated staff user.
        """
        return request.user.is_authenticated and request.user.is_staff
