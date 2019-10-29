from django.urls import path, include

from rest_framework import routers

from api_v1.authapp.views import (TokenAPIView, VerifyAPIView, UsersAPIView, UserDetailAPIView, CompaniesAPIView,
                                  CompanyDetailAPIView)

router = routers.DefaultRouter()

app_name = 'authapp'

urlpatterns = [
    path('', include(router.urls)),
    path('users/', UsersAPIView.as_view(), name='users'),
    path('users/<int:pk>', UserDetailAPIView.as_view(), name='user-detail'),
    path('companies/', CompaniesAPIView.as_view(), name='companies'),
    path('companies/<int:pk>', CompanyDetailAPIView.as_view(), name='company-detail'),
    path('verification/', VerifyAPIView.as_view(), name='verify'),
    path('token/', TokenAPIView.as_view(), name='api-token'),

]