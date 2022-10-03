class Cart():

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if 'cart' not in request.session:
            cart = self.session['cart'] = {}
        self.cart = cart # built just the sessions

    def add(self, product, product_quantity, product_size):
        product_id = product.id

        if product_id not in self.cart:
            self.cart[product_id] = {'price': str(product.price), 'quantity': int(product_quantity), 'size': str(product_size)}
        
        self.session.modified = True

    def __len__(self):
        
        return sum(item['quantity'] for item in self.cart.values())
    
         