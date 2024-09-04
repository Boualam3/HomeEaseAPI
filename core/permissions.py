from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
     allow only admin users (is_staff) to edit or delete an object.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class IsProfileOwner(permissions.BasePermission):
    """
    Object-level allow owners of a profile object to edit or view it.
    """

    def has_object_permission(self, request, view, obj):
        # check if the profile's user is the same as the requesting user
        return obj.user == request.user
