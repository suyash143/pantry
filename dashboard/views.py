import csv
from django.shortcuts import render, redirect
from django.contrib import messages
from . import models
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
import os
import pytz
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.sessions.models import Session
from django.core import mail
from datetime import date
from django.utils import timezone
from django.db import connection
import datetime
import random
import json

from .models import Product, Order, OrderItem
from .utils import cookieCart, cartData, guestOrder
from django.db import transaction


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            if request.user.is_staff is True:
                return redirect('/dashboard')
            else:
                return redirect('/index')
        else:
            messages.info(request, "invalid Credentials")
            return redirect('login')
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('login')


def dashboard(request):
    if request.user.is_staff:
        return render(request, 'dashboard.html')
    else:
        return render(request, '403.html')


def active_orders(request):
    if request.user.is_staff:
        orders = models.Order.objects.filter(complete=True, accepted=False, cancelled=False)
        accepted = models.Order.objects.filter(accepted=True, delivered=False)
        if request.method == "POST" and request.POST.get('accept'):
            deliver_time = request.POST.get('delivery_time', None)
            id = request.POST.get('id', None)
            obj = models.Order.objects.get(pk=id)
            obj.expected_delivery_time = deliver_time
            obj.save()

            return redirect(f'update_order/accept/{id}')

        elif request.method == "POST" and request.POST.get('cancel'):
            deliver_time = request.POST.get('delivery_time', None)
            id = request.POST.get('id', None)
            obj = models.Order.objects.get(pk=id)
            obj.expected_delivery_time = deliver_time
            obj.save()

            return redirect(f'update_order/cancel/{id}')

        print(request.POST)

        return render(request, 'active_orders.html', {'orders': orders, 'accepted': accepted})
    else:
        return render(request, '403.html')


def previous(request):
    if request.user.is_staff:
        orders = models.Order.objects.filter(complete=True, accepted=False, cancelled=False)
        accepted = models.Order.objects.filter(accepted=True, delivered=False)
        return render(request, 'active_orders.html', {'orders': orders, 'accepted': accepted})
    else:
        return render(request, '403.html')


def update_order(request, **kwargs):
    if request.user.is_staff:
        print(kwargs)

        pk = kwargs.get('pk')
        action = kwargs.get('action')
        order = models.Order.objects.get(pk=pk)
        print(order.price)
        if action == 'accept':
            order.accepted = True
            order.response_time = datetime.datetime.now()
            print(order.customer.coin_spent)
            order.status = 'Accepted'
        elif action == 'cancel':
            order.cancelled = True
            order.status = 'Cancelled'
            order.response_time = datetime.datetime.now()
        elif action == 'delivered':
            order.delivered = True
            order.status = 'Delivered'
            order.delivery_time = datetime.datetime.now()
            order.customer.coin_spent = order.customer.coin_spent + order.price
            order.customer.save()
        else:
            pass
        order.save()
        return redirect('active_orders')
    else:
        return render(request, '403.html')


def index(request):
    data = cartData(request)
    cartItems = data['cartItems']
    print(data)

    cat = list(models.Category.objects.all())
    random.shuffle(cat)
    unique_category = []
    original = cat[:6]
    for item in original:
        if item not in unique_category:
            unique_category.append(item)

    category = unique_category

    unique_product = []
    prods = list(models.Product.objects.all())
    random.shuffle(prods)
    og = prods[:8]
    for item in og:
        if item not in unique_product:
            unique_product.append(item)

    products = unique_product

    if request.user.is_authenticated:
        active_order = models.Order.objects.filter(customer=request.user.customer, complete=True, delivered=False)
    else:
        active_order = None
    today_special = models.Product.objects.get(today_special=True)
    return render(request, 'index.html', {'category': category, 'today_special': today_special, 'products': products,
                                          'cartItems': cartItems, 'active_order': active_order})


def products(request, **kwargs):
    data = cartData(request)
    cartItems = data['cartItems']
    name = kwargs.get('name')
    items = models.Product.objects.filter(category__name__contains=name)
    return render(request, 'product-list.html', {'name': name, 'items': items, 'cartItems': cartItems})


def cart(request):
    if request.user.is_authenticated:
        data = cartData(request)
        cartItems = data['cartItems']
        order = data['order']
        items = data['items']
        return render(request, 'cart.html', {'order': order, 'items': items, 'cartItems': cartItems})
    else:
        return redirect('login')


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


@transaction.atomic
def checkout(request):
    if request.user.is_authenticated:
        data = cartData(request)
        cartItems = data['cartItems']
        order = data['order']
        items = data['items']

        total = order.get_cart_total
        print(total)

        print(data)
        if request.method == 'POST':
            if request.user.is_authenticated:
                customer = request.user.customer
                order, created = Order.objects.get_or_create(customer=customer, complete=False)
            print(order)
            order.transaction_id = datetime.datetime.now().timestamp()
            order.complete = True
            order.date_ordered = datetime.datetime.now()
            order.comment = request.POST.get('comment', None)
            order.status = 'Active'
            order.date_ordered = datetime.datetime.now()
            order.seat = request.POST.get('seat', None)

            order.price = total
            order.save()

            return redirect('index')
        return render(request, 'checkout.html', {'order': order, 'items': items, 'cartItems': cartItems})
    else:
        return redirect('login')


def orders(request):
    accepted_order = models.Order.objects.filter(customer=request.user.customer, complete=True, delivered=False,
                                                 accepted=True)
    cancelled_order = models.Order.objects.filter(customer=request.user.customer, complete=True, delivered=False,
                                                  cancelled=True)
    all_orders = models.Order.objects.filter(customer=request.user.customer, complete=True, delivered=True)
    return render(request, "orders.html", {'accepted_order': accepted_order,'cancelled_order':cancelled_order,
                                           'all_orders':all_orders})
