from django.urls import path, include

from rest_framework import routers

from api_v1.authapp.views import (RegistrationAPIView, LoginAPIView, ListUsersAPIView)

router = routers.DefaultRouter()
# router.register(r'users', ListUsersAPIView)


app_name = 'authapp'

urlpatterns = [
    path('', include(router.urls)),
    path('users', ListUsersAPIView.as_view(), name='users'),
    path('registration', RegistrationAPIView.as_view(), name='registration'),
    path('login', LoginAPIView.as_view(), name='login'),

]