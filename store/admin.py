from ast import Or
from django.contrib import admin
from .models import *

admin.site.register(Customer)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'slug']
    prepopulated_fields = {'slug': ('name', )}



admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
