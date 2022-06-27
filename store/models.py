from secrets import choice
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from localflavor.br.models import BRPostalCodeField, BRCPFField
from django.utils.text import slugify


class Product(models.Model):  
    CATEGORY_CHOICES = (
    ('T', 'Terço'),
    ('L', 'Livro'),
    ('E', 'Estatua')
    )
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    slug = models.SlugField(null=True, unique=True)
    description = models.TextField(blank=True)
    available = models.BooleanField(default=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=1, null=True)
    sold = models.IntegerField(default=0)

    def get_add_to_cart(self):
        # Reverse is to find an url, Redirect is just a redirect to url
        return reverse('store:add-to-cart', args=[self.slug])

    def get_remove_from_cart(self):
        return reverse('store:remove-from-cart', args=[self.slug])

    def get_absolute_url(self):
        return reverse('store:product', args=[self.slug])

    def get_total_sold(self):
        return self.sold

    def __str__(self):
        return self.name


class OrderItem(models.Model):  # Items inside my cart, o Product só se transforma em OrderItem, o OrderItem é classe filho que herda todos os atributos (e até métodos?) da classe pai Product.
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def get_total_product_price(self):
        return self.quantity * self.product.price


    def __str__(self):
        return f'{self.quantity} of {self.product.name}'


class ShippingAddress(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    postal_code = BRPostalCodeField('CEP')
    number = models.CharField(max_length=250, null=False)
    complement = models.CharField(max_length=255, blank=True)
    district = models.CharField(max_length=255, null=False)
    address = models.CharField(max_length=250, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    

    def __str__(self):
        return self.address


class Order(models.Model):  # Cart
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    shipping_address = models.ForeignKey(
        ShippingAddress, on_delete=models.SET_NULL, blank=True, null=True)
    products = models.ManyToManyField(OrderItem)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    ref_code = models.CharField(max_length=20, null=True, blank=True)
    delivered = models.BooleanField(default=False)
    

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
        return reverse('store:cart')

    def __str__(self):
        return str(self.id)
