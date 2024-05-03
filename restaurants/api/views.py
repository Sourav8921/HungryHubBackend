from ..models import Restaurants, MenuItem
from rest_framework import viewsets, generics
from .serializers import RestaurantsSerializer, MenuItemSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurants.objects.all()
    serializer_class = RestaurantsSerializer


class MenuItemsByRestaurantAPIView(generics.ListAPIView):
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        restaurant__id = self.request.query_params.get('restaurant_id')
        queryset = MenuItem.objects.filter(restaurant_id=restaurant__id)
        return queryset
