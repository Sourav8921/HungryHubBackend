from ..models import Restaurants, MenuItem
from rest_framework import viewsets
from .serializers import RestaurantsSerializer, MenuItemSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurants.objects.all()
    serializer_class = RestaurantsSerializer


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

