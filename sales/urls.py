# apps/sales/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.view_cart, name='view_cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_confirmation/<int:sale_id>/', views.order_confirmation, name='order_confirmation'),
    path('download_receipt/<int:sale_id>/', views.download_receipt, name='download_receipt'),

]
