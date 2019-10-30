from rest_framework.permissions import BasePermission


class IsAuthenticatedOnlySelf(BasePermission):
    """
    Allows access only to authenticated user.
    """

    def has_permission(self, request, view):
        print(request)
        return bool(request.user and request.user.is_authenticated)