# products/forms.py

from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['SKU', 'name', 'description', 'price', 'stock', 'image']
