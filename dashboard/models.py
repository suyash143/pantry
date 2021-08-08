from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True,blank=True)
    email = models.CharField(max_length=200, null=True,blank=True)
    coin=models.DecimalField(max_digits=5,blank=True,null=True,default=0, decimal_places=1)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    description=models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to='menu_item',null=True, blank=True)
    category=models.ManyToManyField('Category',related_name='item')
    today_special=models.BooleanField(blank=True,default=False)

    def save(self, *args, **kwargs):
        if self.today_special:
            try:
                temp = Product.objects.get(today_special=True)
                if self != temp:
                    temp.today_special = False
                    temp.save()
            except Product.DoesNotExist:
                pass
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Category(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='menu_item', null=True, blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    complete = models.BooleanField(default=False,null=True,blank=True)
    price=models.DecimalField(max_digits=7, decimal_places=2,null=True,blank=True)
    transaction_id = models.CharField(max_length=100, null=True,blank=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
    

