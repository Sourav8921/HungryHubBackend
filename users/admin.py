from django.contrib import admin
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']


admin.site.register(CustomUser, CustomUserAdmin)

