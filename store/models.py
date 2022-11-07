from contextlib import nullcontext
from tabnanny import verbose
from django.db import models
from django.urls import reverse



SIZE_CHOICES = [
    ('PP', 'PP'),
    ('P', 'P'),
    ('M', 'M'),
    ('G', 'G'),
    ('GG', 'GG')
]



class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Categoria')
    slug = models.SlugField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.FloatField()
    slug = models.SlugField(max_length=255)
    size = models.CharField(max_length=2, choices=SIZE_CHOICES, blank=True, null=True)
    image = models.ImageField(blank=True)
    description = models.TextField(blank=True)
    sold = models.IntegerField(default=0)
    available = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True,)

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])
    
    def __str__(self):
        return self.name
        

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')




