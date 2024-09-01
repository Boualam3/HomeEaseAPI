from django.urls import path, include
# from rest_framework import routers
from rest_framework_nested import routers
from . import views


router = routers.DefaultRouter()
router.register('properties', views.PropertyViewSet, basename='products')

# parent router that can register child routers which made nested endpoints
properties_router = routers.NestedDefaultRouter(
    router, 'properties', lookup='property'
)

# nested endpoint in properties
properties_router.register(
    'images', views.PropertyImageViewSet,  basename='property-images'
)

# router.register(r'images', views.PropertyImageViewSet, basename='property-images')

urlpatterns = router.urls + properties_router.urls
