import decimal

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from phone_field import PhoneField
from django.db import models

# Create your models here.



class Customer(models.Model):
    user= models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    image= models.ImageField(null=True, blank=True, upload_to= 'customer_pics')
    phone= PhoneField(blank=True, help_text='Contact phone number')
"""
    @receiver(post_save, sender=User)
    def create_user_customer(sender, instance, created, **kwargs):
        if created:
            Customer.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_customer(sender, instance, **kwargs):
        instance.customer.save()
"""

class Supplier(models.Model):
    customer = models.OneToOneField(Customer, null=True, blank=True, on_delete=models.CASCADE)
    company = models.CharField(max_length= 200, null=True, blank=True)



class Category(models.Model):
    name= models.CharField(max_length= 200,null=True, blank=True)
    parent_id= models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name= models.CharField(max_length= 200,null=True, blank=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    category= models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True)
    code= models.CharField(max_length=200,null=True, blank=True)
    name= models.CharField(max_length= 200)
    price= models.DecimalField(max_digits = 7,decimal_places = 2)
    discount = models.FloatField(null=True, blank=True, default=0)
    digital= models.BooleanField(default= False, null= True, blank=False)
    image= models.ImageField(null= True, blank=True,default= 'default.jpg',upload_to= 'product_pics/%y/%m/%d/')
    image_back_view= models.ImageField(null= True, blank=True, default= 'default.jpg',upload_to= 'product_pics/%y/%m/')
    image_right_view = models.ImageField(null=True, blank=True, default= 'default.jpg',upload_to= 'product_pics/%y/%m/')
    image_left_view = models.ImageField(null=True, blank=True,default= 'default.jpg',upload_to= 'product_pics/%y/%m/')
    details= models.CharField(max_length=500, blank= True,default= 'default.jpg')
    status= models.BooleanField(default=False, blank=True, null=True)



    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url= self.image.url
        except:
            url= ''
        return url

    @property
    def imageL(self):
        try:
            url = self.image_left_view.url
        except:
            url = ''
        return url

    @property
    def imageR(self):
        try:
            url = self.image_right_view.url
        except:
            url = ''
        return url

    @property
    def imageB(self):
        try:
            url = self.image_back_view.url
        except:
            url = ''
        return url
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_time= models.DateTimeField(auto_now_add= True)
    complete= models.BooleanField(default= True, null= True, blank= False)
    transaction_id= models.CharField(max_length=200, null= True)
    status= models.BooleanField(default=False,null=True, blank=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping= False
        orderitems= self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping= True
        return shipping


    @property
    def get_cart_total(self):
        orderitems= self.orderitem_set.all()
        total= sum([item.get_total() for item in orderitems])
        return total

    @property
    def get_cart_net_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([(item.get_total()-item.get_discount_total()) for item in orderitems])
        return total

    @property
    def get_cart_discount_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([(item.get_discount_total()) for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total



class Orderitem(models.Model):
    product= models.ForeignKey(Product, on_delete= models.SET_NULL, blank=True, null=True)
    order= models.ForeignKey(Order, on_delete=models.SET_NULL, blank= True, null=True)
    quantity= models.IntegerField(default=0, null=True, blank=True)
    date_added= models.DateTimeField(auto_now_add= True)

    def get_total(self):
        total= self.product.price * self.quantity
        return total

    def get_total_inc_discount(self):
        total= self.product.price *decimal.Decimal((100-self.product.discount)*0.001)
        return total

    def get_discount_total(self):
        total = self.product.price * self.quantity * decimal.Decimal(self.product.discount*0.01)
        return total


    def get_net_total(self):
        total_amount=self.product.price * self.quantity
        discount_amount=self.product.price * self.quantity * decimal.Decimal(self.product.discount*0.001)
        total = total_amount-discount_amount
        return total

    #def __str__(self):
      #  return self.product.name

class Wishlist(models.Model):
    product=models.OneToOneField(Product, on_delete= models.CASCADE, blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.customer)

class Like(models.Model):
    product=models.ForeignKey(Product, on_delete= models.SET_NULL, blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name

class ShippingAddress(models.Model):
    customer= models.ForeignKey(Customer, on_delete= models.SET_NULL, blank=True, null=True)
    order= models.ForeignKey(Order, blank=True, null=True, on_delete= models.SET_NULL)
    address= models.CharField(max_length= 200, null=True)
    state= models.CharField(max_length=200, null=True)
    zipcode= models.CharField(max_length=200,null=200)
    date_added= models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.address






