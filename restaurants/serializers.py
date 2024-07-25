from rest_framework import serializers
from restaurants.models import Restaurant, MenuItem, Order, Category, OrderItem


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'image']


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price', 'restaurant', 'category', 'image']


class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer()

    class Meta:
        model = OrderItem
        fields = ['menu_item', 'count']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    restaurant = RestaurantSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'restaurant', 'items', 'total_price', 'status', 'created_at']
