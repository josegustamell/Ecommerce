from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('product/<slug:slug>/', views.product_detail, name='product'),
    path('add-to-cart/<slug:slug>/', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug:slug>/', views.remove_from_cart, name='remove-from-cart'),
    path('cart/', views.cart, name='cart'),
    path('remove-single-product/<slug:slug>/', views.remove_single_product, name='remove-single-product'),
    path('add-product-in-cart/<slug:slug>', views.add_product_in_cart, name='add-product-in-cart'),
    path('address/', views.define_address, name='address'),
    path('create-checkout/', views.create_checkout, name='create_checkout'),
    path('sucess/', views.sucess, name='sucess'),
    path('cancel/', views.cancel, name='cancel'),
    path('orders-completed/', views.orders_completed, name='orders_completed'),
    path('detail-order/<int:pk>', views.detail_order_completed, name='detail_order')
]