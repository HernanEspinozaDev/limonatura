# apps/sales/models.py

from django.db import models
from products.models import Product
from users.models import CustomUser

class Sale(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_value = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)
    delivery_option = models.CharField(max_length=50)

    def __str__(self):
        return f"Venta #{self.id} - Cliente: {self.customer.username}"

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
