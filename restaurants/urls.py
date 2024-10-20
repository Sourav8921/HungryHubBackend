from django.urls import path, include
from restaurants import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'restaurants', views.RestaurantViewSet)
router.register(r'orders', views.OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('menu-items/', views.MenuItemsByRestaurantAPIView.as_view(), name='menu_items_by_restaurant'),
    path('search/', views.search_menu_items, name='search_menu_items'),
    path('create-payment-intent/', views.create_payment_intent, name='create-payment-intent'),
    path('get-csrf-token/', views.get_csrf_token, name='get-csrf-token'),
    path('categories/', views.CategoriesView.as_view(), name='categories'),
    path('restaurants-category/', views.restaurants_by_category, name='restaurants-category'),
]
