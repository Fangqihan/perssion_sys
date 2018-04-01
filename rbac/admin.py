from django.contrib import admin

from .models import UserInfo, Menu, Permissions, Role

admin.site.register(Menu)
admin.site.register(UserInfo)
admin.site.register(Permissions)
admin.site.register(Role)



