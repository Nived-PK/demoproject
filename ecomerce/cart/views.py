import razorpay
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from shop.models import Product
from cart.models import Cart,Order_details,Payment

# Create your views here.
@login_required
def addtocart(request,i):
    user=request.user
    product=Product.objects.get(id=i)
    try:
        c=Cart.objects.get(user=user,product=product)
        if(product.stock>0):
            c.quantity+=1
            c.save()
            product.stock-=1
            product.save()

    except:
        if (product.stock > 0):
            c = Cart.objects.create(user=user, product=product, quantity=1)
            product.stock-= 1
            c.save()
            product.save()
    return redirect('cart:cartview')
@login_required
def cartview(request):
    u=request.user
    c=Cart.objects.filter(user=u)
    total=0
    for i in c:
        total+=i.quantity*i.product.price
    context={'cart':c,'total':total}
    return render(request,'cartview.html',context)

def cartminus(request,i):
    product=Product.objects.get(id=i)
    u=request.user
    try:
        c = Cart.objects.get(user=u, product=product)
        if(c.quantity>1):
            c.quantity -= 1
            c.save()
            product.stock += 1
            product.save()
        else:
            c.delete()
            product.stock +=1
            product.save()

    except:
        pass
    return redirect('cart:cartview')
def cartdelete(request,i):
    user=request.user
    product=Product.objects.get(id=i)
    try:
        c=Cart.objects.get(user=user, product=product)
        if c.quantity >=1:
            c.delete()
            product.stock += c.quantity
            product.save()
        else:
            pass
    except:
        pass
        return redirect('cart:cartview')

def orderform(request):
    if request.method=='POST':
        a=request.POST['a']
        p = request.POST['p']
        pc = request.POST['pc']

        u = request.user
        c = Cart.objects.filter(user=u)
        total = 0
        for i in c:
            total+=i.quantity * i.product.price
        total=int(total)

        client=razorpay.Client(auth=('rzp_test_nXXuyLZotv8p95','PqmVno6IgFtmwC6Wn5fPWjHQ'))
        response_payment=client.order.create(dict(amount=total*100,currency='INR'))
        print(response_payment)
        order_id=response_payment['id']   #retrieve the order id from response
        status=response_payment['status'] #retrieve the ststus from response

        if (status=="created"):
            pa=Payment.objects.create(name=u.username,amount=total,order_id=order_id)
            pa.save()

            for i in c:
                o=Order_details.objects.create(product=i.product,user=i.user,phone=p,address=a,pin=pc,order_id=order_id,no_of_items=i.quantity)
                o.save()

            context={'payment':response_payment,'name':u.username}

            return render(request,'payment.html',context)

    return render(request, 'orderform.html')
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import login
@csrf_exempt
def payment_status(request,p):
    user=User.objects.get(username=p)
    login(request,user)
    response=request.POST
    print(response)
    param_dict={
        'razorpay_order_id':response['razorpay_order_id'],
        'razorpay_payment_id':response['razorpay_payment_id'],
        'razorpay_signature':response['razorpay_signature']
    }
    client=razorpay.Client(auth=('rzp_test_nXXuyLZotv8p95','PqmVno6IgFtmwC6Wn5fPWjHQ'))
    try:
        status=client.utility.verify_payment_signature(param_dict)
        print(status)
        p=Payment.objects.get(order_id=response['razorpay_order_id'])
        p.paid=True
        p.razorpay_payment_id=response['razorpay_payment_id']
        p.save()

        o=Order_details.objects.filter(order_id=response['razorpay_order_id'])
        for i in o:
            i.payment_status="Completed"
            i.save()
        c=Cart.objects.filter(user=user)
        c.delete()
    except:
        pass
    return render(request,'paymentstatus.html')

def yourorders(request):
    u=request.user
    o=Order_details.objects.filter(user=u,payment_status="Completed")
    context={'orders':o}
    return render(request,'yourorders.html',context)