from rest_framework.permissions import BasePermission


class IsCustomerUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profile.type == "customer"


class IsBusinessUser(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        profile = getattr(
            request.user,
            "profile",
            None,
        )

        return profile is not None and profile.type == "business"


class IsOrderBusinessOwner(BasePermission):
    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):
        return obj.business_user == request.user


class IsStaffUser(BasePermission):
    def has_permission(
        self,
        request,
        view,
    ):
        return request.user.is_authenticated and request.user.is_staff
