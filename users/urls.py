from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import register_user, ProfileView, DeliveryAddressViewSet

router = DefaultRouter()
router.register(r'delivery-addresses', DeliveryAddressViewSet, basename='delivery-address')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', register_user, name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
]

