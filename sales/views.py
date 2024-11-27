# sales/views.py

from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from .models import Sale, SaleItem
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.conf import settings
from django.contrib.staticfiles import finders
import os

def link_callback(uri, rel):
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        path = result[0]
    else:
        sUrl = settings.STATIC_URL
        sRoot = settings.STATIC_ROOT
        mUrl = settings.MEDIA_URL
        mRoot = settings.MEDIA_ROOT
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri
    if not os.path.isfile(path):
        raise Exception('URI de medios no válida')
    return path


def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('product_list')

def update_cart(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                product_id = key.split('_')[1]
                cart[product_id] = int(value)
            elif key.startswith('remove_'):
                product_id = key.split('_')[1]
                cart.pop(product_id, None)
        request.session['cart'] = cart
    return redirect('view_cart')

def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
    return render(request, 'sales/cart.html', {'cart_items': cart_items, 'total': total})


@login_required
def checkout(request):
    if request.method == 'POST':
        # Procesar el pago y crear la venta
        cart = request.session.get('cart', {})
        if not cart:
            return redirect('product_list')
        sale = Sale.objects.create(
            customer=request.user,
            total_value=0,  # Se actualizará más adelante
            payment_method=request.POST.get('payment_method'),
            delivery_option=request.POST.get('delivery_option'),
        )
        total = 0
        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)
            SaleItem.objects.create(sale=sale, product=product, quantity=quantity)
            total += product.price * quantity
            # Actualizar stock
            product.stock -= quantity
            product.save()
        sale.total_value = total
        sale.save()
        # Limpiar el carrito
        del request.session['cart']
        return redirect('order_confirmation', sale_id=sale.id)
    else:
        # Mostrar el resumen de la compra
        cart = request.session.get('cart', {})
        if not cart:
            return redirect('product_list')
        cart_items = []
        total = 0
        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)
            subtotal = product.price * quantity
            total += subtotal
            cart_items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
        return render(request, 'sales/checkout.html', {'cart_items': cart_items, 'total': total})
    
@login_required
def download_receipt(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id, customer=request.user)
    template_path = 'sales/receipt.html'
    
    # Calcular el total por producto
    sale_items = sale.saleitem_set.all()
    for item in sale_items:
        item.total = item.quantity * item.product.price
    
    context = {
        'sale': sale,
        'sale_items': sale_items
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="boleta_{sale.id}.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
        html, dest=response, link_callback=link_callback)
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)
    return response

@login_required
def order_confirmation(request, sale_id):
    sale = Sale.objects.get(id=sale_id)
    return render(request, 'sales/order_confirmation.html', {'sale': sale})
