from django.urls import path
from . import views

app_name = 'accounts'


urlpatterns = [
    path('account-register', views.account_register, name='account_register'),
    path('account-login', views.account_login, name='account_login'),
    path('dashboard', views.account_dashboard, name='account_dashboard'),
    path('account-detail', views.account_detail, name='account_detail'),
    path('account-orders', views.account_orders, name='account_orders'),
    # Delivery

]