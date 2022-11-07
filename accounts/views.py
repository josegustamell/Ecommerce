from django.shortcuts import redirect, render
from .forms import *
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from store.models import Product


def account_register(request):
    register_form = RegisterForm()

    if request.user.is_authenticated:
        return redirect('store:store')
    
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.set_password(register_form.cleaned_data['password'])
            user.save()
            return redirect('store:store')

    context = {'form': register_form}
    return render(request, 'accounts/registration/register.html', context)


def account_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        if user is not None:    
            login(request, user=user)
            return redirect('store:store')
        else:
            messages.error(request, 'Email ou senha inválidos.')
    
    return render(request, 'accounts/registration/login.html')


def account_dashboard(request):
    user = request.user
    context = {'user': user}
    return render(request, 'accounts/user/dashboard.html', context)


def account_orders(request):
    if request.user.is_authenticated:
        products = Product.objects.all()
        context = {'products': products}
        return render(request, 'accounts/user/account-orders.html', context)
    else:
        messages.warning(request, 'Você deve estar autenticado para acessar esta página.')
        return redirect('accounts:account_register')


def account_detail(request):
    if request.user.is_authenticated:
        products = Product.objects.all()
        context = {'products': products}
        return render(request, 'accounts/user/account-detail.html', context)
    else:
        messages.warning(request, 'Você deve estar autenticado para acessar esta página.')
        return redirect('accounts:account_register')



        
