from django.db.models import Sum
from .models import CartItem

def cart_item_count(request):
    if request.user.is_authenticated:
        count = CartItem.objects.filter(cart__user=request.user).aggregate(total=Sum('quantity'))['total']
        return {'cart_item_count': count or 0}
    return {'cart_item_count': 0}
