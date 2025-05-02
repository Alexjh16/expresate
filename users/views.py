from django.shortcuts import render
from .forms import registrarUserForm, loginUserForm
from django.core.cache import cache as redis #redis: Jhon Alexander
from .models import Paises, RolesUser
from django.contrib import messages
from django.shortcuts import render, redirect
from altcha import ChallengeOptions
from datetime import datetime, timedelta
from django.conf import settings
from django.http import JsonResponse
from altcha import create_challenge, verify_solution
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required

# Clave secreta (guárdala en settings.py en producción)
SECRET_KEY = settings.ALTCHA_SECRET_KEY



def altcha_challenge(request):
    if request.method == 'POST':
        token = request.POST.get('altcha')
        is_valid = verify_solution(token, hmac_key=SECRET_KEY, check_expires=True)  # Usando settings
        return JsonResponse({'valid': is_valid})
    
    options = ChallengeOptions(
        algorithm=settings.ALTCHA_ALGORITHM,  # Desde settings
        hmac_key=settings.ALTCHA_SECRET_KEY,   # Desde settings
        max_number=100000,
        salt_length=16,
        expires=datetime.now() + timedelta(minutes=10),
        params={'custom': 'django'}
    )
    
    challenge = create_challenge(options)
    return JsonResponse({
        'algorithm': challenge.algorithm,
        'challenge': challenge.challenge,
        'salt': challenge.salt,
        'signature': challenge.signature
    })


def registrarUser(request):
    listPaises = Paises.objects.all() 
    listRoles = RolesUser.objects.all()
    if request.method == 'POST':
        form = registrarUserForm(request.POST)
        if form.is_valid():
            #guardar el usuario en la base de datos pgsql
            user = form.save()
            #guardar el usuario en la base de datos redis
            redis.set(user.username, user.password, timeout=300, version='')  # 5 minutos
            messages.success(request, 'Usuario registrado, por favor inicia sesión')
            return redirect('login') 
        else:
            print(form.errors)
            messages.error(request, 'Por favor valida la información del formulario')
    else:
        form = registrarUserForm()

    return render(request, 'registrar.html', {
        'form': form,
        'listPaises': listPaises,
        'listRoles': listRoles,
    })

def loginUser(request):

    if request.user.is_authenticated:
        return redirect('clases')  # Redirige si ya está autenticado
        
    if request.method == 'POST':
        form = loginUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido {user.first_name}!')                
                # Obtener la URL de redirección, si existe
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('clases')  # O la URL que desees después del login
        else:
            # Si el formulario no es válido, mostramos los errores
            print(form.errors)
            for field in form.errors:
                for error in form.errors[field]:
                    messages.error(request, f"{error}")
    else:
        form = loginUserForm()
    
    return render(request, 'login.html', {
        'form': form,
        'title': 'Iniciar Sesión'
    })
    
def logoutUser(request):
    auth_logout(request)
    return redirect('login')