# products/forms.py

from django import forms
from .models import Product, Category  

class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label="Categoría")

    class Meta:
        model = Product
        fields = ['SKU', 'name', 'category', 'description', 'price', 'stock', 'image']
