from django.urls import path, include

app_name = 'api_v1'

urlpatterns = [
    # path('', include('rest_framework.urls', namespace='rest_framework')),
    path('auth/', include('api_v1.authapp.urls', namespace='auth')),
]