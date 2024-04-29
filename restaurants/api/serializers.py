from rest_framework import serializers
from ..models import Restaurants, MenuItem


class RestaurantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurants
        fields = ['name', 'delivery_time', 'cuisine_type', 'place', 'image_url']


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'

