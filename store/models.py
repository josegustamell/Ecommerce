from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from localflavor.br.models import BRPostalCodeField

class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):  # The product itself
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    slug = models.SlugField(null=True, unique=True)
    # description = models.TextField()

    def get_add_to_cart(self):
        # Reverse is to find an url, Redirect is just a redirect to url
        return reverse('add-to-cart', args=[self.slug])

    def get_remove_from_cart(self):
        return reverse('remove-from-cart', args=[self.slug])

    def get_absolute_url(self):
        return reverse('product', args=[self.slug])

    def __str__(self):
        return self.name


class OrderItem(models.Model):  # Items inside my cart
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    def get_total_product_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f'{self.quantity} of {self.product.name}'


class ShippingAddress(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    postal_code = BRPostalCodeField('CEP', default='')
    number = models.CharField(max_length=250, null=False, default='')
    complement = models.CharField(max_length=255, blank=True)
    district = models.CharField(max_length=255, null=False, default='')
    address = models.CharField(max_length=250, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    

    def __str__(self):
        return self.address


class Order(models.Model):  # Cart
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    products = models.ManyToManyField(OrderItem)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200, null=True)
    shipping_address = models.ForeignKey(
        ShippingAddress, on_delete=models.SET_NULL, blank=True, null=True)

    def get_total(self):
        total = 0
        for order_item in self.products.all():
            total += order_item.get_total_product_price()
        return total

    def get_number_of_products(self):
        total = 0
        for order_item in self.products.all():
            total += order_item.quantity
        return total

    def get_absolute_url(self):
        return reverse('cart')

    def __str__(self):
        return str(self.id)
