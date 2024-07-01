from django.shortcuts import render ,redirect
from django.views import View
from .models import Customer, Product,Cart,OrderPlaced
from .forms import CustomerRegistrationForm
from django.contrib import messages
from .forms import CustomerProfileForm
from django.db.models import Q
from django.http import JsonResponse 
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ProductView(View):
    def get(self,request):
        totalitem=0
        laptops=Product.objects.filter(category='L')
        watches=Product.objects.filter(category='W')
        mobiles=Product.objects.filter(category='M')
        headphones=Product.objects.filter(category='H')
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
        return render(request,'app/home.html',
            {'laptops':laptops,'watches':watches,'mobiles':mobiles,'headphones':headphones,'totalitem':totalitem})


class ProductDetailView(View):
    def get(self,request,pk):
        totalitem=0
        product=Product.objects.get(pk=pk)
        item_already_in_cart=False
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            item_already_in_cart=Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request,'app/productdetail.html',
            {'product':product,'item_already_in_cart':item_already_in_cart,'totalitem':totalitem})

@login_required # as it is function based 
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart') 

def show_cart(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount=0.0
        shipping_amount=70.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==user]
        #print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount=(p.quantity*p.product.discounted_price)
                amount+=tempamount
                total_amount=amount+shipping_amount
            return render(request, 'app/addtocart.html', {'carts': cart,'total_amount':total_amount,'amount':amount,'totalitem':totalitem})
        else:
            return render(request,'app/emptycart.html',{'totalitem':totalitem})

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'total_amount': amount + shipping_amount
        }

        return JsonResponse(data)



def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        if c.quantity > 1:  # Add this condition to prevent quantity from going below 1
            c.quantity -= 1
            c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'total_amount': amount + shipping_amount
        }

        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
    

        data = {
            'amount': amount,
            'total_amount': amount + shipping_amount
        }

        return JsonResponse(data)



@login_required # as it is function based
def address(request):
    add=Customer.objects.filter(user=request.user)
    return render(request,'app/address.html',{'add':add,'active': 'btn-primary'})

@login_required # as it is function based
def orders(request):
    op=OrderPlaced.objects.filter(user=request.user)
    return render(request,'app/orders.html',{'order_placed':op})


def mobile(request,data=None):
    if data==None:
        mobiles=Product.objects.filter(category='M')
    elif data=='below':
        mobiles=Product.objects.filter(category='M').filter(discounted_price__lt=10000)
    elif data=='above':
        mobiles=Product.objects.filter(category='M').filter(discounted_price__gt=10000)

    return render(request, 'app/mobile.html',{'mobiles':mobiles})

class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render(request,'app/customerregistration.html',
            {'form':form})
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Successfully Registered')
            form.save()
        return render(request,'app/customerregistration.html',

            {'form':form})

@login_required
def checkout(request):
    user =request.user
    add=Customer.objects.filter(user=user) 
    cart_items=Cart.objects.filter(user=user)
    amount=0.0
    shipping_amount=70.0
    total_amount=0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
        total_amount=amount+shipping_amount
    return render(request, 'app/checkout.html' ,{'add':add,'total_amount':total_amount,'cart_items':cart_items})

@login_required
def payment_done(request):
    user=request.user # get the current user
    custid=request.GET.get('custid')
    customer=Customer.objects.get(id=custid)
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect("orders")


@method_decorator(login_required,name='dispatch') # no profile view without login
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})
        
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user # to get the current user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            reg=Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request, 'Your profile has been updated successfully!')
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})