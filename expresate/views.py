from django.shortcuts import render
#prueba para redis
from django.core.cache import cache
from django.http import JsonResponse
from users.models import Paises, RolesUser
from mongoData.models import Paises as MongoPaises



#functiones de las vistas : Jhon Alexander
def index(request):
    return render(request, 'index.html', {})

def clases(request):
    return render(request, 'clases.html', {})
#
def nosotros(request):
    return render(request, 'nosotros.html', {})

def cursos(request):
    return render(request, 'cursos.html', {})
def curso(request):
    return render(request, 'curso.html', {})

def descripcionCurso(request):
    return render(request, 'descripcion-curso.html', {})

def registrar(request):
    # Obtener datos de MongoDB
    paisCollection = MongoPaises.objects.all().order_by('nombre')
    # Obtener datos de PostgreSQL
    listRoles = RolesUser.objects.all().order_by('nombre')
    listPaises = Paises.objects.all().order_by('nombre')

    return render(request, 'registrar.html',{
        'listRoles': listRoles,
        'listPaises': listPaises,
        'paisCollection': paisCollection,
    })

def login(request):
    return render(request, 'login.html', {})

def adminLogin(request):
    return render(request, 'admin/login.html', {})

def adminDashboard(request):
    return render(request, 'admin/app/dashboard.html', {})



#funciones para archivos anteriores
def indexOld(request):
    return render(request, 'index-old.html', {})

def clasesOld(request):
 return render(request, 'clases-old.html', {})

def nosotrosOld(request):
    return render(request, 'nosotros-old.html', {})

def contactoOld(request):
    return render(request, 'contacto-old.html', {})

def registrarOld(request):
    return render(request, 'registrar-old.html', {})

def loginOld(request):
    return render(request, 'login-old.html', {})

def moduloClases(request):
    return render(request, 'modulo_clase.html', {})