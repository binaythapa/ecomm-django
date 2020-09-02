import json
import datetime
from math import ceil

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
    """
    Data = cartData(request)
    cartItems = Data['cartItems']
    catagory= SubCatagory.objects.all()


    product = Product.objects.all()
    n= len(product)
    nslides= n//4+ceil((n/4)+(n//4))

    allprods= []
    catprods= Product.objects.values('subcatagory', 'id')
    cats = [item['subcatagory'] for item in catprods]
    for cat in cats:
        prod= Product.objects.filter(subcatagory= cat)
        allprods.append([prod, range(1, nslides), nslides])
    print(f" alprods[1]: {allprods}")
    print(f"nslides{nslides}")
    return render(request, 'store/store.html',{'product': allprods, 'cartItems': cartItems,'catagory':catagory})
"""
    Data = cartData(request)
    cartItems = Data['cartItems']
    catagory = SubCatagory.objects.all()


    products = Product.objects.all()
    allProds = []
    catprods = Product.objects.values('subcatagory', 'id')
    cats = {item["subcatagory"] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(subcatagory=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params = {'allProds': allProds,'cartItems': cartItems,'catagory':catagory}
    return render(request, "store/store.html", params)

def checkout(request):
    Data = cartData(request)
    cartItems = Data['cartItems']
    order = Data['order']
    items = Data['items']
    catagory = SubCatagory.objects.all()
    return render(request, 'store/Checkout.html', {'item': items, 'order': order,'cartItems': cartItems,'shipping': False, 'catagory': catagory})

def cart(request):
    Data = cartData(request)
    cartItems = Data['cartItems']
    order = Data['order']
    items = Data['items']
    catagory = SubCatagory.objects.all()

    return render(request, 'store/Cart.html', {'items': items, 'order': order, 'cartItems': cartItems, 'catagory':catagory})


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


    product= Product.objects.all()
    catagory = SubCatagory.objects.all()

    try:
        review = userReview.objects.filter(product=pk)
    except:
        review= {}

    return render(request, 'store/show-detail.html', {'data':data, 'cartItems': cartItems, 'form': form, 'review': review,'product':product,'catagory':catagory })


def profile(request):
    Data = cartData(request)
    cartItems = Data['cartItems']

    product= Product.objects.all()
    catagory = SubCatagory.objects.all()
    return render(request, 'store/profile.html',{'product': product, 'cartItems': cartItems,'catagory':catagory})

def collection(request,id):
    Data = cartData(request)
    cartItems = Data['cartItems']
    catagory = SubCatagory.objects.all()
    product= Product.objects.filter(subcatagory=id)
    return render(request, 'store/catagory_product.html', {'product': product, 'cartItems': cartItems,'catagory':catagory})

def showorder(request):
    Data = cartData(request)
    cartItems = Data['cartItems']
    catagory = SubCatagory.objects.all()

    orderitem= Orderitem.objects.all().order_by('date_added')
    return render(request, 'store/show-order.html', {'orderitem':orderitem,'cartItems': cartItems,'catagory':catagory})

