from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login #aca se se coloca un alias al metodo login se manda a llamar esto se hace porqeu hay una funcion llamada login y causa conflitos. lo mismo se hace con logout
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import *
import json

#Metodo para selecionar i enviar todas las categoria o modulos al formulario de creacion de video  
def curso(request, nombreCurso):    
    # Filtra las categorías por el nombre de la categoría
    print(nombreCurso)
    categorias = CategoriaClases.objects.all()
    cursos = Cursos.objects.filter(titulo=nombreCurso)
    nombre_categoria = categorias[0].nombre_categoria if categorias.exists() else None
    return render(request, 'curso.html', {
        'categorias':categorias, 
        'cursos':cursos, 
        'nombre_categoria': nombre_categoria
    })
