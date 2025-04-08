from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),  # Use Django's built-in login view
    path('signup/', views.signup, name='signup'),  # Custom signup view
]
