from django import forms
from .models import ShippingAddress
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CheckoutForm(forms.ModelForm):
   class Meta:
      model = ShippingAddress
      fields = ['postal_code', 'number', 'complement', 'district', 'address', 'city', 'state']

      widgets = {
            'postal_code': forms.TextInput(attrs={'onchange': 'getAddress()', 'data-mask': '00000-000'}),
      }


class CreateUserForm(UserCreationForm):
      class Meta:
            model = User
            fields = ['username', 'email', 'password1', 'password2']
            


