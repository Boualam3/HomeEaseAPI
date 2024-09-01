from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend as FilterBackend
from .serializers import CollectionSerializer, PropertyImageSerializer, PropertySerializer
from .models import Collection, Property, PropertyImage
from .permissions import IsHostReadOnly


class PropertyImageViewSet(ModelViewSet):
    serializer_class = PropertyImageSerializer

    def get_serializer_context(self):
        return {'property_id': self.kwargs['property_pk']}

    def get_queryset(self):
        return PropertyImage.objects.filter(property_id=self.kwargs['property_pk'])


class PropertyViewSet(ModelViewSet):
    queryset = Property.objects.prefetch_related('images').all()
    serializer_class = PropertySerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [FilterBackend, SearchFilter, OrderingFilter]

    # pagination_class = DefaultPagination

    search_fields = ['title', 'description', ]
    ordering_fields = ['price', 'last_update']
    # TODO use filterset_class = PropertyFilter instead of filterset_fields
    # https://django-filter.readthedocs.io/en/stable/ref/filterset.html
    filterset_fields = ['category_id']

    # def get_queryset(self):
    #     #Ps : simple filtering before going to use django-filter
    #     queryset = Property.objects.all()
    #     category_id = self.request.query_params.get('category_id')
    #     if category_id is not None:
    #         queryset = queryset.filter(category_id=category_id)
    #     return queryset

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        pass
        # before delete the object check if it is associated with appointment or order , booking
        # user cannot deleted till make it not available if so ,whether is assoiceted or nor will delete


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
        properties_count=Count('properties')).all()
    serializer_class = CollectionSerializer
    # TODO will add custom premission allow only Hoster to post/delete/update collection , likewise guest will be allowed to  view collections
    permission_classes = [IsHostReadOnly]

    def destroy(self, request, *args, **kwargs):
        # in deletion ,collection should be not associated with properties othewise will not delete
        collection = get_object_or_404(Collection.objects.annotate(
            properties_count=Count('properties')), pk=kwargs['pk'])
        if collection.properties.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it has more than one property'})
        return super().destroy(request, *args, **kwargs)
