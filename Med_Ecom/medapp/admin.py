from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Customer)
admin.site.register(Products)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)

# We will create a superuser and then we will access django admin pannel
# This will allow us to add or delete products, and changes will accordingly reflect in the ddatabse.
# We havent yet worked on the part where changes also reflect on the frontend of the application 
# Django admin will directly allow us perform CRUD 

