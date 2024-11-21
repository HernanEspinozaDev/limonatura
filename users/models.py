# users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    RUT = models.CharField(max_length=12, unique=True)
    ROLE_CHOICES = (
        ('admin', 'Administrador'),
        ('seller', 'Vendedor'),
        ('customer', 'Cliente'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username
