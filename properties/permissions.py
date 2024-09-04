
from rest_framework import permissions

from core.models import Profile
from properties.models import Property, PropertyImage, Collection


class IsHostOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_authenticated:
            return request.user.profile.role == Profile.Role.HOST
        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # check is obj instance of models for access to the user object
        if isinstance(obj, Property) or isinstance(obj, Collection):
            return obj.host.user == request.user

        if isinstance(obj, PropertyImage):
            return obj.property.host.user == request.user

        return False
