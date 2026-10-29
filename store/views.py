from django.shortcuts import render, get_object_or_404
from .models import Product

def product_list(request):
    """View to display all available products on the home page"""
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def product_detail(request, pk):
    """View to display details of a single product"""
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})