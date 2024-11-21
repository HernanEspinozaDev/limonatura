# apps/users/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
import openpyxl
from django.http import HttpResponse
from .models import CustomUser

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registro exitoso. Por favor, inicia sesión.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        captcha = CaptchaField()
        if form.is_valid() and captcha.validate(request.POST.get('captcha')):
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
        messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'users/profile.html')

@login_required
def export_users_excel(request):
    if request.user.role != 'admin':
        return HttpResponse('No autorizado', status=403)
    
    users = CustomUser.objects.all()
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Usuarios'

    ws.append(['Nombre', 'RUT', 'Perfil de Acceso'])
    for user in users:
        ws.append([user.username, user.RUT, user.get_role_display()])

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="usuarios.xlsx"'
    wb.save(response)
    return response

def user_logout(request):
    logout(request)
    return redirect('index')
