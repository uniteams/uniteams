from django.urls import path, include

from rest_framework import routers

from api_v1.authapp.views import (RegistrationAPIView, LoginAPIView, UserViewSet)

# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)

app_name = 'authapp'

urlpatterns = [
    # path('', include('rest_framework.urls', namespace='rest_framework')),
    path('registration/', RegistrationAPIView.as_view(), name='registration'),
    path('login/', LoginAPIView.as_view(), name='login'),

]