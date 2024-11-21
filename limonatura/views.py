from django.shortcuts import render
from products.models import Product

def index(request):
    products = Product.objects.all()[:10]  # Muestra los primeros 10 productos
    return render(request, 'index.html', {'products': products})
