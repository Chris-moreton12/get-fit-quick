from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),  # Displays the list of products
    path('products/', views.product_list, name='products'),
]
