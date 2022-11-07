from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='store'),
    path('product/<slug:slug>', views.product_detail, name='product_detail'),
    path('category/<str:pk>', views.category_page, name='category_page')
]