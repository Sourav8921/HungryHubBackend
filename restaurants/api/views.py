import json
from django.middleware.csrf import get_token
from ..models import Restaurant, MenuItem, Order, Category
from users.models import CustomUser
from rest_framework import viewsets, generics, status, views, permissions
from rest_framework.response import Response
from .serializers import RestaurantSerializer, MenuItemSerializer, OrderSerializer, CategorySerializer
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
import stripe
from django.conf import settings
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from geopy.distance import geodesic


@csrf_exempt
def nearby_restaurants(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_location = (data['latitude'], data['longitude'])
        restaurants = []

        for restaurant in Restaurant.objects.all():
            full_image_url = request.build_absolute_uri(restaurant.image.url)
            restaurant_location = (restaurant.latitude, restaurant.longitude)
            distance = geodesic(user_location, restaurant_location).kilometers
            if distance <= 10:
                restaurants.append({
                    'id': restaurant.id,
                    'name': restaurant.name,
                    'delivery_time': restaurant.delivery_time,
                    'cuisine_type': restaurant.cuisine_type,
                    'place': restaurant.place,
                    'image': full_image_url,
                })

        return JsonResponse(restaurants, safe=False)


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    

class MenuItemsByRestaurantAPIView(generics.ListAPIView):
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        restaurant__id = self.request.query_params.get('restaurant_id')
        queryset = MenuItem.objects.filter(restaurant_id=restaurant__id)
        return queryset


def search_menu_items(request):
    query = request.GET.get('q')
    if query:
        menu_items = MenuItem.objects.filter(name__icontains=query)

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

    return JsonResponse({'results': results_list})


def restaurants_by_category(request):
    category_id = request.GET.get('category')
    if category_id:
        menu_items = MenuItem.objects.filter(category_id=category_id)
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


# stripe payment integration
stripe.api_key = settings.STRIPE_SECRET_KEY


def create_payment_intent(request):
    try:
        data = json.loads(request.body)
        amount = data.get('amount')
        if not amount:
            return HttpResponseBadRequest("Amount is required")
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='inr',
        )
        return JsonResponse({'clientSecret': intent['client_secret']})
    except Exception as e:
        return JsonResponse({'error': str(e)})


@ensure_csrf_cookie
def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})


class CategoriesView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

