from django.urls import path, include

from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()

# router.register('booking', views.PropertyViewSet, basename='booking')

urlpatterns = router.urls