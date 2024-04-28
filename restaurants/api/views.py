from ..models import Restaurants
from rest_framework import viewsets
from .serializers import RestaurantsSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurants.objects.all()
    serializer_class = RestaurantsSerializer

