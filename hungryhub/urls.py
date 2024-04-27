from django.contrib import admin
from django.urls import path
from restaurants.views import RestaurantListAPIView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('restaurants/', RestaurantListAPIView.as_view(), name='restaurant-list')
]
