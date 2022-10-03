import re
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .cart import Cart
from store.models import Product

def cart_summary(request):
    
    context = {}
    return render(request, 'cart/cart.html', context)


def add_to_cart(request):
    cart = Cart(request)    
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_quantity = request.POST.get('productquantity')
        product_size = str(request.POST.get('productsize'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, product_quantity=product_quantity, product_size=product_size)
        cart_quantity = cart.__len__()
        response = JsonResponse({'quantity': cart_quantity})
        return response 
