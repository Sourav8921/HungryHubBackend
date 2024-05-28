from django.urls import path, include
from .views import RestaurantViewSet, MenuItemsByRestaurantAPIView, CreateOrderView, search_menu_items
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'restaurants', RestaurantViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('menu-items/', MenuItemsByRestaurantAPIView.as_view(), name='menu_items_by_restaurant'),
    path('orders/', CreateOrderView.as_view(), name='create-order'),
    path('search/', search_menu_items, name='search_menu_items'),
]
