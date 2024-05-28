from ..models import Restaurant, MenuItem, Order
from users.models import CustomUser
from rest_framework import viewsets, generics, status, views
from rest_framework.response import Response
from .serializers import RestaurantsSerializer, MenuItemSerializer, OrderSerializer
from django.shortcuts import get_object_or_404


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantsSerializer
    

class MenuItemsByRestaurantAPIView(generics.ListAPIView):
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        restaurant__id = self.request.query_params.get('restaurant_id')
        queryset = MenuItem.objects.filter(restaurant_id=restaurant__id)
        return queryset


class CreateOrderView(views.APIView):
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid(): #Checks if the data adheres to the defined schema (e.g., types, required fields).
            user = get_object_or_404(CustomUser, id=request.data.get('user'))
            restaurant = get_object_or_404(Restaurant, id=request.data.get('restaurant'))
            total_price = request.data.get('total_price')
            order = Order.objects.create(
                user=user,
                restaurant=restaurant,
                total_price=total_price,
                status="Pending"
            )
            for item in request.data['items']:
                menu_item = get_object_or_404(MenuItem, id=item['id'])
                for _ in range(item['count']):
                    order.items.add(menu_item)
            order.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)