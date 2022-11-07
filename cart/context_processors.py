from .cart import Cart
from store.models import Category

def cart(request):
    return {'cart': Cart(request)}
