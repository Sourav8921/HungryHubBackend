from django.urls import path, include
from .views import RestaurantViewSet, MenuItemsByRestaurantAPIView, CreateOrderView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'restaurants', RestaurantViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('menu-items/', MenuItemsByRestaurantAPIView.as_view(), name='menu_items_by_restaurant'),
    path('orders/', CreateOrderView.as_view(), name='create-order'),
]
