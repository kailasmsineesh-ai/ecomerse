from django.shortcuts import render

from shop.models import Product

# Create your views here.

def home(request):
    return render(request,'index.html')

def allproducts(request):
    products = Product.objects.all() 
    return render(request,'allproducts.html', {'products': products})


