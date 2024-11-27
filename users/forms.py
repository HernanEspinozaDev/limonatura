# users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from captcha.fields import CaptchaField

class CustomUserCreationForm(UserCreationForm):
    RUT = forms.CharField(max_length=12)
    captcha = CaptchaField()

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'RUT', 'password1', 'password2')  # Elimina 'role' de aquí

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'customer'  # Asigna el rol 'customer' por defecto
        if commit:
            user.save()
        return user

    
    def clean_RUT(self):
        RUT = self.cleaned_data.get('RUT')
        if not validar_rut(RUT):
            raise forms.ValidationError('El RUT ingresado no es válido.')
        return RUT

def validar_rut(rut):
    # Implementa aquí la lógica de validación del RUT
    return True  # Retorna True si el RUT es válido

class CustomAuthenticationForm(AuthenticationForm):
    captcha = CaptchaField()