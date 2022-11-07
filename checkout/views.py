from django.shortcuts import render, redirect
from .forms import *


# Delivery
def add_address(request):
    form = AddressForm()
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():        
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('checkout:payment')
    context = {'form': form}
    return render(request, 'accounts/addresses/add-address.html', context)
    

def payment(request):
    if request.method == 'POST':
        pass

    return render(request, 'checkout/payment.html')