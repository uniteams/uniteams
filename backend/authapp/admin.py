from django.contrib import admin

from authapp.models import UniteamsUser, UserProfile

admin.site.register(UniteamsUser)
admin.site.register(UserProfile)
