# apps/sales/views.py

from django.shortcuts import render, redirect
from apps.products.models import Product
from .models import Sale, SaleItem
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('product_list')

@login_required
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
        return redirect('view_cart')
    
@login_required
def download_receipt(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id, customer=request.user)
    template_path = 'sales/receipt.html'
    context = {'sale': sale}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="boleta_{sale.id}.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)
    return response

@login_required
def order_confirmation(request, sale_id):
    sale = Sale.objects.get(id=sale_id)
    return render(request, 'sales/order_confirmation.html', {'sale': sale})
