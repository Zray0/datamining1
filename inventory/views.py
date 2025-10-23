from django.shortcuts import render, get_object_or_404
from .models import Product

def product_list(request):
    q = request.GET.get('q', '')
    products = Product.objects.all()
    if q:
        products = products.filter(name__icontains=q)
    return render(request, 'inventory/product_list.html', {'products': products, 'q': q})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'inventory/product_detail.html', {'product': product})

from rest_framework import viewsets
from inventory.models import Product
from inventory.serializers import ProductSerializer, CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

