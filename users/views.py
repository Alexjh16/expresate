from django.shortcuts import render
from .forms import registrarUserForm, loginUserForm
from expresate.redisUtil import redisClient
from .models import Paises, RolesUser
from django.contrib import messages
from django.shortcuts import render, redirect
from altcha import ChallengeOptions
from datetime import datetime, timedelta
from django.conf import settings
from django.http import JsonResponse
from django.contrib.sessions.models import Session
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from altcha import create_challenge, verify_solution
from django.contrib.auth import authenticate, logout as auth_logout, login
from mongoData.models import Users as MongoUsers
from mongoData.models import Paises as MongoPaises
import logging

logger = logging.getLogger(__name__)



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
    
    # Obtener datos de PostgreSQL
    listPaises = Paises.objects.all() 
    listRoles = RolesUser.objects.all()   
   

    if request.method == 'POST':
        form = registrarUserForm(request.POST)
        if form.is_valid():
            # guardar el usuario en la base de datos pgsql
            user = form.save()
            # guardar el usuario en la base de datos redis
            redisClient.set(user.username, user.password, ex=3000)  # 5 minutos
            print("Usuario guardado en Redis")
            messages.success(request, 'Usuario registrado, por favor inicia sesión')

            # guardar el usuario en la base de datos mongo
            pais_name = user.pais.nombre
            MongoUsers(
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                username=user.username,
                password=user.password,
                foto_perfil="static/img/usuario.png",
                edad=25,
                rol=user.rol.nombre,
                idPais=MongoPaises.objects.get(nombre=pais_name),
                dispositivo=user.dispositivo,
            ).save()            
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


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('clases')  # Redirige si ya está autenticado
        
    if request.method == 'POST':
        form = loginUserForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Verificar si el usuario está en Redis
            cached_password = redisClient.get(username)
            if cached_password:
                cached_password = cached_password.decode('utf-8') # Decodificar la contraseña almacenada en Redis                
                user = authenticate(username=username, password=password)
                if user is not None:
                    print("login redis")
                    login(request, user)
                    return redirect('clases')  # Redirigir después del login
                else:
                    messages.error(request, 'Contraseña incorrecta.')
            else:
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    print("login pgsql")              
                    return redirect('clases')  # O la URL que desees después del login
        else:
            # Si el formulario no es válido, mostramos los errores
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
    response = redirect('index')
    return response