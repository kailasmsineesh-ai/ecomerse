from django.shortcuts import render,redirect

from shop.models import Product


from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def home(request):
    products = Product.objects.all().order_by('-created_time')[0:10]
    return render(request,'index.html', {'products': products})

def allproducts(request):
    products = Product.objects.all().order_by('-created_time')
    return render(request,'allproducts.html', {'products': products})


def register(request):

    if request.method == 'POST':
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password != confirm_password:
            return render(request,'register.html', {'error': 'Passwords do not match'})
        
        if User.objects.filter(username=username).exists():
            return render(request,'register.html', {'error': 'Username already taken'})
        if User.objects.filter(email=email).exists():
            return render(request,'register.html', {'error': 'Email already registered'})
        user = User.objects.create_user(username=username, email=email, password=password, first_name=fname, last_name=lname)
        user.save()
        return redirect('login')


    return render(request,'register.html')


def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user :
            login(request, user)
            return redirect('home')
        else:
            return render(request,'login.html', {'error': 'Invalid username or password'})
    return render(request,'login.html')

def sign_out(request):
    logout(request)
    return redirect('home')

def product_details(request, p_id):
    product = Product.objects.get(id=p_id)
    return render(request,'productdetail.html', {'product': product})