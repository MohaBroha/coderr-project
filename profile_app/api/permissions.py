from rest_framework.permissions import BasePermission


class IsProfileOwner(BasePermission):
    """
    Permission that allows access only to the owner of a profile.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check whether the requesting user owns the requested profile.
        """
        return obj.user == request.user
