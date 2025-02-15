from django.shortcuts import render
from shop.models import Product
from  django.db.models import Q
# Create your views here.

def search(request):
    if request.method=='POST':
        q=request.POST['q']
        b=Product.objects.filter(Q(name__icontains=q) | Q(desc__icontains=q))
        context={'pro':b}
    return render(request,'search.html',context)
