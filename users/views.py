from django.db import IntegrityError
from django.shortcuts import render
from .models import Users, Paises, RolesUser

from django.contrib import messages
from django.shortcuts import render, redirect

# Create your views here.
def registrarUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        edad = request.POST.get('edad')
        dispositivo = request.POST.get('dispositivo')
        pais = request.POST.get('pais')
        rol = request.POST.get('rol')

        try:
            pais = Paises.objects.get(id=pais)  
            rol = RolesUser.objects.get(id=rol)
            user = Users.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name,
                edad=edad,
                dispositivo=dispositivo,
                pais=pais,
                rol=rol
            )
            user.save()
            messages.success(request, 'Usuario registrado exitosamente.')
        except IntegrityError:
            messages.error(request, 'El nombre de usuario ya existe. Por favor, elige otro.')

    return render(request, 'registrar.html')  # Asegúrate de tener esta plantilla creada