import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Cart, CartItem
from products.models import Product

# Initialize Stripe with the secret key
stripe.api_key = settings.STRIPE_SECRET_KEY

# Show cart items
@login_required
def cart(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)
    for item in cart_items:
        item.total_price = item.price * item.quantity
    total = sum(item.total_price for item in cart_items)
    return render(request, 'cart/cart.html', {'cart_items': cart_items, 'total': total})

# Add product to cart (redirect back to previous page)
@login_required
def add_to_cart(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        cart, _ = Cart.objects.get_or_create(user=request.user)

        cart_item = CartItem.objects.filter(cart=cart, product=product).first()

        if cart_item:
            cart_item.quantity += 1
        else:
            cart_item = CartItem(
                cart=cart,
                product=product,
                price=product.price,
                quantity=1
            )
        cart_item.save()

        # Redirect back to referring page or product list if no referrer
        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        else:
            return redirect('products:product_list')

    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

# Stripe Checkout redirect
@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)

    if not cart_items.exists():
        return redirect('cart:cart')

    line_items = []

    for item in cart_items:
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item.product.name,
                },
                'unit_amount': int(item.price * 100),  # Stripe expects amount in cents
            },
            'quantity': item.quantity,
        })

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            customer_email=request.user.email,
            success_url=request.build_absolute_uri('/cart/checkout/success/'),
            cancel_url=request.build_absolute_uri('/cart/'),
        )
        return redirect(checkout_session.url, code=303)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Checkout success
@login_required
def checkout_success(request):
    CartItem.objects.filter(cart__user=request.user).delete()
    return render(request, 'cart/checkout_success.html')

from django.views.decorators.http import require_POST

@require_POST
@login_required
def remove_from_cart(request, item_id):
    try:
        item = CartItem.objects.get(id=item_id, cart__user=request.user)
        item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect('cart:cart')
