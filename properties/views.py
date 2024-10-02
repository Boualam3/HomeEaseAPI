from multiprocessing import context
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

from properties.pagination import DefaultPagination
from .serializers import CategorySerializer, CollectionSerializer, PropertyImageSerializer, PropertySerializer, ReviewSerializer
from rest_framework.exceptions import PermissionDenied
from core.models import Profile
from .models import Category, Collection, Property, PropertyImage, Review
from .permissions import IsGuestOrReadOnly, IsHostOrReadOnly, IsOwnerOrReadOnly


class PropertyImageViewSet(ModelViewSet):
    serializer_class = PropertyImageSerializer
    # is authenticated (has per) and is host (has obj per) | readonly
    permission_classes = [IsHostOrReadOnly]

    def get_serializer_context(self):
        return {'property_id': self.kwargs['property_pk']}

    def get_queryset(self):
        return PropertyImage.objects.filter(property_id=self.kwargs['property_pk'])


class PropertyViewSet(ModelViewSet):
    queryset = Property.objects.prefetch_related('images').all()
    serializer_class = PropertySerializer
    permission_classes = [IsHostOrReadOnly]
    filter_backends = [FilterBackend, SearchFilter, OrderingFilter]

    pagination_class = DefaultPagination
    search_fields = ['title', 'description', ]
    ordering_fields = ['price', 'last_update', ]
    # TODO use filterset_class = PropertyFilter instead of filterset_fields
    # https://django-filter.readthedocs.io/en/stable/ref/filterset.html
    filterset_fields = ['category_id']

    def get_serializer_context(self):
        if self.request.user.is_authenticated:
            return {'hosted_user_id': self.request.user.profile.id}
        return super().get_serializer_context()

    # def get_serializer(self, *args, **kwargs):
    #     return PropertySerializer(self.queryset, context={'request': self.request})

    def destroy(self, request, *args, **kwargs):
        property_obj = self.get_object()
        self.check_object_permissions(request, property_obj)
        # property_obj shouldn't be associated with any appointments to delete it
        # if propert.(instance_model).exists():
        #     return Response({'error': 'Property cannot be deleted as it is associated with an appointment'},
        #                     status=status.HTTP_400_BAD_REQUEST)

        # if no associations exist, proceed with deletion
        # return super().destroy(request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
        properties_count=Count('properties')).all()
    serializer_class = CollectionSerializer
    permission_classes = [IsHostOrReadOnly]

    def get_serializer_context(self):
        if self.request.user.is_authenticated:
            return {'hosted_user_id': self.request.user.profile.id}
        return super().get_serializer_context()

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


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    # it include check for is authenticated too
    permission_classes = [IsAuthenticatedOrReadOnly, IsGuestOrReadOnly]

    # FIXME Update this get_serializer_context , we're using this functionality before we make FK to profile
    # its same thing :)
    def get_serializer_context(self):
        context = {'property_id': self.kwargs['property_pk']}
        if self.request.user.is_authenticated:
            context['reviewer_name'] = self.request.user.first_name if self.request.user.first_name else self.request.user.username
            context['user_profile_id'] = self.request.user.profile.id
        return context

    def get_queryset(self):
        return Review.objects.filter(property_id=self.kwargs['property_pk'])


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
        return super().get_permissions()

    def destroy(self, request, *args, **kwargs):
        # in deletion ,category should be not associated with properties otherwise will not delete
        collection = get_object_or_404(Collection.objects.annotate(
            properties_count=Count('properties')), pk=kwargs['pk'])
        if collection.properties.count() > 0:
            return Response({'error': 'Category cannot be deleted because it has more than one property'})
        return super().destroy(request, *args, **kwargs)
