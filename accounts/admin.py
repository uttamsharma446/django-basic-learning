from ast import Or
from django.contrib import admin

from .models import Customer, Product, Order, Tags

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Tags)
