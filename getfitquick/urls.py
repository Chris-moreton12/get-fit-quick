from django.contrib import admin
from django.urls import path, include
from accounts import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls')), 
    path('products/', include('products.urls')),  # Link to the products app
    path('subscriptions/', include('subscriptions.urls')),  # Link to the subscriptions app
    path('accounts/', include('accounts.urls')),
    path('contact/', views.contact, name='contact'),
    path('subscriptions/', include('subscriptions.urls', namespace='subscriptions')), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
