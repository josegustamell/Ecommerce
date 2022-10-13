from decimal import Decimal
from store.models import Product


class Cart():

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if 'cart' not in request.session:
            cart = self.session['cart'] = {}
        self.cart = cart 

    def __len__(self):  
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        products_ids = self.cart.keys()
        products = Product.objects.filter(id__in=products_ids, available=True)
        cart = self.cart.copy() 

        for product in products:           
            cart[str(product.id)]['product'] = product
            
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def add(self, product, product_quantity, product_size):
            product_id = str(product.id)

            if product_id not in self.cart:
                self.cart[product_id] = {'price': str(product.price), 'quantity': int(product_quantity), 'size': str(product_size)}
            else:
                self.cart[product_id]['quantity'] += product_quantity
                self.cart[product_id]['size'] += ', ' + product_size
            
            self.save()

    def add_quantity(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] += 1
            self.save()
    
    def remove_quantity(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] -= 1
            self.save()

    def delete(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def get_total_price(self):
        return sum(Decimal(item['price']) * int(item['quantity']) for item in self.cart.values())

    def get_item(self, product_id):
        product_id = str(product_id)
        return self.cart[product_id]
    
    def save(self):
        self.session.modified = True


