import csv
from django.shortcuts import render, redirect
from django.contrib import messages
from . import models
from django.contrib.auth.models import User
from django.http import HttpResponse
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


def dashboard(request):
    return render(request,'main.html')


def index(request):
    cat=list(models.Category.objects.all())
    random.shuffle(cat)
    unique_category=[]
    original=cat[:6]
    for item in original:
        if item not in unique_category:
            unique_category.append(item)

    category=unique_category

    unique_product=[]
    prods=list(models.Product.objects.all())
    random.shuffle(prods)
    og=prods[:8]
    for item in og:
        if item not in unique_product:
            unique_product.append(item)

    product=unique_product

    today_special=models.Product.objects.get(today_special=True)
    return render(request,'index.html',{'category':category,'today_special':today_special,'product':product})


def products(request,**kwargs):
    name=kwargs.get('name')
    items=models.Product.objects.filter(category__name__contains=name)
    return render(request,'product-list.html',{'name':name,'items':items})