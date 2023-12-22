from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from shop.models import Product
from cart.models import Cart,Account,Order


def cartview(request):
    total=0
    u=request.user
    try:
        cart=Cart.objects.filter(user=u)
        for i in cart:
            total+=i.quantity*i.product.price
    except:
        pass
    return render(request,'cart.html',{'c':cart,'total':total})
# Create your views here.
@login_required
def add_to_cart(request,p):
    product=Product.objects.get(name=p)
    u=request.user
    try:
        cart=Cart.objects.get(product=product,user=u)
        if(cart.quantity<cart.product.stock):
            cart.quantity+=1
        cart.save()
    except:
        cart=Cart.objects.create(product=product,user=u,quantity=1)
        cart.save()
    return redirect('cart:cartview')
@login_required
def cart_remove(request,p):
    product=Product.objects.get(name=p)
    u=request.user
    try:
        cart=Cart.objects.get(product=product,user=u)
        if cart.quantity>1:
            cart.quantity-=1
            cart.save()
        else:
             cart.delete()
    except:
        pass
    return redirect('cart:cartview')

def full_remove(request,p):
    product=Product.objects.get(name=p)
    u=request.user
    try:
        cart=Cart.objects.get(product=product,user=u)
        cart.delete()
    except:
        pass
    return redirect('cart:cartview')

def orderform(request):
    if(request.method=="POST"):
        a=request.POST['a']
        p = request.POST['p']
        n = request.POST['n']
        u=request.user
        cart=Cart.objects.filter(user=u)

        total = 0
        for i in cart:
                total += i.quantity * i.product.price
        ac=Account.objects.get(acctnum=n)
        if (ac.amount>=total):
            ac.amount=ac.amount-total
            ac.save()

            for i in cart:# creates record in order table for each object in cart table for the current user
                o=Order.objects.create(user=u,product=i.product,address=a,phone=p,noofitems=i.quantity,order_status="paid")
                o.save()
                i.product.stock=i.product.stock-i.quantity
                i.product.save()
            cart.delete()#clears the cart after placement
            msg="Order Placed Successfully"
            return render(request,'orderdetail.html',{'m':msg})


        else:
            msg="Insufficient Amount in User Account.You cannot place Order."
            return render(request, 'orderdetail.html', {'m': msg})

    return render(request,'orderform.html')


def orderview(request):
    u=request.user
    o=Order.objects.filter(user=u)
    return render(request,'orderview.html',{'u':u.username,'o':o})

