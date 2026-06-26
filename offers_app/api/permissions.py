from rest_framework.permissions import BasePermission


class IsBusinessUser(BasePermission):
    """
    Permission that allows access only to authenticated business users.
    """

    def has_permission(self, request, view):
        """
        Check whether the requesting user is an authenticated business user.
        """
        return request.user.is_authenticated and request.user.is_staff


class IsOfferOwner(BasePermission):
    """
    Permission that allows access only to the owner of an offer.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check whether the requesting user owns the requested offer.
        """
        return obj.user == request.user
