from django.urls import path, include
# from rest_framework.routers import DefaultRouter
from .views import TempUserActivationView

# router = DefaultRouter()
# router.register('profile', ProfileViewSet)

urlpatterns = [
    # path('',  include(router.urls)),
    path(r'activate/<str:uid>/<str:token>/',
         TempUserActivationView.as_view()),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
