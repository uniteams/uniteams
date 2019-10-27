from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from uniteams import settings

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('main.urls'), name='main'),
                  path('api/v1/', include('api_v1.urls', namespace='api-v1')),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
