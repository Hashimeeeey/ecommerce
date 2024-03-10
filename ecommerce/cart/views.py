from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from shop.models import Product
from cart.models import Cart,Account,Order
from django.db import transaction
from django.contrib import messages

@login_required
def cartview(request):
    u = request.user
    try:
        cart_items = Cart.objects.filter(user=u)
        total = sum(item.quantity * item.product.price for item in cart_items)
    except Cart.DoesNotExist:
        cart_items = []
        total = 0

    return render(request, 'cartview.html', {'c': cart_items, 'total': total})

@login_required
# Create your views here.
def cart(request, n):
    p = Product.objects.get(name=n)
    u = request.user
    try:
        cart = Cart.objects.get(user=u, product=p)
        if (p.stock > 0):
            cart.quantity += 1
            cart.save()
            p.stock -= 1
            p.save()

    except:
        if (p.stock > 0):
            cart = Cart.objects.create(product=p, user=u, quantity=1)
            cart.save()
            p.stock-=1
            p.save()

    return redirect('cart:cartview')
@login_required
def cart_remove(request, n):
    p = Product.objects.get(name=n)
    u = request.user
    try:
        cart = Cart.objects.get(user=u, product=p)
        if (cart.quantity >1):
            cart.quantity -= 1
            cart.save()
            p.stock += 1
            p.save()

        else:
            cart.delete()
            p.stock += 1
            p.save()

    except:
       pass

    return redirect('cart:cartview')
@login_required
def full_remove(request, n):
    p = Product.objects.get(name=n)
    u = request.user
    try:
        cart = Cart.objects.get(user=u, product=p)
        cart.delete()
        p.stock += cart.quantity
        p.save()
    except:
       pass

    return cartview(request)
@login_required
def orderform(request):
    if request.method == "POST":
        a = request.POST['a']
        ph = request.POST['ph']
        an = request.POST['an']

        u = request.user
        cart = Cart.objects.filter(user=u)
        total = 0
        for i in cart:
            total += i.quantity * i.product.price
        try:
            ac = Account.objects.get(acctnum=an)  # to retrieve the acctobject
            if ac.amount >= total:
                ac.amount = ac.amount - total
                ac.save()
                for i in cart:
                    o = Order.objects.create(user=u, product=i.product, address=a, phone=ph, no_of_items=i.quantity, order_status="paid")
                    o.save()
                cart.delete()
                return redirect('cart:orderview')

            else:
                msg = "Insufficient amount, you can't place an order"
                return render(request, "orderdetail.html", {'msg': msg})
        except Account.DoesNotExist:
            pass

    return render(request, 'orderform.html')
@login_required
def orderview(request):
    u=request.user
    o=Order.objects.filter(user=u)
    return render(request,'orderview.html',{'o':o})