# cart/urls.py

from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart, name='cart'),  # Cart view
    path('checkout/', views.checkout, name='checkout'),  # Checkout view
    path('checkout/success/', views.checkout_success, name='checkout_success'),  # Checkout success view
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]
