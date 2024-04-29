from django.urls import path, include
from .views import RestaurantViewSet, MenuItemViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'restaurants', RestaurantViewSet)
router.register(r'menu-items', MenuItemViewSet)

urlpatterns = [
    path('', include(router.urls))
]
