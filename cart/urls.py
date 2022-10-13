from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_summary, name='cart_summary'),
    path('add/', views.add_to_cart, name='add_to_cart'),
    path('add-quantity/', views.add_quantity, name='add_quantity'),
    path('remove-quantity/', views.remove_quantity, name='remove_quantity'),
    path('delete/', views.delete, name='delete'),
    

]

htmxpatterns = [
    path('hx_cart_quantity', views.hx_cart_quantity, name='hx_cart_quantity'),
    path('hx_cart_total_price', views.hx_cart_total_price, name='hx_cart_total_price'),

]

urlpatterns += htmxpatterns