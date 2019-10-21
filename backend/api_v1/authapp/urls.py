from django.urls import path, include

from rest_framework import routers

from api_v1.authapp.views import (RegistrationAPIView, LoginAPIView, ListUsersAPIView, VerifyAPIView)

router = routers.DefaultRouter()

app_name = 'api_auth'

urlpatterns = [
    path('', include(router.urls)),
    path('users/', ListUsersAPIView.as_view(), name='users'),
    path('registration', RegistrationAPIView.as_view(), name='registration'),
    path('verify', VerifyAPIView.as_view(), name='verify'),
    path('login', LoginAPIView.as_view(), name='login'),

]