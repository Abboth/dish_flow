from rest_framework.permissions import BasePermission, IsAuthenticated


class IsDriver(BasePermission):
    """
    Allows access only to drivers.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_driver and IsAuthenticated())


class IsRestaurant(BasePermission):
    """
    Allows access only to restaurant owner user.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_restaurant and IsAuthenticated())