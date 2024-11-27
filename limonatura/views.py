from django.shortcuts import render
from products.models import Product, Category

def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()[:10]  # Muestra los primeros 10 productos
    return render(request, 'index.html', {'products': products, 'categories': categories})
