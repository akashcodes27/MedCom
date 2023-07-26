from django.db import models
from django.contrib.auth.models import User 


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE ,null=True, blank=True)
    name = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, null=True)
    

    def __str__ (self):
        return self.name
    
class Products(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url=""

        return url 
    

    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_orderred = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    #    If this is False, implies cart is not yet full, if True, then carts capacity is full
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)
    

    def get_grand_total(self):
        order_items = self.orderitem_set.all()
        grandtotal = sum([itemss.get_total for itemss in order_items])
        return grandtotal 
    # Order.orderitems_set.all() creates an object "order_items" by considering all order items 
    # In this case we are using self, because we are defining the function inside the Order model itself 
    # we create a list containing as many values as many orderitems there are. Every value inside list will be the total price of each orderitem(considering qty * price). 
    # We then take a sum of all values in list to get a grand total price
    # Similarly we will define a function which gives us grand total for quantity

    def get_total_qty(self):
        order_items = self.orderitem_set.all()
        qtytotal = sum([itemms.quantity for itemms in order_items])
        return qtytotal 
    
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    # we will now define a function to retrieve the total amount associated with the items bought
    # The reason why we define the function in here is because we need "quantity" 


    def __str__(self):
        return str(self.product.name)

    @property
    def get_total(self):
        totalprice = self.product.price * self.quantity
        return totalprice 
 

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=100, null=False)
    city = models.CharField(max_length=100, null=False)
    state = models.CharField(max_length=100, null=False)
    zipcode = models.CharField(max_length=100, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


# After you have clearly defined the models and their attributes, run "makemigrations" in cmd
# This generates a 0001init file inside migrations folder
# We will use the default sqlite database to store data.
# But remember we also need to gain access of it from the admin pannel in the future.