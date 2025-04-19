from django.shortcuts import render
from .forms import registrarUserForm
from .models import Paises, RolesUser
from django.contrib import messages
from django.shortcuts import render, redirect


def registrarUser(request):
    listPaises = Paises.objects.all() 
    listRoles = RolesUser.objects.all()
    if request.method == 'POST':
        form = registrarUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario registrado, por favor inicia sesión')
            return redirect('login') 
        else:
            messages.error(request, 'Por favor valida la información del formulario')
    else:
        form = registrarUserForm()

    return render(request, 'registrar.html', {
        'form': form,
        'listPaises': listPaises,
        'listRoles': listRoles,
    })