from rest_framework.permissions import BasePermission


class IsCustomerUser(BasePermission):
    """
    Permission that allows access only to customer users.
    """

    def has_permission(self, request, view):
        """
        Check whether the requesting user has a customer profile.
        """
        return (
            hasattr(request.user, "profile") and request.user.profile.type == "customer"
        )


class IsReviewOwner(BasePermission):
    """
    Permission that allows access only to the owner of a review.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check whether the requesting user owns the requested review.
        """
        return obj.reviewer == request.user
