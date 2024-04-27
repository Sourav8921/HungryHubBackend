from django.shortcuts import render
from .models import Restaurants
from rest_framework import generics

from .serializers import RestaurantsSerializer


class RestaurantListAPIView(generics.ListAPIView):
    queryset = Restaurants.objects.all()
    serializer_class = RestaurantsSerializer

