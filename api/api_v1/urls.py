from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view
from rest_framework.schemas import get_schema_view

from api_v1.views import SwaggerView

app_name = 'api_v1'

urlpatterns = [

    # path('', include('rest_framework.urls', namespace='rest_framework')),
    path('swagger-ui/', SwaggerView.as_view(), name='swagger-ui'),
    path('openapi', get_schema_view(
        title="Uniteams",
        description="API for all things …"
    ), name='openapi-schema'),
    path('auth/', include('api_v1.authapp.urls', namespace='auth')),
]
