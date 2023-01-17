from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
import json
import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .forms import ProductForm
from .utils import cookieCart, cartData, guestOrder
from django.urls import reverse
from django.conf import settings  # new
from django.http.response import JsonResponse  # new
from django.views.decorators.csrf import csrf_exempt  # new
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.

products = [
    {'id': 1, 'name': 'All products'},
    {'id': 2, 'name': 'Foods'},
    {'id': 3, 'name': 'Drinks'},
    {'id': 4, 'name': 'Snacks'},
]

categories = Product.objects.order_by().values('category').distinct()


def stripe_checkouts_view(request):
    return render(request, "stripe-checkout.html")


@csrf_exempt
def create_payment_intent_view(request):
    data = {}
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

    total = order.get_cart_total * 100
    total = int(total)
    print("Total card charge: ", total)

    try:
        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            amount=total,
            currency='myr',
            payment_method_types=['card', 'fpx', 'grabpay'],
        )
        print('clientSecret: ', intent['client_secret'])
        return JsonResponse({
            'clientSecret': intent['client_secret']
        })
    except Exception as e:
        return JsonResponse(error=str(e)), 403


def payment_status_view(request, pk):
    table_number = request.COOKIES['myTable']
    payment_status = request.GET.get('redirect_status')
    transaction_id = datetime.datetime.now().timestamp()
    print("transaction amount: ", pk)
    print("Payment status: ", payment_status)

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

    order.transaction_id = transaction_id

    if payment_status == "succeeded":
        order.complete = True
        order.save()
        payment_status_msg = "Payment is successful."
    else:
        payment_status_msg = "Payment is unsuccessful. Please try again."

    data = cartData(request)
    customer = data['customer']
    order = data['order']
    items = data['items']

    context = {
        'categories': categories,
        'items': items,
        'order': order,
        'table_number': table_number,
        'payment_status': payment_status,
        'payment_status_msg': payment_status_msg
    }

    return render(request, 'payment-status.html', context)


def stripe_card_payment_view(request):
    data = {}
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

    total = order.get_cart_total * 100
    total = int(total)
    print("Total card charge: ", total)

    try:
        intent = stripe.PaymentIntent.create(
            amount=total,
            currency="myr",
            payment_method_types=["card"]
        )
        print('clientSecret: ', intent['client_secret'])
        return JsonResponse({
            'clientSecret': intent['client_secret']
        })
    except Exception as e:
        return JsonResponse(error=str(e)), 403


def stripe_checkout_view(request):
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card', 'fpx', 'grabpay'],
        line_items=[
            {
                # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                'price': 'price_1MPNPwKgVq5fGvtgkI83LmzI',
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url='http://127.0.0.1:8000' + '/success',
        cancel_url='http://127.0.0.1:8000' + '/cancel',
    )
    return redirect(checkout_session.url, code=303)


def loginPage_view(request):
    table_number = request.COOKIES['myTable']
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exist')

    data = cartData(request)
    customer = data['customer']
    order = data['order']
    items = data['items']

    if request.user.is_authenticated:
        itemsOrder = OrderItem.objects.filter(
            order__customer=customer, order__complete=True, complete=False).order_by('-order__transaction_id')
        itemsHistory = OrderItem.objects.filter(
            order__customer=customer, order__complete=True, complete=True).order_by('-order__transaction_id')
    else:
        itemsOrder = []
        itemsHistory = []

    context = {
        'categories': categories,
        'page': page,
        'items': items,
        'order': order,
        'table_number': table_number,
        'itemsOrder': itemsOrder,
        'itemsHistory': itemsHistory,
    }
    return render(request, 'login_register.html', context)


def logoutUser_view(request):
    logout(request)
    return redirect('home')


def registerUser_view(request):
    table_number = request.COOKIES['myTable']
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')

    data = cartData(request)
    customer = data['customer']
    order = data['order']
    items = data['items']

    context = {
        'categories': categories,
        'form': form,
        'items': items,
        'order': order,
        'table_number': table_number
    }
    return render(request, 'login_register.html', context)


def home_view(request):
    table_number = request.COOKIES['myTable']
    print("table_number: " + table_number)

    best_sellers = Product.objects.all().order_by('-number_of_sales')[:10]

    data = cartData(request)
    customer = data['customer']
    order = data['order']
    items = data['items']

    context = {
        'categories': categories,
        'best_sellers': best_sellers,
        'items': items,
        'order': order,
        'table_number': table_number
    }
    return render(request, "index.html", context)


def products_view(request, pk):
    table_number = request.COOKIES['myTable']
    if pk == "":
        products = Product.objects.all()
        product_category = "All products"
    elif pk == "All":
        products = Product.objects.all()
        product_category = "All products"
    else:
        products = Product.objects.filter(category=pk)
        product_category = pk

    data = cartData(request)
    customer = data['customer']
    order = data['order']
    items = data['items']

    context = {
        'categories': categories,
        'products': products,
        'product_category': product_category,
        'items': items,
        'order': order,
        'table_number': table_number
    }
    return render(request, "products.html", context)


def search_view(request):
    table_number = request.COOKIES['myTable']
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    products = Product.objects.filter(
        Q(name__icontains=q) |
        Q(description__icontains=q) |
        Q(category__icontains=q) |
        Q(type__icontains=q)
    )

    products_count = products.count()

    product_category = "Search: " + q + \
        " (" + str(products_count) + " results found)"

    if not products:
        product_category = "Search: " + q + " (no results found)"

    data = cartData(request)
    customer = data['customer']
    order = data['order']
    items = data['items']

    context = {
        'categories': categories,
        'products': products,
        'product_category': product_category,
        'items': items,
        'order': order,
        'table_number': table_number
    }
    return render(request, "products.html", context)


def updateItem_view(request):
    table_number = request.COOKIES['myTable']
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product, table_number=table_number)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    elif action == 'item_order_complete':
        orderItem.complete = True
    elif action == 'item_order_reactivate':
        orderItem.complete = False

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def cart_view(request):
    table_number = request.COOKIES['myTable']
    data = cartData(request)
    customer = data['customer']
    order = data['order']
    items = data['items']

    context = {
        'categories': categories,
        'items': items,
        'order': order,
        'table_number': table_number
    }
    return render(request, "cart.html", context)


def checkout_view(request):
    table_number = request.COOKIES['myTable']
    data = cartData(request)
    customer = data['customer']
    order = data['order']
    items = data['items']

    if request.user.is_authenticated:
        email = customer.email
        print('email: ', email)
    else:
        email = ""

    context = {
        'categories': categories,
        'items': items,
        'order': order,
        'email': email,
        'table_number': table_number
    }
    return render(request, "checkout.html", context)


def processOrder_view(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    totalcheck = float(order.get_cart_total)
    order.transaction_id = transaction_id

    if total == totalcheck:
        order.complete = True
    order.save()
    print('total:', total, 'totalcheck:', totalcheck)

    return JsonResponse('Payment submitted..', safe=False)


def updateOrderItem_view(request):
    data = json.loads(request.body)
    orderItemId = data['orderItemId']
    action = data['action']
    print('Action:', action)
    print('orderItemId', orderItemId)

    state = State.objects.filter(name="showorderhistory")

    if not state:
        state, created = State.objects.get_or_create(
            name="showorderhistory", state=False)
        state.save()

    if action == 'order_item_complete':
        orderItem = OrderItem.objects.get(id=orderItemId)
        orderItem.complete = True
        orderItem.save()
        orderItem.product.number_of_sales = (
            orderItem.product.number_of_sales + 1)
        orderItem.product.save()
        print(orderItem.product.number_of_sales)
    elif action == 'order_item_reactivate':
        orderItem = OrderItem.objects.get(id=orderItemId)
        orderItem.complete = False
        orderItem.save()
        if orderItem.product.number_of_sales >= 0:
            orderItem.product.number_of_sales = (
                orderItem.product.number_of_sales - 1)
            orderItem.product.save()
            print(orderItem.product.number_of_sales)
    elif action == 'toggle_order_history':
        state = State.objects.get(name="showorderhistory")
        if state.state == True:
            state.state = False
        else:
            state.state = True
        state.save()

    return JsonResponse('Item status updated', safe=False)


@ login_required(login_url='login')
def order_view(request, pk):
    show_order_history = State.objects.get(name="showorderhistory")
    if pk == "":
        product_category = "All"
        items = OrderItem.objects.filter(
            order__complete=True, complete=False).order_by('order__transaction_id')
        itemsHistory = OrderItem.objects.filter(
            order__complete=True, complete=True).order_by('-order__transaction_id')
    elif pk == "All":
        product_category = "All"
        items = OrderItem.objects.filter(
            order__complete=True, complete=False).order_by('order__transaction_id')
        itemsHistory = OrderItem.objects.filter(
            order__complete=True, complete=True).order_by('-order__transaction_id')
    else:
        product_category = pk
        items = OrderItem.objects.filter(
            product__category=pk, order__complete=True, complete=False).order_by('order__transaction_id')
        itemsHistory = OrderItem.objects.filter(
            product__category=pk, order__complete=True, complete=True).order_by('-order__transaction_id')

    context = {
        'categories': categories,
        'product_category': product_category,
        'items': items,
        'itemsHistory': itemsHistory,
        'show_order_history': show_order_history
    }
    if request.user.is_staff:
        return render(request, "order.html", context)
    return HttpResponse('You do not have access to this page')


@ login_required(login_url='login')
def manage_view(request):
    categories = Product.objects.order_by().values('category').distinct()
    products = Product.objects.all().order_by('-number_of_sales')[:10]
    context = {
        'categories': categories,
        'products': products,
    }
    if request.user.is_staff:
        return render(request, "manage.html", context)
    return HttpResponse('You do not have access to this page')


@ login_required(login_url='login')
def manage_menu_view(request):
    categories = Product.objects.order_by().values('category').distinct()
    products = Product.objects.all()
    context = {
        'categories': categories,
        'products': products,
    }
    if request.user.is_staff:
        return render(request, "manage-menu.html", context)
    return HttpResponse('You do not have access to this page')


@ login_required(login_url='login')
def add_product_view(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manage_menu')
    context = {'form': form}
    if request.user.is_staff:
        return render(request, "add-product.html", context)
    return HttpResponse('You do not have access to this page')


@ login_required(login_url='login')
def update_product_view(request, pk):
    products = Product.objects.get(id=pk)
    form = ProductForm(instance=products)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=products)
        if form.is_valid():
            form.save()
            return redirect('manage_menu')
    context = {'form': form}
    if request.user.is_staff:
        return render(request, 'update-product.html', context)
    return HttpResponse('You do not have access to this page')


@ login_required(login_url='login')
def delete_product_view(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('manage_menu')
    if request.user.is_staff:
        return render(request, 'delete-product.html', {'obj': product})
    return HttpResponse('You do not have access to this page')


def success_view(request):
    table_number = request.COOKIES['myTable']
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

    order.transaction_id = transaction_id

    order.complete = True
    order.save()

    data = cartData(request)
    customer = data['customer']
    order = data['order']
    items = data['items']

    context = {
        'categories': categories,
        'items': items,
        'order': order,
        'table_number': table_number
    }

    return render(request, 'success.html', context)


def cancel_view(request):
    table_number = request.COOKIES['myTable']
    data = cartData(request)
    customer = data['customer']
    order = data['order']
    items = data['items']

    context = {
        'categories': categories,
        'items': items,
        'order': order,
        'table_number': table_number
    }
    return render(request, 'cancel.html', context)


def set_table_number_view(request, pk):
    table_number = pk

    data = cartData(request)
    customer = data['customer']
    order = data['order']
    items = data['items']

    context = {
        'categories': categories,
        'items': items,
        'order': order,
        'table_number': table_number
    }
    return render(request, 'set-table-number.html', context)


def table_view(request, pk):
    table_number = pk

    data = cartData(request)
    customer = data['customer']
    order = data['order']
    items = data['items']

    itemsOrder = OrderItem.objects.filter(
        table_number=table_number, order__complete=True, complete=False).order_by('-order__transaction_id')

    context = {
        'categories': categories,
        'items': items,
        'order': order,
        'table_number': table_number,
        'itemsOrder': itemsOrder,
    }
    return render(request, 'table.html', context)
