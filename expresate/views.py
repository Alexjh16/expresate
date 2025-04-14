from django.shortcuts import render
#prueba para redis
from django.core.cache import cache
from django.http import JsonResponse

#prueba para mongodb
#from pymongo import MongoClient
#from django.conf import settings
#prueba para postgres

#from modelos_expresate.models import User


#conexión a mongodb
#client = MongoClient(settings.MONGO_DB["HOST"], settings.MONGO_DB["PORT"])
#mongo_db = client[settings.MONGO_DB["NAME"]]


#prueba conexion a las bases de datos y cache: Jhon Alexander
"""def dbs(request):
    datos_pg = User.objects.all()

    #datos mongo
    comentarios_collection = mongo_db["comentarios"]
    comentarios = list(comentarios_collection.find())
    for comentario in comentarios:
        comentario["_id"] = str(comentario["_id"]),
        if "usuario" in comentario:
            comentario["usuario"] = str(comentario["usuario"])  # Convertir usuario si existe
        if "video" in comentario:
            comentario["video"] = str(comentario["video"])
        if "parent_id" in comentario:
            comentario["parent_id"] = str(comentario["parent_id"])
    
    for dato in datos_pg:
        cache.set(dato.email, dato.password, timeout=300)  # 300 segundos (5 min)

    
    datos_redis = {dato.email: cache.get(dato.email) for dato in datos_pg}

    return JsonResponse({
        "datos_postgres": [{"email": dato.email, "password": dato.password} for dato in datos_pg],
        "datos_redis": datos_redis,
        "datos_mongo": comentarios
    })
"""


#functiones de las vistas : Jhon Alexander
def index(request):
    return render(request, 'index.html', {})

def clases(request):
    return render(request, 'clases.html', {})
#
def nosotros(request):
    return render(request, 'nosotros.html', {})
def contacto(request):
    return render(request, 'contacto.html', {})


def mision(request):
    return render(request, 'mision.html', {})

def vision(request):
    return render(request, 'vision.html', {})

#funciones para archivos anteriores
def indexOld(request):
    return render(request, 'index-old.html', {})

def clasesOld(request):
 return render(request, 'clases-old.html', {})

def nosotrosOld(request):
    return render(request, 'nosotros-old.html', {})

def contactoOld(request):
    return render(request, 'contacto-old.html', {})

def registrar(request):
    return render(request, 'registrar.html', {})

def login(request):
    return render(request, 'login.html', {})

def moduloClases(request):
    return render(request, 'modulo_clase.html', {})