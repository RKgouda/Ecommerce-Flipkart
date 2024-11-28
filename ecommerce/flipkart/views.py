from django.shortcuts import render,redirect,HttpResponse


# Create your views here.
from .models import *
from django.contrib.auth.hashers import check_password,make_password
from django.shortcuts import get_object_or_404

def index(request):
    if request.method == 'POST':
        product_id = request.POST.get('productid')
        remove = request.POST.get('remove')
        print("product_id-----------", product_id)

        cart_id = request.session.get('cart')
        print("cart_id-----------", cart_id)
        if cart_id:
            quantity = cart_id.get(product_id)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart_id.pop(product_id)
                    else:
                        cart_id[product_id] = quantity -1
                else:
                    cart_id[product_id] = quantity +1
            else:
                cart_id[product_id] = 1
        else:
            cart_id = {}
            cart_id[product_id] = 1
        request.session['cart'] = cart_id
        print("request.session[cart]-----------", request.session['cart'])

    category_obj = Category.objects.all()
    
    category_id = request.GET.get("category_id")
    search = request.GET.get("search")

    if category_id:
        product_obj = Product.objects.filter(product_category=category_id)
    elif search:
        product_obj = Product.objects.filter(product_name__icontains=search)
    else:
        product_obj = Product.objects.all()

    context = {
        "category": category_obj,
        "product": product_obj
    }
    return render(request, 'home.html',context=context)

def contact(request):
    context = {

    }
    return render(request, 'contact.html',context=context)

def about(request):
    context = {

    }
    return render(request, 'about.html',context=context)

def validateCustomer(customer):
    error_messagge = None
    if (not customer.first_name):
        error_messagge = "Please Enter your First Name !!"
    elif len(customer.first_name) < 3:
        error_messagge = "First Name must be 3 Charater long or more"
    elif not customer.last_name:
        error_messagge = "Please Enter your Last Name"
    elif len(customer.last_name) < 3:
        error_messagge = "Last Name must be 3 Charater long or more"
    elif not customer.phone:
        error_messagge = "Please Enter your Phone Number"
    elif len(customer.phone) < 10:
        error_messagge = "Phone Number must be 10 disite long"
    elif len(customer.password) < 5:
        error_messagge = "Password must be 5 character long"
    elif len(customer.email) < 5:
        error_messagge = "Email Address must be 5 character long"
    elif customer.isExists():
        error_messagge = "Email Address already registered"
    return error_messagge


def sign_up(request):
    if request.method == 'POST':
        f_name = request.POST.get('fname')
        l_name = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('pwd')
        mobile = request.POST.get('mbl')
        gender = request.POST.get('gender')

        # validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'mobile': mobile,
            'email': email,
            'gender': gender
        }
        print(value)
        error_message = None

        customer = Registration(
            first_name=f_name,
            last_name=l_name,
            email=email,
            password=password,
            mobile=mobile,
            gender=gender)
        error_message = validateCustomer(customer)

        if not error_message:
            print(first_name, last_name, mobile, email, password, gender)
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('home')
        else:

            data = {
                'error': error_message,
                'values': value,
                'category_obj': contents.get('category_obj'),
                'product_obj': contest.get('product_obj')
            }
            return render(request, 'home.html', data)

        # reg_obj = Registration(
        #     first_name=f_name,
        #     last_name=l_name,
        #     email=email,
        #     password=make_password(password),
        #     mobile=mobile,
        #     gender=gender
        # )

        # reg_obj.save()

        # return redirect('home')

def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        email_id = Registration.objects.get(email=email)
        try:
            if check_password(password,email_id.password):
                request.session['name'] = email_id.first_name
                request.session['customer_id'] = email_id.id
                return redirect('home')
            else:
                return HttpResponse("Wrong password")
        except:
            return HttpResponse("Wrong Email")

def logout(request):
    request.session.clear()
    return redirect('home')


def cart_details(request):

    cart_id = list(request.session.get('cart').keys())
    product = Product.objects.filter(id__in = cart_id)

    context = {
        'product': product
    }
    return render(request,'cart.html',context=context)

def checkout(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        customer_id = request.session.get('customer_id')
        if not customer_id:
            return HttpResponse("Please Login")
        
        cart_id = request.session.get('cart')

        product = Product.objects.filter(id__in = list(cart_id.keys()))

        for pro in product:
            order_obj = Order (
                address = address,
                mobile = mobile,
                customer = Registration(id=customer_id),
                price = pro.product_price,
                product = pro,
                quantity = cart_id.get(str(pro.id))

            )
            order_obj.save()
        return redirect('order')
    
# Delete-------------
def delete_order(request, order_id):
    # Ensure the user is authenticated
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('login')

    order = get_object_or_404(Order, id=order_id, customer_id=customer_id)
    order.delete()

    return redirect('order') 
    
def order_details(request):
    customer_id = request.session.get('customer_id')

    order = Order.objects.filter(customer=customer_id)
    tp = 0
    for i in order:
        tp = tp + (i.price * i.quantity)

    context = {
        'order': order,
        'tp': tp,
    }
    return render(request,'order.html',context=context)


from rest_framework import viewsets
from .serializers import RegistrationSerializer

class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer







