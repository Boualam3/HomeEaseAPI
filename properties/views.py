from urllib import request
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from rest_framework import status
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend as FilterBackend
from .serializers import CategorySerializer, CollectionSerializer, PropertyImageSerializer, PropertySerializer
from rest_framework.exceptions import PermissionDenied
from core.models import Profile
from .models import Category, Collection, Property, PropertyImage
from .permissions import IsHostOrReadOnly, IsOwnerOrReadOnly


# * We Make this Base class for achieve DRY in update/destroy operations sometimes permissions_classes don't working properly but when we call check_objects_permissions it works
class BaseOwnershipViewSet(ModelViewSet):
    """
    A base viewset that includes ownership checks for update and destroy actions.
    """

    def check_object_permissions(self, request, obj):
        """
        Check if the user has ownership of the object.
        """
        super().check_object_permissions(request, obj)

        # Property and Collection has host attribute
        if hasattr(obj, 'host'):
            if obj.host.user != request.user:
                raise PermissionDenied(
                    "You do not have permission to perform this action (from base).")

        # PropertyImage has property attribute ;will add Reviews here it should has property too
        if hasattr(obj, 'property'):
            if obj.property.host.user != request.user:
                raise PermissionDenied(
                    "You do not have permission to perform this action (from base).")

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        self.check_object_permissions(request, obj)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        self.check_object_permissions(request, obj)
        return super().destroy(request, *args, **kwargs)


class PropertyImageViewSet(BaseOwnershipViewSet):
    serializer_class = PropertyImageSerializer
    permission_classes = [IsOwnerOrReadOnly, IsHostOrReadOnly]

    def get_serializer_context(self):
        return {'property_id': self.kwargs['property_pk']}

    def get_queryset(self):
        return PropertyImage.objects.filter(property_id=self.kwargs['property_pk'])


class PropertyViewSet(BaseOwnershipViewSet):
    queryset = Property.objects.prefetch_related('images').all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticatedOrReadOnly,
                          IsHostOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [FilterBackend, SearchFilter, OrderingFilter]

    # pagination_class = DefaultPagination
    search_fields = ['title', 'description', ]
    ordering_fields = ['price', 'last_update', ]
    # TODO use filterset_class = PropertyFilter instead of filterset_fields
    # https://django-filter.readthedocs.io/en/stable/ref/filterset.html
    filterset_fields = ['category_id']

    def get_serializer_context(self):
        return {'hosted_user_id': self.request.user.profile.id}

    def destroy(self, request, *args, **kwargs):
        property_obj = self.get_object()
        self.check_object_permissions(request, property_obj)
        # property_obj shouldn't be associated with any appointments to delete it
        # if propert.(instance_model).exists():
        #     return Response({'error': 'Property cannot be deleted as it is associated with an appointment'},
        #                     status=status.HTTP_400_BAD_REQUEST)

        # if no associations exist, proceed with deletion
        # return super().destroy(request, *args, **kwargs)


class CollectionViewSet(BaseOwnershipViewSet):
    queryset = Collection.objects.annotate(
        properties_count=Count('properties')).all()
    serializer_class = CollectionSerializer
    permission_classes = [IsHostOrReadOnly, IsOwnerOrReadOnly]

    def get_serializer_context(self):
        return {'hosted_user_id': self.request.user.profile.id}

    def destroy(self, request, *args, **kwargs):
        # in deletion ,collection should be not associated with properties otherwise will not delete
        collection = get_object_or_404(
            Collection.objects.annotate(
                properties_count=Count('properties')), pk=kwargs['pk']
        )
        self.check_object_permissions(request, collection)
        if collection.properties.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it has more than one property'})
        return super().destroy(request, *args, **kwargs)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(
        properties_count=Count('properties')).all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        """
        Override get_permissions to provide permission handling based on actions
        drf expects list of instances of permissions when we override get_permissions method
        behind scenes it loop thought list and get class of each instance using 'obj.__class__' 
        """
        if self.action in ['retrieve', 'list']:
            return [AllowAny()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]

    def destroy(self, request, *args, **kwargs):
        # in deletion ,category should be not associated with properties otherwise will not delete
        collection = get_object_or_404(Collection.objects.annotate(
            properties_count=Count('properties')), pk=kwargs['pk'])
        if collection.properties.count() > 0:
            return Response({'error': 'Category cannot be deleted because it has more than one property'})
        return super().destroy(request, *args, **kwargs)
