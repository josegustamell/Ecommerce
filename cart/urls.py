from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_summary, name='cart_summary'),
    path('add/', views.add_to_cart, name='add_to_cart'),
]