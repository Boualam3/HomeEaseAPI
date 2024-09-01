from django.urls import path, include
from rest_framework import routers
from .views import PropertyImageViewSet


router = routers.DefaultRouter()
router.register(r'images', PropertyImageViewSet, basename='property-images')

urlpatterns = [
    path('', include(router.urls)),
]
