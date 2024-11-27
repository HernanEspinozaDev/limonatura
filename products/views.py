from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from .forms import ProductForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
import openpyxl


def product_list(request):
    category_id = request.GET.get('category')
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None,
    })

def product_list_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()
    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': category.id,
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

def is_admin_or_seller(user):
    return user.is_authenticated and (user.role == 'admin' or user.role == 'seller')

@login_required
@user_passes_test(is_admin)
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'products/product_create.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_update.html', {'form': form})

@login_required
@user_passes_test(is_admin_or_seller)
def export_stock_excel(request):
    products = Product.objects.all()
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Stock de Productos'

    # Agregar encabezados
    ws.append(['Código SKU', 'Nombre', 'Descripción', 'Precio', 'Stock', 'Imagen'])

    # Agregar datos de productos
    for product in products:
        ws.append([
            product.SKU,
            product.name,
            product.description,
            float(product.price),
            product.stock,
            product.image.url if product.image else ''
        ])

    # Configurar la respuesta HTTP
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="stock_productos.xlsx"'
    wb.save(response)
    return response
