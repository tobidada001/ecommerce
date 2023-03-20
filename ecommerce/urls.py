from django.urls import path
from . import views

app_name = 'ecommerce'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('shop/', views.shop, name = 'shop'),
    path('product-details/<int:pk>/', views.product_details, name = 'product_info'),
    path('cart/', views.cart, name = 'cart'),
    path('add/', views.add_to_cart, name = 'add_to_cart'),
    path('update-cart/', views.update_cart, name = 'update_cart'),
    path('remove-cart/', views.remove_from_cart, name='remove_cart'),
    path('load-color/', views.load_colors, name='load_colors'),
    path('checkout/', views.checkout, name= 'checkout'),
    path('orders/', views.orders, name = 'orders'),
    path('auth-user', views.auth_user, name = 'auth_user'),
    path('register-user', views.register_user, name = 'register_user'),
    path('logout/', views.logoutuser, name = 'logout')
]
