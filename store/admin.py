from django.contrib import admin

from .models import Customer, Product, ShippingAddress, Orderitem, Order,Catagory,SubCatagory,Brand

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Orderitem)
admin.site.register(ShippingAddress)
admin.site.register(Catagory)
admin.site.register(SubCatagory)
admin.site.register(Brand)
from django.contrib import admin

# Register your models here.
