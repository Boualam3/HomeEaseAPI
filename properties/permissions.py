from pickle import TRUE
from rest_framework import permissions

from core.models import Profile


class IsHostReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_authenticated:
            try:
                profile = Profile.objects.get(user_id=request.user.id)
                return profile.role == Profile.Role.HOST
            except Profile.DoesNotExist:
                return False
        return False
