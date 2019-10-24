from django.contrib import admin

from authapp.models import UniteamsUser, UserProfile, Company, UniteamsGroup, UniteamsTeam, OrgStruct

admin.site.register(UniteamsUser)
admin.site.register(UserProfile)
admin.site.register(Company)
admin.site.register(UniteamsTeam)
admin.site.register(UniteamsGroup)
admin.site.register(OrgStruct)
