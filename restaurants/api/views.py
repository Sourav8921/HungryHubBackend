from ..models import Restaurant, MenuItem, Order
from users.models import CustomUser
from rest_framework import viewsets, generics, status, views, permissions
from rest_framework.response import Response
from .serializers import RestaurantsSerializer, MenuItemSerializer, OrderSerializer
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantsSerializer
    

class MenuItemsByRestaurantAPIView(generics.ListAPIView):
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        restaurant__id = self.request.query_params.get('restaurant_id')
        queryset = MenuItem.objects.filter(restaurant_id=restaurant__id)
        return queryset


# class CreateOrderView(views.APIView):
#     def post(self, request):
#         serializer = OrderSerializer(data=request.data)
#         if serializer.is_valid():  # Checks if the data adheres to the defined schema (e.g., types, required fields).
#             user = get_object_or_404(CustomUser, id=request.data.get('user'))
#             restaurant = get_object_or_404(Restaurant, id=request.data.get('restaurant'))
#             total_price = request.data.get('total_price')
#             order = Order.objects.create(
#                 user=user,
#                 restaurant=restaurant,
#                 total_price=total_price,
#                 status="Pending"
#             )
#             for item in request.data['items']:
#                 menu_item = get_object_or_404(MenuItem, id=item['id'])
#                 for _ in range(item['count']):
#                     order.items.add(menu_item)
#             order.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def search_menu_items(request):
    # request.GET is a dictionary-like object that contains all the parameters passed in the URL query string
    query = request.GET.get('q')
    if query:
        # Filter menu items containing the search query
        menu_items = MenuItem.objects.filter(name__icontains=query)

        # Create a list of restaurants associated with the filtered menu items
        restaurants = []
        for item in menu_items:
            if item.restaurant not in restaurants:
                restaurants.append(item.restaurant)

        results_list = []
        for restaurant in restaurants:
            full_image_url = request.build_absolute_uri(restaurant.image.url)
            results_list.append({
                'id': restaurant.id,
                'name': restaurant.name,
                'delivery_time': restaurant.delivery_time,
                'cuisine_type': restaurant.cuisine_type,
                'place': restaurant.place,
                'image': full_image_url
            })
    else:
        results_list = []

    # Return the list of restaurant objects as JSON response
    return JsonResponse({'results': results_list})


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter orders to return only those belonging to the authenticated user
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():  # Checks if the data adheres to the defined schema (e.g., types, required fields).
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