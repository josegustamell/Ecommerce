from django import forms
from .models import MyUser, Address

 
class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)
    
    class Meta:
        model = MyUser
        fields = ('email', 'name', 'cpf', 'phone', 'gender', 'birth_date')



