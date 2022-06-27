from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .decorators import allowed_users
from .forms import ProductEdit, NewProduct
from django.utils.text import slugify
from store.models import *


@allowed_users(allowed_roles=['admin'])
def home(request):
    last_five_orders = Order.objects.all().order_by('-date_ordered')[0:5]
    top_selling_products = Product.objects.all().order_by('-sold')[0:5]
    total_orders = Order.objects.all().count()
    delivered_orders = Order.objects.filter(delivered=True).count()
    undelivered_orders = Order.objects.filter(delivered=False).count()

    context = {
        'last_five_orders': last_five_orders,  
        'top_selling_products': top_selling_products, 
        'total_orders': total_orders,
        'delivered_orders': delivered_orders, 
        'undelivered_orders': undelivered_orders
        }
    return render(request, 'adm/home.html', context)


@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()

    return render(request, 'adm/products.html', context={'products': products})


def new_product(request):
    form = NewProduct()
    
    if request.method == 'POST':
        form = NewProduct(request.POST)
        if form.is_valid():
            product = form.save(commit=False)  # Commit eu salvo meu formulário, mas não salvo no banco de dados, sacou?
            product.slug = slugify(product.name)
            product.save()
            return redirect('adm:home')
    
    context = {'form': form}
    return render(request, 'adm/new_product.html', context)



@allowed_users(allowed_roles=['admin'])
def edit_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    form = ProductEdit(instance=product)

    if request.method == 'POST':
        form = ProductEdit(request.POST, instance=product)
        if form.is_valid():
            product_edited = form.save(commit=False)
            product_edited.slug = slugify(product_edited.name)
            product_edited.save()
            return redirect('adm:products')

    context = {'product': product, 'form': form,}
    return render(request, 'adm/edit_product.html', context)


@allowed_users(allowed_roles=['admin'])
def admin_orders(request):
    orders = Order.objects.all()
    
    return render(request, 'adm/orders.html', context={'orders': orders})


@allowed_users(allowed_roles=['admin'])
def single_order(request, pk): # Tentar fazer um raw form disso, já que é incrivelmentwe simples
    order = get_object_or_404(Order, id=pk)
    
    if request.method == 'POST':
        if 'checkbox-true' in request.POST:
            order.delivered = True
            order.save()
            return redirect('adm:orders_delivered')
        else:
            order.delivered = False
            order.save()
            return redirect('adm:orders_undelivered')

    context = {'order': order}
    return render(request, 'adm/single_order.html', context)


@allowed_users(allowed_roles=['admin'])
def orders_delivered(request):
    orders = Order.objects.filter(delivered=True)
    return render(request, 'adm/orders_undelivered.html', {'orders': orders})
    

@allowed_users(allowed_roles=['admin'])
def orders_undelivered(request):
    orders = Order.objects.filter(delivered=False)
    return render(request, 'adm/orders_undelivered.html', context={'orders': orders})


def user_information(request, pk):
    user = User.objects.get(id=pk)
    return render(request, 'user_information.html', context={'user': user})