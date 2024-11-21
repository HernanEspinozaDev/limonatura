# products/apps.py

from django.apps import AppConfig

class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'  # Solo 'products', ya que está en la raíz
