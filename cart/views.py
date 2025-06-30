import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import Cart, CartItem, ShippingAddress
from .forms import ShippingAddressForm
from products.models import Product
from subscriptions.models import SubscriptionPlan

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    for item in cart_items:
        item.total_price = item.price * item.quantity

    total = sum(item.total_price for item in cart_items)

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            request.session['shipping_address_id'] = address.id
            return redirect('cart:checkout')
    else:
        form = ShippingAddressForm()

    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'total': total,
        'form': form
    })

@login_required
def add_product_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    cart_item = CartItem.objects.filter(cart=cart, product=product).first()

    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        CartItem.objects.create(
            cart=cart,
            product=product,
            price=product.price,
            quantity=1
        )

    referer = request.META.get('HTTP_REFERER')
    return redirect(referer or 'products:product_list')

@login_required
def add_subscription_to_cart(request, subscription_id):
    subscription = get_object_or_404(SubscriptionPlan, id=subscription_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    existing_subscription = CartItem.objects.filter(cart=cart, subscription__isnull=False).first()

    if existing_subscription:
        messages.error(request, 'You can only have one subscription in your cart.')
        return redirect('subscriptions:subscription_list')

    CartItem.objects.create(
        cart=cart,
        subscription=subscription,
        price=subscription.price,
        quantity=1
    )

    referer = request.META.get('HTTP_REFERER')
    return redirect(referer or 'subscriptions:subscription_list')

@login_required
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        return redirect('cart:cart')

    address_id = request.session.get('shipping_address_id')
    if not address_id:
        return redirect('cart:cart')

    line_items = []
    for item in cart_items:
        item_name = item.product.name if item.product else (item.subscription.name if item.subscription else 'Unknown')
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item_name,
                },
                'unit_amount': int(item.price * 100),
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
        error_message = str(e)
        return render(request, 'cart/checkout_error.html', {'error_message': error_message})

@login_required
def checkout_success(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    context = {
        'user': request.user,
        'cart_items': cart_items,
        'total': sum(item.price * item.quantity for item in cart_items),
    }

    html_message = render_to_string('cart/order_confirmation_email.html', context)
    plain_message = strip_tags(html_message)

    send_mail(
        subject="Thank you for your purchase at GetFitQuick!",
        message=plain_message,
        from_email=None,
        recipient_list=[request.user.email],
        html_message=html_message,
    )

    CartItem.objects.filter(cart=cart).delete()
    request.session.pop('shipping_address_id', None)

    return render(request, 'cart/checkout_success.html')

@require_POST
@login_required
def remove_from_cart(request, item_id):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    try:
        item = CartItem.objects.get(id=item_id, cart=cart)
        item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect('cart:cart')
