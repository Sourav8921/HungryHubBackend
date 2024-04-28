from rest_framework import serializers
from restaurants.models import Restaurants


class RestaurantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurants
        fields = ['name', 'delivery_time', 'cuisine_type', 'place', 'image_url']
