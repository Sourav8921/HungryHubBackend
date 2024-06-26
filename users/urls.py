from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import register_user, user_login, user_logout, ProfileView, DeliveryAddressViewSet

router = DefaultRouter()
router.register(r'delivery-addresses', DeliveryAddressViewSet, basename='delivery-address')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', register_user, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
]

