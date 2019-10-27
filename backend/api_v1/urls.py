from django.urls import path, include

from api_v1.views import SwaggerView

app_name = 'api_v1'

urlpatterns = [

    path('', SwaggerView.as_view(), name='swagger-ui'),
    path('', include('api_v1.authapp.urls', namespace='auth')),
]
