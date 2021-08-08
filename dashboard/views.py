import csv
from django.shortcuts import render, redirect
from django.contrib import messages
from . import models
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
import os
import pytz
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


def dashboard(request):
    return render(request, 'main.html')


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

    today_special = models.Product.objects.get(today_special=True)
    return render(request, 'index.html', {'category': category, 'today_special': today_special, 'products': products,
                                          'cartItems': cartItems})


def products(request, **kwargs):
    data = cartData(request)
    cartItems = data['cartItems']
    name = kwargs.get('name')
    items = models.Product.objects.filter(category__name__contains=name)
    return render(request, 'product-list.html', {'name': name, 'items': items,'cartItems': cartItems})


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
