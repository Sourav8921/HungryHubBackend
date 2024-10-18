import json
from django.middleware.csrf import get_token
from restaurants.models import Restaurant, MenuItem, Order, Category, OrderItem
from users.models import CustomUser
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from restaurants.serializers import RestaurantSerializer, MenuItemSerializer, OrderSerializer, CategorySerializer
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
import stripe
from django.conf import settings
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]
    

class MenuItemsByRestaurantAPIView(generics.ListAPIView):
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]

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


def create_order(order_details):
    items_data = order_details.pop('items')
    user = get_object_or_404(CustomUser, id=order_details['user'])
    restaurant = get_object_or_404(Restaurant, id=order_details['restaurant'])
    order = Order.objects.create(
        user=user,
        restaurant=restaurant,
        total_price=order_details['total_price'],
        status=order_details["status"]
    )
    for item_data in items_data:
        menu_item = MenuItem.objects.get(id=item_data['id'])
        OrderItem.objects.create(order=order, menu_item=menu_item, count=item_data['count'])

    return order


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter orders to return only those belonging to the authenticated user
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):

        payment_method = request.data.get('payment_method')
        order_details = request.data.get('order_details')

        if payment_method == 'stripe':
            # Stripe payment verification
            payment_intent_id = request.data.get('payment_intent_id')
            try:
                payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
                if payment_intent["status"] == 'succeeded':
                    # Payment was successful, create the order
                    order = create_order(order_details)
                    serializer = self.get_serializer(order)
                    return Response(serializer.data)
                else:
                    return Response({'success': False, 'error': 'Payment not completed'}, status=400)
            except Exception as e:
                return Response({'success': False, 'error': str(e)}, status=500)
        elif payment_method == 'cod':
            # Create the order directly for Cash on Delivery
            order = create_order(order_details)
            serializer = self.get_serializer(order)
            return Response(serializer.data)
        else:
            return Response({'success': False, 'error': 'Invalid payment method'}, status=400)


# stripe payment integration
stripe.api_key = settings.STRIPE_SECRET_KEY


@csrf_exempt
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
        return JsonResponse({
            'clientSecret': intent['client_secret'],
            'paymentIntentId': intent['id']
        })
    except Exception as e:
        return JsonResponse({'error': str(e)})


@ensure_csrf_cookie
def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})


class CategoriesView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

