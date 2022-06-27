from importlib.metadata import metadata
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import Settings, settings
from adm.decorators import unauthenticated_user
from .models import *
from .forms import CheckoutForm, CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid:
            user = form.save()
            group = Group.objects.get(name='customer')
            user.groups.add(group)

            return redirect('store:login')
        else:
            messages.info(request, 'Some error in validation. Please try again.')
    context = {'form': form}
    return render(request, 'store/register.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('store:store')
        else:
            messages.info(request, 'Username OR Password is incorrect.')
    return render(request, 'store/login.html')


def logoutUser(request):
    logout(request)
    return redirect('store:login')


def store(request):
    products = Product.objects.all()
    user = request.user.id
    context = {'products': products, 'user': user}
    return render(request, 'store/store.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    context = {'product': product}
    return render(request, 'store/product.html', context)

#for order_item in order.products.all():
        #order_items.append(order_item.product.name)
        #items = ', '.join(order_items)


@login_required(login_url='store:login')
def cart(request):
    try:
        order = Order.objects.get(user=request.user, complete=False)
        
    except Order.DoesNotExist:
        return render(request, 'store/empty_cart.html')

    context = {'order': order}
    return render(request, 'store/cart.html', context)


@login_required(login_url='store:login')
def add_to_cart(request, slug):  # Tentar deixar mais organizada esses if e else do order_qs.exists. Botar pra criar primeiro se não existir seria bem melhor e mais "código limpo"
    previous_url = request.META.get('HTTP_REFERER')
    host = request.get_host()
    product = get_object_or_404(Product, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, complete=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, 'This item quantity was updated')
        else:
            name = order_item.product.name 
            order.products.add(order_item)
            messages.info(request, f'{name} was added to your cart')
    else:
        order = Order.objects.create(user=request.user)
        order.products.add(order_item)
        messages.info(request, 'This item was added to your cart')

    if previous_url == (f'http://{host}/'):  # The url of your page
        return redirect('store:store')  #
    else:
        return redirect('store:product', slug=slug)


@login_required(login_url='store:login')
def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_item = OrderItem.objects.get(
        product=product,
        user=request.user,
        ordered=False
    )
    order = Order.objects.get(user=request.user, complete=False)

    order.products.remove(order_item)
    order_item.delete()
    messages.info(request, 'Item removed from your cart.')
    return redirect('store:cart')


@login_required(login_url='store:login')
def remove_single_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_item = OrderItem.objects.get(
        product=product,
        user=request.user,
        ordered=False,
    )
    order = Order.objects.get(user=request.user, complete=False)
    if order_item.quantity > 1:
        order_item.quantity -= 1
        order_item.save()
        messages.info(request, 'This item quantity was updated.')
        return redirect('store:cart')
    else:
        order.products.remove(order_item)
        order_item.delete()
        messages.info(request, 'Item removed from your cart.')
        return redirect('store:cart')


@login_required(login_url='store:login')
def add_product_in_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_item = OrderItem.objects.get(
        product=product,
        user=request.user,
        ordered=False,
    )
    order_item.quantity += 1
    order_item.save()
    messages.info(request, 'This item quantity was updated.')
    return redirect('store:cart')


@login_required(login_url='store:login') 
def define_address(request):
    order = Order.objects.get(user=request.user, complete=False)
    if order.products.all().count() == 0:
        messages.warning(request, 'You do not have items in your cart. Try add new items.')
        return redirect('store:store')
        
    form = CheckoutForm()
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        order = Order.objects.get(user=request.user, complete=False)
        if form.is_valid():
            postal_code = form.cleaned_data.get('postal_code')
            number = form.cleaned_data.get('number')
            complement = form.cleaned_data.get('complement')
            district = form.cleaned_data.get('district')
            address = form.cleaned_data.get('address')
            city = form.cleaned_data.get('city')
            state = form.cleaned_data.get('state')

            shipping_address = ShippingAddress(
                user=request.user,
                postal_code=postal_code,
                number=number,
                complement=complement,
                district=district,
                address=address,
                city=city,
                state=state,
            )
            shipping_address.save()
            order.shipping_address = shipping_address
            order.save()
            return redirect('store:create_checkout')
    context = {'form': form}
    return render(request, 'store/checkout.html', context)


@login_required(login_url='store:login')
def create_checkout(request):  # Essa view nada mais faz do que criar as informações para o pagamento pelo stripe. Só isso, ela não lida diretamente COM O PAGAMENTO EM SI, mas só com as informações que vão pra ele.
    order = Order.objects.get(user=request.user, complete=False)
    amount = order.get_total()
    host = request.get_host()
    order_items = []
    
    for order_item in order.products.all():
        order_items.append(order_item.product.name)
        items = ', '.join(order_items)
    
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
         line_items=[
             {
                 'amount': amount * 100,
                 'currency': 'brl',
                 'quantity': 1,
                 'name': items,
                 'images': ['https://img.cancaonova.com/cnimages/canais/uploads/sites/2/2021/12/santododia-Nossa-Senhora-de-Guadalupe.jpg'], # Colocar a imagem do primeiro produto que foi adicionado ao carrinho, ou algo mais ou menos assim. Ou só uma imagem de qualquer produto mesmo. Ver vídeo do Very Academy
             }
         ],
        metadata={'client_reference_id': request.user.id},
        mode='payment',
        success_url=(f'http://{host}{reverse("store:sucess")}'),
        cancel_url=(f'https://{host}{reverse("store:cancel")}'),
    )
    return redirect(checkout_session.url, code=303)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user_id = session['metadata']['client_reference_id']
        user = User.objects.get(id=user_id)
        order = Order.objects.get(user=user, complete=False)
        order_items = order.products.all()
                    
        order_items.update(ordered=True)  # O método do .update serve pra quando eu quero colocar um valor específico pra um campo em todos os objetos do meu queryset
        
        for item in order_items:
            item.product.sold += item.quantity
            item.product.save()
            item.save()

        order.complete = True
        order.save()
    
    return HttpResponse(status=200)


@login_required(login_url='store:login')
def sucess(request):
    return render(request, 'store/sucess.html')


@login_required(login_url='store:login')
def cancel(request):  # Ver o que essa view de cancel deveria fazer e organiza-la. Talvez tenha algo a ver com o tratamento de erros e webhooks.
    return render(request, 'store/cancel.html')


@login_required(login_url='store:login')
def orders_completed(request):
    orders = Order.objects.filter(user=request.user, complete=True)
    context = {'orders': orders}
    return render(request, 'store/orders_completed.html', context)


@login_required(login_url='store:login')
def detail_order_completed(request, pk):
    order = Order.objects.get(id=pk)
    products = order.products.all()
    context = {'order': order, 'products': products}
    return render(request, 'store/detail_order_completed.html', context)

