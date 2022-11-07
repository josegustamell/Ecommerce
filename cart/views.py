from django.shortcuts import redirect, render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.contrib import messages


def cart_summary(request):
    cart = Cart(request)
    context = {'cart': cart}
    return render(request, 'cart/cart.html', context)


def add_to_cart(request):
    cart = Cart(request)    
    if request.method == 'POST':       
        product_id = int(request.POST.get('productid'))
        product_quantity = int(request.POST.get('product-quantity'))
        product_size = str(request.POST.get('sizes'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, product_quantity=product_quantity, product_size=product_size)
        return render(request, 'cart/partials/cart-quantity.html')


def add_quantity(request):
    cart = Cart(request)
    if request.method == 'POST':
        product_id = request.POST.get('productid')
        cart.add_quantity(product_id=product_id)
        quantity = cart.get_item(product_id=product_id)['quantity']
        product = get_object_or_404(Product, id=product_id)

        item = {
            'product': {
                'id': product.id,
                'name': product.name,
                'image': product.image,
                'price': product.price,

            },
            'total_price': quantity * product.price,
            'quantity': quantity,
        }
        context = {'item': item}
        response = render(request, 'cart/partials/cart-item.html', context)
        response['HX-Trigger'] = 'update-cart-quantity'
        
        return response


def remove_quantity(request):
    cart = Cart(request)
    if request.method == 'POST':
        product_id = request.POST.get('productid')
        cart.remove_quantity(product_id=product_id)
        quantity = cart.get_item(product_id=product_id)['quantity']
        product = get_object_or_404(Product, id=product_id)

        item = {
            'product': {
                'id': product.id,
                'name': product.name,
                'image': product.image,
                'price': product.price,

            },
            'total_price': quantity * product.price,
            'quantity': quantity,
        }
        context = {'item': item}
        response = render(request, 'cart/partials/cart-item.html', context)
        response['HX-Trigger'] = 'update-cart-quantity'
        
        return response

def delete(request):
    cart = Cart(request)
    if request.method == 'POST':
        product_id = request.POST.get('productid')
        print(product_id)
        cart.delete(product_id=product_id)
        response = render(request, 'cart/partials/item-deleted.html')
        response['HX-Trigger'] = 'update-cart-quantity'
        
        return response


def hx_cart_quantity(request):
    return render(request, 'cart/partials/cart-quantity.html')


def hx_cart_total_price(request):
    return render(request, 'cart/partials/cart-total-price.html')