from django.contrib import admin
from .models import Restaurants, MenuItem


class RestaurantsAdmin(admin.ModelAdmin):
    list_display = ('name', 'cuisine_type', 'place')


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'price')


admin.site.register(Restaurants, RestaurantsAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
