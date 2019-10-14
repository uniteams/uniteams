from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from main.views import show_landing

app_name = 'main'

urlpatterns = [
    path('', show_landing, name='main')
]
