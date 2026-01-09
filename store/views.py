from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import FoodItem, Order, OrderItem

# Create your views here.

def menu(request):
    foods = FoodItem.objects.filter(is_available=True)
    return render(request, 'store/menu.html', {'foods': foods})


@login_required
def add_to_cart(request, food_id):
    food = get_object_or_404(FoodItem, id=food_id)

    order, created = Order.objects.get_or_create(
        user=request.user,
        is_paid=False
    )

    order_item, created = OrderItem.objects.get_or_create(
        order=order,
        food_item=food
    )

    if not created:
        order_item.quantity += 1
    order_item.save()

    return redirect('cart')


@login_required
def cart_view(request):
    order = Order.objects.filter(user=request.user, is_paid=False).first()

    if order:
        cart_items = OrderItem.objects.filter(order=order)
    else:
        cart_items = []

    total_price = sum(item.food_item.price * item.quantity for item in cart_items)

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

@login_required
def place_order(request):
    order = Order.objects.filter(
        user=request.user,
        is_paid=False
    ).first()

    if order:
        order.is_paid = True
        order.save()

    return redirect('menu')