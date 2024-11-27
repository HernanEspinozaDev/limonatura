# sales/models.py

from django.db import models
from products.models import Product
from users.models import CustomUser

class Sale(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('tarjeta', 'Tarjeta de Débito'),
        ('efectivo', 'Pago en Efectivo'),
    ]

    DELIVERY_OPTION_CHOICES = [
        ('retiro', 'Retiro en Tienda'),
        ('despacho', 'Despacho a Domicilio'),
    ]

    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_value = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)
    delivery_option = models.CharField(max_length=50, choices=DELIVERY_OPTION_CHOICES)

    def __str__(self):
        return f"Venta #{self.id} - Cliente: {self.customer.username}"

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name} for Sale #{self.sale.id}"
