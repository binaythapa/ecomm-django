import json
import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
from review.forms import userReviewForm
from review.models import userReview
from .models import *
from .utils import cookieCart, cartData, guestOrder


def search(request):
    Data = cartData(request)
    cartItems = Data['cartItems']

    val = request.GET['q']
    search= Product.objects.all().filter(name__icontains= val)
    return render(request, 'store/search.html', {'product': search, 'cartItems': cartItems})


def store(request):
    Data = cartData(request)
    cartItems = Data['cartItems']

    product = Product.objects.all()
    return render(request, 'store/search.html',{'product': product, 'cartItems': cartItems})


def checkout(request):
    Data = cartData(request)
    cartItems = Data['cartItems']
    order = Data['order']
    items = Data['items']
    return render(request, 'store/Checkout.html', {'item': items, 'order': order,'cartItems': cartItems,'shipping': False})

def cart(request):
    Data = cartData(request)
    cartItems = Data['cartItems']
    order = Data['order']
    items = Data['items']

    return render(request, 'store/Cart.html', {'items': items, 'order': order, 'cartItems': cartItems})


def updateItem(request):
    data= json.loads(request.body)
    productId = data['productId']
    action= data['action']

    print('Action:', action)
    print('productId:', productId)
    print("Product id and action are send to backend successfully")

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

    print("welcome at processorder")

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
    data = Product.objects.get(pk=pk)
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

    Data = cartData(request)
    cartItems = Data['cartItems']

    review= userReview.objects.all()
    product= Product.objects.all()

    return render(request, 'store/show-detail.html', {'data':data, 'cartItems': cartItems, 'form': form, 'review': review,'product':product })


def profile(request):
    Data = cartData(request)
    cartItems = Data['cartItems']

    product= Product.objects.all()

    #orderitem= Orderitem.objects.all()

    return render(request, 'store/profile.html',{'product': product, 'cartItems': cartItems})