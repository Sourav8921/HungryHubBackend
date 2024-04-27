from django.contrib import admin
from .models import Restaurants


class RestaurantsAdmin(admin.ModelAdmin):
    list_display = ('name', 'cuisine_type', 'place')


admin.site.register(Restaurants, RestaurantsAdmin)
