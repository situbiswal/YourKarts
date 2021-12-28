from django.shortcuts import render,HttpResponseRedirect,redirect,HttpResponse
from django.http import JsonResponse
from .form import SignupForm,LoginForm,ChangePasswordForm,ProfileForm
from .models import Product,Cart,Customer,OrderPlaced
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control


# Create your views here.
@cache_control(no_cache=True, must_revalidate=True)
def home(request):
    bottom_wear=Product.objects.filter(category='BW')
    top_wear=Product.objects.filter(category='TW')
    mobile=Product.objects.filter(category='M')
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    return render(request,'app/home.html',{'bottom_wears':bottom_wear,'top_wears':top_wear,'mobiles':mobile,'totalitem':totalitem })

def signup(request):
    if request.method == 'POST':
        form=SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Congratulation You Are Registred !!!!')
            
    else:
        form=SignupForm()
    return render(request,'app/signup.html',{'form':form})


def user_login(request):
    if request.method == 'POST':
        form=LoginForm(request=request,data=request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(username=username,password=password)
            messages.success(request,'Congratulation You Are logedin !!!!')
            if user is not None:
                login(request,user)
                return HttpResponseRedirect('/')
            
    else:
        form=LoginForm()
    return render(request,'app/login.html',{'form':form})



def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')

def product_details(request,pk):
    product=Product.objects.get(pk=pk)
    item_alredy_in_cart = False
    if request.user.is_authenticated:
        item_alredy_in_cart=Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
    return render(request,'app/product_details.html',{'products':product,'item_alredy_in_cart':item_alredy_in_cart})


def mobile(request,data=None):
    if data == None:
        mobile=Product.objects.filter(category='M')
    elif data == 'realme' or  data == 'samsung' or  data == 'mi' or  data == 2:
        mobile=Product.objects.filter(category='M').filter(brand=data)
    elif data == "above":
        mobile=Product.objects.filter(category='M').filter(discount_price__gt=15000)
    elif data == "below":
        mobile=Product.objects.filter(category='M').filter(discount_price__lt=15000)      
    return render(request,'avpp/allmobile.html',{'mobiles':mobile}) 


def men(request,data=None):
    if data == None:
        mens=Product.objects.filter(category='BW')
    if data == 'topwear':
        mens=Product.objects.filter(category='TW')
    return render(request,'app/mens.html',{'mens':mens})


def change_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form=ChangePasswordForm(user=request.user,data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request,form.user)
                messages.success(request,'Congratulation You Are Password is Successfull Change !!!!')
                return render(request,'app/change_successfull.html')
        else:
            form=ChangePasswordForm(user=request.user)
        return render(request,'app/change_password.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

def profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form=ProfileForm(request.POST)
            if form.is_valid():
                user=request.user
                name=form.cleaned_data['name']
                locality=form.cleaned_data['locality']
                city=form.cleaned_data['city']
                state=form.cleaned_data['state']
                zipcode=form.cleaned_data['zipcode']
                reg=Customer(user=user,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
                reg.save()
                form=ProfileForm()
        else:
            form=ProfileForm()
        return render(request,'app/profile.html',{'form':form,'primary':'btn-primary'})
    else:
        return HttpResponseRedirect('/login/')


def address(request):
    if request.user.is_authenticated:
        user=request.user
        form=Customer.objects.filter(user=user)
        return render(request,'app/address.html',{'form':form,'primary':'btn-primary'}) 
    else:
        return HttpResponseRedirect('/login/')       


def add_to_cart(request):
    if request.user.is_authenticated:
        user=request.user
        prod_id=request.GET.get('product_id')
        product=Product.objects.get(id=prod_id)
        reg=Cart(user=user,product=product)
        reg.save()
        return redirect('/cart/')
    else:
        return HttpResponseRedirect('/login/')     
    

def cart(request):
    if request.user.is_authenticated:
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0.0
        shipping_amount=70.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==user]
        if cart_product:
            for p in cart_product:
                tempamount=p.quantity*p.product.discount_price
                amount +=tempamount
                totalamount=amount+shipping_amount

            return render(request,'app/cart.html',{'carts':cart,'amount':amount,'totalamount':totalamount})

        else:
            return render(request,'app/empty.html')    
    else:
        return HttpResponseRedirect('/login/')        

def plus_cart(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            product_id=request.GET.get('prod_id')
            
            c=Cart.objects.get(Q(product=product_id) & Q(user=request.user))
            c.quantity +=1
            c.save()
            amount=0.0
            shippingamount=70.0
            cart_product=[p for p in Cart.objects.all() if p.user==request.user]
            for p in cart_product:
                tempamount=p.quantity*p.product.discount_price
                amount +=tempamount
                
                data={
                    'quantity':c.quantity,
                    'amount':amount,
                    'totalamount':amount+shippingamount
                }
            return JsonResponse(data)
    else:
        return HttpResponseRedirect('/login/')      


def minus_cart(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            product_id=request.GET.get('prod_id')
            print(product_id)
            c=Cart.objects.get(Q(product=product_id)  &  Q(user=request.user))
            c.quantity -=1
            c.save()
            amount=0.0
            shippingamount=70.0
            cart_product=[p for p in Cart.objects.all() if p.user==request.user]
            for p in cart_product:
                tempamount=p.quantity*p.product.discount_price
                amount +=tempamount
            
                data={
                    'quantity':c.quantity,
                    'amount':amount,
                    'totalamount':amount+shippingamount
                }
            return JsonResponse(data)
    else:
        return HttpResponseRedirect('/login/')       

def remove(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            product_id=request.GET.get('prod_id')
            print(product_id)
            c=Cart.objects.get(Q(product=product_id) & Q(user=request.user))
            c.delete()
            amount=0.0
            shippingamount=70.0
            product_cart=[p for p in Cart.objects.all() if p.user == request.user]
            for p in product_cart:
                tempamount=p.quantity*p.product.discount_price
                amount +=tempamount
            
                data={
                    
                    'amount':amount,
                    'totalamount':amount+shippingamount
                }
            return JsonResponse(data)
    else:
        return HttpResponseRedirect('/login/')         


def placeorder(request):
    if request.user.is_authenticated:
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_item=Cart.objects.filter(user=user)
        amount=0.0
        shippingamount=70.0
        totalamount=0.0
        product_cart_item=[p for p in Cart.objects.all() if p.user==request.user]
        if product_cart_item:
            for p in product_cart_item:
                tempamount=p.quantity*p.product.discount_price
                amount +=tempamount
            totalamount=amount+shippingamount
            
        return render(request,'app/placeorder.html',{'add':add,'totalamount':totalamount,'cart_item':cart_item})
    else:
        return HttpResponseRedirect('/login/') 



def payment(request):
    if request.user.is_authenticated:
        user=request.user
        address=request.GET.get('Select_Address')
        customer=Customer.objects.get(id=address)
        cart=Cart.objects.filter(user=user)
        for c in cart:
            OrderPlaced(user=user,customer=customer,quantity=c.quantity,product=c.product).save()
            c.delete()
    
        return render(request,'app/transcation_complete.html')
    else:
        return HttpResponseRedirect('/login/') 
    


    
def order_status(request):
    if request.user.is_authenticated:
        user=request.user
        op=OrderPlaced.objects.filter(user=user)
        return render(request,'app/order_status.html',{'op':op})
    else:
        return HttpResponseRedirect('/login/')     



def passw(request):
    return render(request,'app/transcation_complete.html')