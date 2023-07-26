from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.main, name="home"),
    path("main", views.main, name="main"),
    path("store", views.store, name="store"),
    path("cart", views.cart, name="cart"),
    path("checkout", views.checkout, name="checkout"),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update_arrow_qty/<int:product_id>/', views.update_arrow_qty, name='update_arrow_qty'),
    path('downdate_arrow_qty/<int:product_id>/', views.downdate_arrow_qty, name='downdate_arrow_qty')
]
