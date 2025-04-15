from django.contrib import admin
from django.urls import path, include
from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('products.urls')),  # Link to the products app
    path('subscriptions/', include('subscriptions.urls')),  # Link to the subscriptions app
    path('accounts/', include('accounts.urls')),
    path('contact/', views.contact, name='contact'),
]
