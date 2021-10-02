from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    is_money_manager = models.BooleanField(default=False, blank=True, null=True)
    coin_spent = models.DecimalField(max_digits=5, blank=True, null=True, default=0, decimal_places=1)
    is_successful = models.BooleanField(default=False)



class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='menu_item', null=True, blank=True)
    category = models.ManyToManyField('Category', related_name='item')
    today_special = models.BooleanField(blank=True, default=False)



class Category(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='menu_item', null=True, blank=True)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(null=True, blank=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    cart_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    response_time = models.TimeField(blank=True, null=True)
    accepted = models.BooleanField(default=False, null=True, blank=True)
    cancelled = models.BooleanField(default=False, null=True, blank=True)
    delivered = models.BooleanField(default=False, null=True, blank=True)
    expected_delivery_time = models.TimeField(null=True, blank=True)
    delivery_time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=200, null=True, blank=True)
    comment = models.TextField(blank=True, null=True)
    seat = models.CharField(max_length=200, null=True, blank=True)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


#one succesful order per date
#any no. of person can apply to place that request for that particular date.
#one successful per customer and no another order +91822598112


class Order_1(models.Model):
    id=models.AutoField(primary_key=True)
    customer = models.OneToOneField(User, on_delete=models.CASCADE)
    date=models.DateField(unique_for_date=True)
    is_successful=models.BooleanField()

    class Meta:
        unique_together=(('id','date'))


class queued_order(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)



class Successful_order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)










