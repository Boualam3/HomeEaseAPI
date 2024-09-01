from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from core.models import Profile
from core.serializers import ProfileSerializer


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    # overrides the permissions in 'GET' and 'PUT' methods  in decorators below by adding another permission IsAuthenticated
    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        # like destructuring in js
        # get_or_create return tuple we unpack for get first value below
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
