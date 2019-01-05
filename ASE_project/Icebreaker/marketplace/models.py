from django.db import models
from django.db.models import PROTECT
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
import datetime
from datetime import timedelta

class product(models.Model):
    fullname = models.ForeignKey(User, on_delete=models.PROTECT,null = True, blank = True) #foreign key from user table from django-admin
    product_title = models.CharField(max_length = 100,)
    product_type = models.CharField(null=True, max_length = 100)
    overview = models.TextField()
    description = models.TextField(null = True)
    date = models.DateTimeField(auto_now_add = True)
    image = models.ImageField(upload_to="media", blank=True)
    quantity = models.PositiveIntegerField(null=True)
    cost = models.FloatField(null=True)
#    pic = models.ForeignKey(profile, on_delete=models.PROTECT,null = True, blank = True)

    def __str__(self):
        return self.product_title

    def snippept(self):
        return self.overview[:50] + "..."

class OrderItem(models.Model):
    product = models.ForeignKey(product, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    date_ordered = models.DateTimeField(null=True)
    qty = models.PositiveIntegerField(null=True,default=1)
    ref_code = models.CharField(max_length=20)
    cost = models.IntegerField(null=True,default=0)

    def __str__(self):
        return self.product.product_title

    # def order_item_total(self):
    #     return float(product.cost) * float(product.quantity)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='o')
    ref_code = models.CharField(max_length=20)
    items = models.ManyToManyField(OrderItem)
    is_ordered = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(null=True)

    def get_cart_item(self):
        return self.items.all()

    def get_cart_total(self):
        return sum([item.product.cost*item.qty for item in self.items.all()])

    def __str__(self):
        return '{0} -- {1}'.format(self.user, self.ref_code)

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=120)
    order_id = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    success = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.order_id

    class Meta:
        ordering = ['-timestamp']
