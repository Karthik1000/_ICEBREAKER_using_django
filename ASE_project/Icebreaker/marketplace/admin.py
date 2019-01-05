from django.contrib import admin
from .models import product, OrderItem, Order, Transaction

admin.site.register(product)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Transaction)
