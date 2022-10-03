from django.contrib import admin
from .models import Category, Product, ProductImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class ProductImageAdmin(admin.StackedInline):
    model = ProductImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]

    class Meta:
       model = Product
       list_display = ['name', 'category', 'slug', 'price','size', 'sold', 'available']
    
    prepopulated_fields = {'slug': ('name',)}
    

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass


