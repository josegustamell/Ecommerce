from tkinter import Widget
from django import forms
from store.models import Product, Order


class ProductEdit(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'available', 'category']
        


class NewProduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'available', 'category']
        

    