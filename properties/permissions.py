
from rest_framework import permissions

from core.models import Profile
from properties.models import Property, PropertyImage, Collection, Review


class IsHostOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_authenticated:
            return request.user.profile.role == Profile.Role.HOST
        return False

    def has_object_permission(self, request, view, obj):
        """
        Check if the user has ownership of the object.
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        # Property and Collection has host attribute
        if hasattr(obj, 'host'):
            return obj.host.user == request.user
            # raise PermissionDenied(
            #     "You do not have permission to perform this action")

        # PropertyImage has property attribute ;will add Reviews here it should has property too
        if hasattr(obj, 'property'):
            return obj.property.host.user == request.user

        return False


class IsGuestOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_authenticated:
            return request.user.profile.role == Profile.Role.GUEST
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow property host to modify reviews
        # if hasattr(obj, 'property'):
        #     return obj.property.host.user == request.user

        # Allow the review owner to update or delete their own review
        if hasattr(obj, 'profile'):
            return obj.profile == request.user.profile

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
        if isinstance(obj, (Property, Collection)):
            return obj.host.user == request.user

        if isinstance(obj, PropertyImage):
            return obj.property.host.user == request.user  # True /False

        return False
