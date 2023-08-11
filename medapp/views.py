from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from .models import *
from .models import ShippingAddress
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def home(request):
    return HttpResponse("This is home page")

def main(request):
    return render(request, "medapp/main.html")

def store(request):
    if request.user.is_authenticated:
      products = Products.objects.all()
      customer = request.user.customer
      order, created = Order.objects.get_or_create(customer=customer, complete=False)
      cart_tot_default = order.get_total_qty()
      context = {'products': products, 'cart_tot_default': cart_tot_default}
      return render(request, "medapp/store.html", context)
    
    else:
        return render(request, "medapp/store.html")

def cart(request):
    order_items = []
    cart_tot_default = 0

    # this checks if user is loged in
    
        # This checks if there is OneToOne relationship between "user" and "customer"
    if request.user.is_authenticated:
       customer = request.user.customer
       products = Products.objects.all()
       order, created = Order.objects.get_or_create(customer=customer, complete=False)
       cart_tot_default = order.get_total_qty()
       order_items = order.orderitem_set.all()

    else:
        order = {'get_total_qty':0,
                 'get_grand_total':0}
        

    
    context ={
        'order': order,
        'order_items':order_items,
        'cart_tot_default':cart_tot_default,
        'products':products}
    return render(request, "medapp/cart.html", context)





def checkout(request):
    if request.user.is_authenticated:
      products = Products.objects.all()
      customer = request.user.customer
      order, created = Order.objects.get_or_create(customer=customer, complete=False)

    context ={
         'order' : order
     }
    
    return render(request, "medapp/checkout.html", context)




def add_to_cart(request, product_id):
    response_data = {}  

    if request.user.is_authenticated:
        customer = request.user.customer
        product = Products.objects.get(id=product_id)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order_item, item_created = OrderItem.objects.get_or_create(order=order, product=product)

        if not item_created:
            order_item.quantity += 1
            order_item.save()

        response_data['message'] = f'"{product.name}" added to cart successfully.'
        response_data['success'] = True
        response_data['cart_total_quantity'] = order.get_total_qty()

    else:
        response_data['message'] = 'Please login to add items to the cart.'
        response_data['success'] = False

    return JsonResponse(response_data)




# We are defining this function for the purpose of updating the quantity of items by clicking the arrows 

def update_arrow_qty(request, product_id):
    response_data = {}

    if request.user.is_authenticated:
        customer = request.user.customer
        product = Products.objects.get(id=product_id)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order_item, item_created = OrderItem.objects.get_or_create(order=order, product=product)

        order_item.quantity += 1 
        order_item.save()
        # response_data['cart_total_quantity'] = order.get_total_qty()
        # cart_tot_default = order.get_total_qty()


        # response_data['message']= 'Updating Cart Items'
        # response_data['cart_total_quantity'] = order.get_total_qty()
        
    # return JsonResponse(response_data)

# ----------------------------------------------------------------------------------------------------------------------------

def downdate_arrow_qty(request, product_id):
    response_data = {}

    if request.user.is_authenticated:
        customer = request.user.customer
        product = Products.objects.get(id=product_id)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order_item, item_created = OrderItem.objects.get_or_create(order=order, product=product)

        order_item.quantity -= 1 
        order_item.save()
        # response_data['cart_total_quantity'] = order.get_total_qty()
        # cart_tot_default = order.get_total_qty()


        # response_data['message']= 'Updating Cart Items'
        # response_data['cart_total_quantity'] = order.get_total_qty()
        
    # return JsonResponse(response_data)

# -----------------------------------------------------------------------------------------------------------------------------

def shipping_address_view(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        city = request.POST.get('city')
        street = request.POST.get('street')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')

        # Save the data to the ShippingAddress model
        shipping_address = ShippingAddress.objects.create(
            address=address,
            city=city,
            street=street,
            state=state,
            zipcode=zipcode,
            customer=request.user.customer  # Assuming you have a OneToOneField between User and Customer models
        )

        # You can also perform any additional actions here, like calculating the order total and creating an Order object.

        # Redirect to a success page or wherever you need to go after the form submission.
        return redirect('store')

    return JsonResponse("Transaction is Successfull")


def signup(request):

    if request.method=="POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('conf-password')


        if User.objects.filter(username=username):
            messages.error(request, "Username alreaady exists, Please try another one")
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request, "Email already exists, Please try another Email")
            return redirect('store')
        
        if len(username)>12:
            messages.error(request, "Username Too Long")

        if len(username)<5:
            messages.error(request, "Username too short")

        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
        
        
        # This snippet of code begins the process of registering person details
        myuser = User.objects.create_user(username, email, pass1)
        myuser.save()
        # This snippet of code was to save data to backend

        messages.success(request, "Your Account Has Been Created Successfully")
        return redirect('login')
    return render(request, "medapp/signup.html")


def logingin(request):

    if request.user.is_authenticated:
        return redirect('store')
    else:

      if request.method=="POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username , password=password)
        # Django will authenticate user, and check if user exists 


        if user is not None:
            login(request, user)
            fname = user.first_name
            messages.success(request, "Logged in successfully" )
            return redirect('store')
        else:
            messages.error(request, "Sorry Incorrect Crendentials!")
            SorryDictionary={
                "SorryMssg": "Sorry Wrong Credentials"
            }
            return render(request, "authentication/signup.html", SorryDictionary)
      return render(request, "medapp/login.html")
    
def logingout(request):

    if request.user.is_authenticated:
        logout(request)
        return redirect('home')
    
    else:
        return redirect('checkout')

   
    