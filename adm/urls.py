from django.urls import path
from . import views


app_name = 'adm'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('products/', views.products, name='products'), # Mudar o nome pra all-products
    path('new-product/', views.new_product, name='new_product'),
    path('edit-product/<slug:slug>', views.edit_product, name='edit_product'),
    path('admin-orders/', views.admin_orders, name='admin_orders'),
    path('order/<int:pk>', views.single_order, name='single_order'), # Tentar achar um nome melhor pra essa url, single_order é paia demais kkkkkk
    path('orders-delivered/', views.orders_delivered, name='orders_delivered'),
    path('orders-undelivered/', views.orders_undelivered, name='orders_undelivered')

]