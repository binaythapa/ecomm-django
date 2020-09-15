from django.contrib import admin

from .models import Customer, Product, ShippingAddress, Orderitem, Order,Category,Brand,Wishlist,Supplier

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Orderitem)
admin.site.register(ShippingAddress)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Wishlist)
admin.site.register(Supplier)


from django.contrib import admin

# Register your models here.
