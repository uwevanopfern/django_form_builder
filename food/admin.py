from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_admin', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'forms')}),
    )

    search_fields =  ('username', 'email')
    ordering = ('username',)
admin.site.register(User, CustomUserAdmin)
