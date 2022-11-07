from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [
    path('add-address', views.add_address, name='add_address'),
    path('payment', views.payment, name='payment'),
    ]