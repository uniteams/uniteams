from django.urls import path, include

from rest_framework import routers

from authapp.views import (RegistrationAPIView, LoginAPIView, UserViewSet)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


app_name = 'authapp'

urlpatterns = [
    path('', include(router.urls)),
    path('api/v0/registration/', RegistrationAPIView.as_view(), name='registration'),
    path('api/v0/login/', LoginAPIView.as_view(), name='login'),
    path('api/', include('rest_framework.urls', namespace='rest_framework'))
]