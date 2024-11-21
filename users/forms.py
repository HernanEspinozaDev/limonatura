# apps/users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from captcha.fields import CaptchaField

class CustomUserCreationForm(UserCreationForm):
    RUT = forms.CharField(max_length=12)
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES)
    captcha = CaptchaField()

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'RUT', 'role', 'password1', 'password2')

    def clean_RUT(self):
        RUT = self.cleaned_data.get('RUT')
        if not validar_rut(RUT):
            raise forms.ValidationError('El RUT ingresado no es válido.')
        return RUT

def validar_rut(rut):
    # Implementa aquí la lógica de validación del RUT
    return True  # Retorna True si el RUT es válido
