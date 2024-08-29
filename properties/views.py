from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from .serializers import PropertyImageSerializer
from .models import PropertyImage


class PropertyImageViewSet(ModelViewSet):
    serializer_class = PropertyImageSerializer

    def get_serializer_context(self):
        return {'property_id': self.kwargs['property_pk']}

    def get_queryset(self):
        return PropertyImage.objects.filter(property_id=self.kwargs['property_pk'])