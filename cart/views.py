import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Cart, CartItem
from products.models import Product

# Initialize Stripe with the secret key
stripe.api_key = settings.STRIPE_SECRET_KEY

# Cart view to show cart items
@login_required
def cart(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)

    # Calculate the total price for each item in the cart
    for item in cart_items:
        item.total_price = item.price * item.quantity

    total = sum(item.total_price for item in cart_items)

    return render(request, 'cart/cart.html', {'cart_items': cart_items, 'total': total})

# Add a product to the cart
@login_required
def add_to_cart(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        cart, _ = Cart.objects.get_or_create(user=request.user)

        # Try to find existing cart item by product (using the foreign key)
        cart_item = CartItem.objects.filter(cart=cart, product=product).first()

        if cart_item:
            cart_item.quantity += 1
        else:
            cart_item = CartItem(
                cart=cart,
                product=product,  # Using the product foreign key
                price=product.price,
                quantity=1
            )
        cart_item.save()

        return redirect('cart:cart')

    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

# Checkout view to handle checkout process
@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)
    total = sum(item.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(total * 100),
                currency='usd',
                metadata={'integration_check': 'accept_a_payment'},
            )
            return render(request, 'cart/checkout.html', {
                'cart_items': cart_items,
                'total': total,
                'client_secret': intent.client_secret,
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'cart/checkout.html', {'cart_items': cart_items, 'total': total})

# Checkout success page
@login_required
def checkout_success(request):
    CartItem.objects.filter(cart__user=request.user).delete()
    return render(request, 'cart/checkout_success.html')
