from django.contrib import admin
from .models import Restaurant, MenuItem


class RestaurantsAdmin(admin.ModelAdmin):
    list_display = ('name', 'cuisine_type', 'place')


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'price')


admin.site.register(Restaurant, RestaurantsAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
