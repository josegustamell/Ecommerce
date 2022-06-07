from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.conf import Settings, settings
from .models import *
from .forms import CheckoutForm
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


def store(request):
    products = Product.objects.all()

    context = {'products': products}
    return render(request, 'store/store.html', context)


def product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    
    url = request.META.get('HTTP_REFERER')
    urls = url[:10]
    context = {'product': product, 'url': urls}
    return render(request, 'store/product.html', context)


def cart(request):
    try:
        order = Order.objects.get(user=request.user, complete=False)
        
    except:
        return render(request, 'store/empty_cart.html')

    context = {'order': order}
    return render(request, 'store/cart.html', context)


def add_to_cart(request, slug):
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
            order.products.add(order_item)
            messages.info(request, 'This item was added to your cart')
    else:
        order = Order.objects.create(user=request.user)
        order.products.add(order_item)
        messages.info(request, 'This item was added to your cart')

    previous_url = request.META.get('HTTP_REFERER')
    host = request.get_host()
    if previous_url == (f'http://{host}/'):  # The url of your page
        return redirect('store')  #
    else:
        return redirect('product', slug=slug)


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
    messages.info(request, 'Product removed from your cart.')
    return redirect('cart')


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
        return redirect('cart')
    else:
        order.products.remove(order_item)
        order_item.delete()
        messages.info(request, 'Product removed from your cart.')
        return redirect('cart')


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
    return redirect('cart')


def define_address(request):
    order = Order.objects.get(user=request.user, complete=False)
    if order.products.all().count() == 0:
        messages.warning(request, 'You do not have items in your cart. Try add new items.')
        return redirect('store')
    else:
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
                return redirect('create_checkout')

        context = {'form': form}
        return render(request, 'store/checkout.html', context)


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
        mode='payment',
        success_url=(f'http://{host}{reverse("sucess")}'),
        cancel_url=(f'https://{host}{reverse("cancel")}'),
    )
    
    return redirect(checkout_session.url, code=303)


def sucess(request):
    order = Order.objects.get(user=request.user, complete=False)
    order_items = order.products.all()
                
    order_items.update(ordered=True)  # O método do .update serve pra quando eu quero colocar um valor específico pra um campo em todos os objetos do meu queryset
    for item in order_items:
        item.save()

    order.complete = True
    order.save()

    context = {'order': order}
    return render(request, 'store/sucess.html', context)


def cancel(request):  # Ver o que essa view de cancel deveria fazer e organiza-la. Talvez tenha algo a ver com o tratamento de erros e webhooks.
    return render(request, 'store/cancel.html')


def orders_completed(request):
    orders = Order.objects.filter(user=request.user, complete=True)
    context = {'orders': orders}
    return render(request, 'store/orders_completed.html', context)

def detail_order_completed(request, pk):
    order = Order.objects.get(id=pk)
    products = order.products.all()
    context = {'order': order, 'products': products}
    return render(request, 'store/detail_order_completed.html', context)

