from django.contrib import admin
from django.urls import path, include
from accounts import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/products/')),  # Redirect root URL to /products/
    path('admin/', admin.site.urls),

    # App URLs
    path('cart/', include('cart.urls')),
    path('products/', include('products.urls')),
    path('subscriptions/', include(('subscriptions.urls', 'subscriptions'), namespace='subscriptions')),
    path('accounts/', include('accounts.urls')),
    path('contact/', views.contact, name='contact'),
    path('newsletter/', include(('newsletter.urls', 'newsletter'), namespace='newsletter')),
    path('reviews/', include('reviews.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
