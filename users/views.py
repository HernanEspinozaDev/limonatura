from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
import openpyxl
from django.http import HttpResponse
from .models import CustomUser
from sales.models import Sale  # Importa el modelo Sale

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
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Autenticar y loguear al usuario
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
        messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def profile(request):
    if request.user.role == 'customer':
        sales = Sale.objects.filter(customer=request.user)
    else:
        sales = None
    return render(request, 'users/profile.html', {'sales': sales})

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

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="usuarios.xlsx"'
    wb.save(response)
    return response

def user_logout(request):
    logout(request)
    return redirect('index')
