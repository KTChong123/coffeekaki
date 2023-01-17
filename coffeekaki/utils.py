import json
from .models import *
from django.contrib.auth.models import User


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print('Cart: ', cart)
    items = []
    order = {
        'get_cart_total': 0,
        'get_cart_items': 0
    }
    for i in cart:
        try:
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'image': product.image,
                },
                'quantity': cart[i]['quantity'],
                'get_total': total,
            }
            items.append(item)
        except:
            pass
    return {
        'items': items,
        'order': order,
    }


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        cookieData = cookieCart(request)
        customer = {}
        order = cookieData['order']
        items = cookieData['items']
    return {
        'customer': customer,
        'items': items,
        'order': order,
    }


def guestOrder(request, data):
    print('user is not logged in..')

    print('COOKIES: ', request.COOKIES)

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = User.objects.get_or_create(username="guest")

    order = Order.objects.create(customer=customer, complete=False)

    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )
    return customer, order
