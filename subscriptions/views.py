from django.shortcuts import render
from .models import SubscriptionPlan

def subscription_list(request):
    plans = SubscriptionPlan.objects.all()
    return render(request, 'subscriptions/subscription_list.html', {'plans': plans})
