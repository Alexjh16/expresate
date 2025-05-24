from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login #aca se se coloca un alias al metodo login se manda a llamar esto se hace porqeu hay una funcion llamada login y causa conflitos. lo mismo se hace con logout
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from mongoData.models import Cursos as MongoCursos
from .models import *
import json

#Metodo para selecionar i enviar todas las categoria o modulos al formulario de creacion de video  
def curso(request, idCurso):    
    
    #curso actual
    cursoActual = MongoCursos.objects.filter(id=idCurso).first()   

    return render(request, 'curso.html', {
        'cursoActual':cursoActual
    })
