from django import forms
from accounts.models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['user', 'created', 'updated']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'name'}),
            'CEP': forms.TextInput(attrs={'class': 'form-control', 'id': 'cep'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'id': 'address'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
            'default': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'default-check'})
        }