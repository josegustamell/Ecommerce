from ast import Or
from django.contrib import admin
from .models import *

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'slug']
    prepopulated_fields = {'slug': ('name', )}



