from django.shortcuts import render,redirect
from django.views.generic import ListView,DetailView,CreateView,View,UpdateView
from shop.models import Category,Product
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from shop.forms import Registrationform
from django.contrib.auth.views import LoginView
from  django.contrib.auth import logout
class Home(ListView):
    template_name = 'home.html'
    model = Category
    context_object_name = 'cat'

class CategoryView(DetailView):
    template_name = 'categoryview.html'
    model= Category
    context_object_name = 'cat'

class ProductView(DetailView):
    template_name = 'productview.html'
    model=Product
    context_object_name = 'pro'

class Register(CreateView):
    model = User
    template_name = 'register.html'
    # fields = ['username', ' ', 'email', 'first_name', 'last_name']
    form_class = Registrationform
    success_url = reverse_lazy('shop:home')

    def form_valid(self, form):  # When password is not converted into
        u=form.cleaned_data['username']
        p = form.cleaned_data['password']
        e = form.cleaned_data['email']
        f = form.cleaned_data['first_name']
        l = form.cleaned_data['last_name']

        b=User.objects.create_user(username=u,password=p,email=e,first_name=f,last_name=l)
        b.save()
        return redirect('shop:home')

class Login(LoginView):
    template_name = 'login.html'

class Logout(View):
    def get(self,request):
        logout(request)
        return redirect('shop:login')

class Addcatogries(CreateView):
    model = Category
    template_name = 'addcatogries.html'
    fields = ['name','desc','image']
    success_url = reverse_lazy('shop:home')

class Addproduct(CreateView):
    model = Product
    template_name = 'addproduct.html'
    fields = ['name','desc','image','price','stock','category']
    success_url = reverse_lazy('shop:home')

class Addstock(UpdateView):
    model= Product
    template_name = 'addstock.html'
    fields = ['stock']
    success_url = reverse_lazy('shop:home')