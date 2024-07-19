from django.contrib import admin
from .models import Restaurant, MenuItem, Order, Category


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'cuisine_type', 'place')


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'price')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant', 'total_price', 'status', 'created_at')


admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Category)


