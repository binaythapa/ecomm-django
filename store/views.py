import json
import datetime
from math import ceil
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import JsonResponse

from passlib.hash import pbkdf2_sha256

# Create your views here.
#from django.views.generic import FormView

from review.forms import userReviewForm
from review.models import Comment

from .forms import UserForm, addcategory, productform, ProfileForm, UserRegisterForm, SupplierForm,CreateUser
from .models import *
from .utils import *


def search(request):
    w_data = wishData(request)
    total = w_data['wishItems']

    Data = cartData(request)
    cartItems = Data['cartItems']

    val = request.GET['q']
    search= Product.objects.all().filter(name__icontains= val)
    return render(request, 'store/allproduct.html', {'product': search, 'cartItems': cartItems, 'wishItems': total})


def store(request):
    w_data = wishData(request)
    total1 = w_data['wishItems']
    total2 = w_data['orderItems']
    total3=  w_data['likeItems']
    Data = cartData(request)
    cartItems = Data['cartItems']
    product = Product.objects.all()

    collection= {'product': product, 'cartItems': cartItems, 'wishItems':total1, 'orderItems':total2, 'likeItems':total3}
    return render(request, 'store/banner.html', collection)

#@login_required(login_url='login') #redirect when user is not logged in
def checkout(request):
    Data = cartData(request)
    cartItems = Data['cartItems']
    order = Data['order']
    items = Data['items']
    return render(request, 'store/CheckOut.html', {'item': items, 'order': order,'cartItems': cartItems,'shipping': False})

def cart(request):
    w_data = wishData(request)
    total = w_data['wishItems']

    Data = cartData(request)
    cartItems = Data['cartItems']
    order = Data['order']
    items = Data['items']

    if cartItems == 0:
        messages.warning(request, 'sorry,Your cart is empty')
        return redirect("store")

    else:
        return render(request, 'store/cart.html', {'items': items, 'order': order, 'cartItems': cartItems, 'wishItems':total})




def updateItem(request):
    data= json.loads(request.body)
    productId = data['productId']
    action= data['action']

    customer = request.user.customer
    product= Product.objects.get(id= productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    try:
        orderItem, created = Orderitem.objects.get_or_create(product=product,order=order)
        print(f" name of order item {orderItem.product.name}")
        if action == 'add':
            orderItem.quantity = (orderItem.quantity + 1)

        elif action == 'remove':
            orderItem.quantity = (orderItem.quantity - 1)

        orderItem.save()

        if orderItem.quantity <= 0:
            orderItem.delete()
    except:
        print("Sorry, unable to perform orderItem")
    return JsonResponse('Item was added successfully', safe=False)



def processOrder(request):
    transaction_id= datetime.datetime.now().timestamp()
    data= json.loads(request.body)

    if request.user.is_authenticated:
        customer= request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        if order.shipping == True:
           ShippingAddress.objects.create(
                customer= customer,
                order= order,
                address= data['shipping']['address'],
                state= data['shipping']['state'],
                zipcode= data['shipping']['zipcode'],
            )

    else:
        customer, order= guestOrder(request, data)

    # total = float(data['form']['total'])

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
    total = float(str(data['form']['total']).strip().replace(',', '.'))
    order.transaction_id = transaction_id
    if total == order.get_cart_total:
        order.complete = True
    order.save()
    return JsonResponse('Payment Complete', safe=False)

def showdetail(request, pk):
    w_data = wishData(request)
    total = w_data['wishItems']

    Data = cartData(request)
    cartItems = Data['cartItems']

    data = Product.objects.get(pk=pk)
    product = Product.objects.all().filter(category=data.category)
    comment_all= Comment.objects.all()


    form = userReviewForm(request.POST or None)
    if request.method=="POST" and form.is_valid():
        cmt= form.cleaned_data['userComment']
        user= request.user
        userReview.objects.create(
            userComment=cmt,
            user=user,
            product= data,
                 )
    else:
        form= userReviewForm()


    comment = Comment.objects.all().filter(product=pk)
    i = 0
    total1 = sum([i + 1 for item in comment])
    like = Like.objects.all().filter(product=pk)
    i = 0
    total2 = sum([i + 1 for item in like])

    collection= {'cartItems': cartItems, 'form': form, 'review': comment_all,'data':data, 'product':product, 'wishItems':total,'commentItems':total1, 'likeItems':total2}
    return render(request,'store/productdetail.html', collection)


def profile(request):
    w_data = wishData(request)
    total = w_data['wishItems']

    Data = cartData(request)
    cartItems = Data['cartItems']

    product= Product.objects.all()

    #orderitem= Orderitem.objects.all()

    return render(request, 'store/profile.html',{'product': product, 'cartItems': cartItems, 'wishItems':total})

def category(request):
    data = Product.objects.all()
    return render(request, 'store/allproduct.html',{'product': data})


def supplier(request):
    Data = cartData(request)
    cartItems = Data['cartItems']
    category = Category.objects.all()

    product = Product.objects.all()
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item["category"] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params = {'allProds': allProds, 'cartItems': cartItems, 'category': category}
    return render(request, "store/store.html", params)

def order(request):
    Data = cartData(request)
    cartItems = Data['cartItems']
    category = Category.objects.all()
    items = Data['items']
    order= Order.objects.all()
    #orderitem = Orderitem.objects.filter(order= order)
    #print(orderitem)
    allProds = []
    catprods = Orderitem.objects.values('order', 'id')
    cats = {item["order"] for item in catprods}
    for cat in cats:
        prod = Orderitem.objects.filter(order=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
        print(f"hello world...{allProds}")
    params = {'allProds': allProds, 'cartItems': cartItems, 'category': category, 'item':items}
    return render(request, "store/order.html", params)


@login_required
@transaction.atomic
def update_profile(request):
    customer = Customer.objects.get(user=request.user)
    orderitem = Orderitem.objects.all()

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST,request.FILES or None,instance=request.user.customer)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect("store")
        else:
            messages.error(request,('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.customer)


    return render(request, 'store/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'customer':customer,
        'orderitem':orderitem,

    })



def cregister(request):
    if request.method == 'POST':
        form = CreateUser(request.POST or None)
        form1 = ProfileForm(request.POST or None, request.FILES or None)
        if form.is_valid() and form1.is_valid():
            user = form.save()
            instance = form1.save(commit=False)
            instance.user = user
            instance.save()

            return redirect("store")
            message.success(request, 'your account created successfully')
    else:
        form = CreateUser()
        form1 = ProfileForm()
    return render(request, 'register.html', {'user_form': form, 'profile_form': form1})



def addsupplier(request):
    if request.method == 'POST':
        user_form = CreateUser(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES or None)
        supplier_form = SupplierForm(request.POST, request.FILES or None)

        if user_form.is_valid() and profile_form.is_valid() and supplier_form.is_valid():

            user = user_form.save()

            instance = profile_form.save(commit=False)
            instance.user = user
            instance.save()

            supplier= supplier_form.save(commit=False)
            supplier.customer=instance
            supplier.save()

            messages.success(request, ('Your profile created successfully '))
            return redirect("store")
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = CreateUser()
        customer_form = ProfileForm()
        supplier_form = SupplierForm()


    return render(request, 'register.html', {
        'user_form': user_form,
        'profile_form': customer_form,
        'supplier_form': supplier_form,
    })

def add_product(request):
    if request.method=="POST":
        data= addcategory(request.POST)
        product= productform(request.POST,request.FILES or None)

        if data.is_valid() and product.is_valid():
            name= data.cleaned_data['name']
            parent_id = request.POST['select']
            category, created=Category.objects.get_or_create(name=name, parent_id= parent_id)
            instance= product.save(commit=False)
            instance.category= category
            instance.save()
            messages.warning(request, 'Product Addition Successful')

        else:
            HttpResponse("sorry, task is uncomplete")
        return redirect("add-product")
    else:
       form_c= addcategory()
       form_p= productform()
       data= Category.objects.all()
       return render(request, 'store/add_catagory.html', {'form_c': form_c, 'data':data, 'form_p':form_p})


""""------------update wishlist------------"""
def updatewishlist(request):
    data= json.loads(request.body)
    productId = data['productId']

    customer = request.user.customer
    product= Product.objects.get(id= productId)

    wishlist, created = Wishlist.objects.get_or_create(customer=customer, product=product)
    return JsonResponse('Item was added successfully', safe=False)




def wishlist(request):
    Data = cartData(request)
    cartItems = Data['cartItems']
    order = Data['order']
    items = Data['items']
    customer= request.user.customer

    w_data = wishData(request)
    total = w_data['wishItems']
    try:
        wishlist= Wishlist.objects.all().filter(customer = customer)
    except:
        wishlist= {}
    collection= {'items': items, 'cartItems': cartItems, 'wishItems': total, 'wishlist': wishlist}
    return render(request, 'store/wishlist.html', collection)

"""<-------------update like-------------->"""

def like(request):
    data= json.loads(request.body)
    productId = data['productId']

    customer = request.user.customer
    product= Product.objects.get(id= productId)

    like, created = Like.objects.get_or_create(customer=customer, product=product)

    return JsonResponse('Item was added successfully', safe=False)




def registeruser(request):
    if request.method=='POST':
        form= CreateUser(request.POST or None)
        form1= ProfileForm(request.POST or None, request.FILES or None)
        if form.is_valid() and form1.is_valid():
            user=form.save()
            instance= form1.save(commit= False)
            instance.user= user
            instance.save()

            return redirect("store")
            message.success(request,'your account created successfully')
    else:
        form =CreateUser()
        form1= ProfileForm()
    return render(request,'registerr.html', {'form': form, 'form1':form1})
