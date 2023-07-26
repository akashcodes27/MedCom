from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .models import *

def home(request):
    return HttpResponse("This is home page")

def main(request):
    return render(request, "medapp/main.html")

def store(request):
    products = Products.objects.all()
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    cart_tot_default = order.get_total_qty()
    context = {'products': products, 'cart_tot_default': cart_tot_default}
    return render(request, "medapp/store.html", context)

def cart(request):
    order_items = []

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
    return render(request, "medapp/checkout.html")




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