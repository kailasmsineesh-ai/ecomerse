from django.shortcuts import render,redirect

from shop.models import Product,Category,Cart,CartItem


from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.db.models import Q
from django.core.paginator import Paginator


# Create your views here.
def cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
        cart = request.session.session_key

    return cart

def cart(request):
    cart = cart_id(request)

    cart_item = CartItem.objects.filter(CART__cart_id = cart)
    tamount =0
    for i in cart_item:
        tamount += i.PRODUCT.price*i.quantity
    cart_context= {
        "cart_item":cart_item,
        "cart_total":tamount
    }

    return cart_context

def home(request):

    cart_context = cart(request)
    cart_item = cart_context['cart_item']
    cart_total = cart_context['cart_total']





    products = Product.objects.all().order_by('-created_time')[0:10]
    category = Category.objects.all()
    cat = request.GET.get("category")
    if cat:
        products = products.filter(CATEGORY_id=cat)
    return render(request,'index.html', {'products': products, 'category': category ,"cart_item":cart_item,'cart_total':cart_total })

def allproducts(request):
    cart_context = cart(request)
    cart_item = cart_context['cart_item']
    cart_total = cart_context['cart_total']


    products = Product.objects.all().order_by('-created_time')
    category = Category.objects.all()

    cat = request.GET.get("category")
    if cat:
        products = products.filter(CATEGORY_id=cat)
    

    qry = request.GET.get("q")
    if qry:
        products = Product.objects.filter(Q(name__icontains=qry)|Q(description__icontains=qry)).order_by('-created_time')

    paginator = Paginator(products,5)
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)
    return render(request,'allproducts.html', {'page_obj': page_obj, 'category': category,"cart_item":cart_item,'cart_total':cart_total})


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
    cart_context = cart(request)
    cart_item = cart_context['cart_item']
    cart_total = cart_context['cart_total']



    return render(request,'register.html', {"cart_item":cart_item,'cart_total':cart_total})


def sign_in(request):

    cart_context = cart(request)
    cart_item = cart_context['cart_item']
    cart_total = cart_context['cart_total']

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user :
            login(request, user)
            return redirect('home')
        else:
            return render(request,'login.html', {'error': 'Invalid username or password'})
    return render(request,'login.html' , {"cart_item":cart_item,'cart_total':cart_total})

def sign_out(request):
    logout(request)
    return redirect('home')

def product_details(request, p_id):
    cart_context = cart(request)
    cart_item = cart_context['cart_item']
    cart_total = cart_context['cart_total']

    product = Product.objects.get(id=p_id)
    return render(request,'productdetail.html', {'product': product, "cart_item": cart_item, 'cart_total': cart_total})





def add_to_cart(request, p_id):
    product =Product.objects.get(id=p_id)
    c_id = cart_id(request)
    try:
        cart = Cart.objects.get(cart_id=c_id)
    except:
        cart = Cart.objects.create(cart_id=c_id)
    try :
        cartitem = CartItem.objects.get(CART=cart, PRODUCT=product)
        if cartitem:
            cartitem = cartitem
            cartitem.quantity += 1
            cartitem.save()
        else:
            CartItem.objects.create(CART=cart, PRODUCT=product, quantity=1)
        
    except:
        CartItem.objects.create(CART=cart, PRODUCT=product, quantity=1)

    return redirect('home')

def minus_from_cart(request,p_id):
    product=Product.objects.get(id=p_id)
    c_id=cart_id(request)
    cart = Cart.objects.get(cart_id=c_id)
    try:
        cartitem=CartItem.objects.get(CART=cart, PRODUCT=product)
        if cartitem:
                if cartitem.quantity == 1:
                    cartitem.delete()
                else:
                    cartitem = cartitem
                    cartitem.quantity -= 1
                    cartitem.save()
    except:
        pass
    return redirect('home')



def remove_cart_item(request,p_id):
    product=Product.objects.get(id=p_id)
    c_id=cart_id(request)
    cart= Cart.objects.get(cart_id=c_id)
    cartitem=CartItem.objects.get(CART=cart,PRODUCT=product)
    cartitem.delete()

    return redirect('home')


def buynow(request):
  
    return render(request, 'buynow.html')

    











    