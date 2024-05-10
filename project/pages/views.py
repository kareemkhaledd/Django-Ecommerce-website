from urllib import request
from django.http import HttpResponse ,JsonResponse
from django.shortcuts import render , redirect
from django.views import View
from . models import Customer, Product,Cart,Wishlist,Payment,OrderPlaced
from django.db.models import Count,Q
from . forms import CustomerProfileForm, CustomerRegistrationForm
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.shortcuts import get_object_or_404
from django.urls import reverse
#from django.http import HttpResponse    
# Create your views here.
def index(request):
    totalitem = 0
    witem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        witem = len(Wishlist.objects.filter(user=request.user))
    return render(request,'pages/home.html',locals())

def about(request):
    totalitem = 0
    witem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        witem = len(Wishlist.objects.filter(user=request.user))
    return render(request,'pages/about.html',locals())


from django.db.models import Q

class SearchResultsView(View):
    def get(self, request):
        query = request.GET.get('q')
        products = Product.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        return render(request, 'pages/search_results.html', {'products': products, 'query': query})


def contact(request):
    totalitem = 0
    witem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        witem = len(Wishlist.objects.filter(user=request.user))
    return render(request,'pages/contact.html',locals())

class CategoryView(View): 
    def get(self, request, val): 
        totalitem = 0
        witem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            witem = len(Wishlist.objects.filter(user=request.user))
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        # .annotate(total=Count('title'))
        return render(request, "pages/category.html",locals())
    
class CategoryTitle(View):

    def get(self, request, val):
        totalitem = 0
        witem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            witem = len(Wishlist.objects.filter(user=request.user))
        product = Product.objects.filter(title=val)

        title = Product.objects.filter(category=product[0].category).values("title")

        return render(request, "pages/category.html",locals())


class ProductDetail(View): 
    def get(self, request,pk):
        totalitem = 0
        witem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            witem = len(Wishlist.objects.filter(user=request.user))
            product = Product.objects.get(pk=pk)
            wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
            return render(request, "pages/productdetail.html",locals())
        else:
            return redirect("login")
    

class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request, 'pages/customerregistration.html',locals())
    

    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratiolations! User registeres successfully")
        else:
            messages.warning(request,"Invalid input data")
        return render(request, 'pages/customerregistration.html',locals())
    
class ProfileView(View):
    def get(self,request):
        totalitem = 0
        witem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            witem = len(Wishlist.objects.filter(user=request.user))
        form = CustomerProfileForm()
        return render(request, 'pages/profile.html',locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user,name=name,locality=locality,city=city,mobile=mobile,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congratiolations! Profile save successfully")
        else:
            messages.warning(request,"Invalid input data")
        return render(request, 'pages/profile.html',locals())
    

def address(request):
    totalitem = 0
    witem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        witem = len(Wishlist.objects.filter(user=request.user))
    add =  Customer.objects.filter(user=request.user)
    return render(request, 'pages/address.html',locals())


class updateAddress (View):

    def get(self, request , pk):
        totalitem = 0
        witem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            witem = len(Wishlist.objects.filter(user=request.user))
        add =  Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'pages/updateAddress.html',locals())

    def post(self, request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():

            add = Customer.objects.get(pk=pk)

            add.name = form.cleaned_data['name']

            add.locality = form.cleaned_data['locality']

            add.city = form.cleaned_data['city']

            add.mobile = form.cleaned_data['mobile']

            add.state = form.cleaned_data['state']

            add.zipcode = form.cleaned_data['zipcode']

            add.save()

            messages.success(request, "Congratulations! Profile Update Successfully")

        else:

            messages.warning (request, "Invalid Input Data")

        return redirect("address")


def custom_logout(request):
    logout(request)
    return redirect('login')


def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return redirect("showcart")
    if Cart.objects.filter(user=user, product=product).exists():
        return redirect("showcart")
    Cart(user=user, product=product).save()
    return redirect("showcart")


def show_cart(request):
    user = request.user
    totalitem = 0
    witem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        witem = len(Wishlist.objects.filter(user=request.user))
    cart=Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value=p.quantity*p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40
    return render(request,'pages/addtocart.html',locals())


class checkout(View):
    def get(self,request):
        totalitem = 0
        witem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            witem = len(Wishlist.objects.filter(user=request.user))
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount=0
        for p in cart_items:
            value = p.quantity*p.product.discounted_price
            famount = famount + value
        totalamount = famount + 25
    
        return render(request,'pages/checkout.html',locals())

def paymentSuccessful(request):
    return render(request, 'pages/payment-success.html')

def paymentFailed(request):
    return render(request, 'pages/payment-failed.html')

def plus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value=p.quantity*p.product.discounted_price
            amount = amount + value
        totalamount = amount + 25
        #print(prod_id)
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    


def minus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value=p.quantity*p.product.discounted_price
            amount = amount + value
        totalamount = amount + 25
        #print(prod_id)
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    


def remove_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value=p.quantity*p.product.discounted_price
            amount = amount + value
        totalamount = amount + 25
        #print(prod_id)
        data={
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    

def plus_wishlist(request):

    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        product=Product.objects.get(id=prod_id)
        user=request.user
        Wishlist(user=user, product=product).save()
        data={
            'message': 'Wishlist Added Successfully',
        }
        return JsonResponse(data)

def minus_wishlist(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        product=Product.objects.get(id=prod_id)
        user=request.user
        Wishlist.objects.filter(user=user, product=product).delete()
        data={
            'message': 'Wishlist Remove Successfully',
        }
        return JsonResponse(data)
    


def payment(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    host = request.get_host()
    famount = 0
    product_names = []

    # Calculate total amount and collect product names
    for cart_item in cart_items:
        value = cart_item.quantity * cart_item.product.discounted_price
        famount += value
        product_names.append(cart_item.product.title)

    # Join the product names into a single string
    product_names_str = ', '.join(product_names)

    # Calculate total amount
    totalamount = famount + 25

    # Define PayPal checkout parameters
    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': totalamount,
        'item_name': product_names_str,
        'invoice': str(uuid.uuid4()),  # Convert UUID to string
        'currency_code': 'USD',  # Verify that 'EGY' is correct
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('payment-successful')}",
        'cancel_url': f"http://{host}{reverse('payment-failed')}",
    }

    # Create PayPalPaymentsForm instance
    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    # Pass variables to the template context
    context = {
        'cart_items': cart_items,
        'totalamount': totalamount,
        'paypal': paypal_payment,  # Pass PayPalPaymentsForm instance as 'paypal'
    }
    

    return render(request, 'pages/payment.html', context)



def afterpayment(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    famount = 0
    product_names = []

    # Calculate total amount and collect product names
    for cart_item in cart_items:
        value = cart_item.quantity * cart_item.product.discounted_price
        famount += value
        product_names.append(cart_item.product.title)

    # Join the product names into a single string
    product_names_str = ', '.join(product_names)

    # Calculate total amount
    totalamount = famount + 25

    # Create Payment object
    payment = Payment.objects.create(
        user=user,
        amount=totalamount,
        payment_status='Succeeded',
        paid=True,
    )

    # Save Payment object
    payment.save()

    # Create OrderPlaced objects for each cart item
    for cart_item in cart_items:
        OrderPlaced.objects.create(
            user=user,
            product=cart_item.product,
            quantity=cart_item.quantity,
            status='Accepted'
        )

        # Delete the cart item after creating the order
        cart_item.delete()

    return redirect("orders")


def orders(request):
    totalitem = 0
    witem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    order_placed=OrderPlaced.objects.filter(user=request.user)
    return render(request, 'pages/orders.html', locals())



def wishlist(request):
    totalitem = 0
    witem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    WISHlist=Wishlist.objects.filter(user=request.user)
    return render(request, 'pages/wishlist.html', locals())