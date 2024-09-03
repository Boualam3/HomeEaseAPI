from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, OR
from core.models import Profile
from core.serializers import ProfileSerializer
from .permissions import IsProfileOwner


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminUser]  # default perm for all actions

    # override permissions in profile/ endpoints default is allow-admins-only

    def get_permissions(self):
        if self.action == 'retrieve':
            return [OR(IsProfileOwner(), IsAdminUser())]

        elif self.action in ['update', 'partial_update', 'destroy']:
            return [OR(IsProfileOwner(), IsAdminUser())]
        elif self.action in ['list', 'create']:
            return [IsAdminUser()]
        return super().get_permissions()

    # overrides the permissions in 'GET' and 'PUT' methods  in decorators below by adding another permission IsAuthenticated and IsProfileOwner

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsProfileOwner])
    def me(self, request):
        profile = Profile.objects.get(
            user_id=request.user.id)

        if request.method == 'GET':
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = ProfileSerializer(profile, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
