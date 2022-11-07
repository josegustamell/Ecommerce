from django.shortcuts import render, get_object_or_404
from .models import Category, Product, ProductImage

def home(request):
    products = Product.objects.all()
    highlights = Product.objects.filter(available=True).order_by('-sold')[0:3]
    releases = Product.objects.filter(available=True).order_by('-date_created')[0:6]
    dresses = Product.objects.filter(category=1, available=True)
    skirts = Product.objects.filter(category=2, available=True)
    blouses = Product.objects.filter(category=3, available=True)
    sacred_art = Product.objects.filter(category=4, available=True)
    rosaries = Product.objects.filter(category=5, available=True)
    context = {
        'products': products, 'highlights': highlights, 'releases': releases, 
        'dresses': dresses, 'skirts': skirts, 'blouses': blouses, 'sacred_art': sacred_art,
        'rosaries': rosaries,
        }
    return render(request, 'store/store.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    context = {'product': product}
    return render(request, 'store/product_detail.html', context)


def category_page(request, pk):
    category = get_object_or_404(Category, id=pk)
    context = {'category': category}
    return render(request, 'store/category-page.html', context)