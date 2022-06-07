from django import forms
from .models import ShippingAddress




class CheckoutForm(forms.ModelForm):
   class Meta:
      model = ShippingAddress
      fields = ['postal_code', 'number', 'complement', 'district', 'address', 'city', 'state']

      widgets = {
            'postal_code': forms.TextInput(attrs={'onchange': 'getAddress()', 'data-mask': '00000-000'}),
      }





