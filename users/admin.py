from django.contrib import admin
from .models import CustomUser, DeliveryAddress


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(DeliveryAddress)
