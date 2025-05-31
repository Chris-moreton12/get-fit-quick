from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from subscriptions.models import SubscriptionPlan

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)

    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    subscription = models.ForeignKey(SubscriptionPlan, null=True, blank=True, on_delete=models.CASCADE)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        if self.product:
            return f"{self.product.name} x {self.quantity}"
        elif self.subscription:
            return f"{self.subscription.name} x {self.quantity}"
        else:
            return "Unknown item"

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.address_line1}, {self.city}"
