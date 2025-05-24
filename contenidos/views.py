from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login #aca se se coloca un alias al metodo login se manda a llamar esto se hace porqeu hay una funcion llamada login y causa conflitos. lo mismo se hace con logout
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from mongoData.models import Cursos as MongoCursos
from mongoData.models import Videos as MongoVideos
from mongoData.models import UserVideosCurso #para el progrose del usuario
from types import SimpleNamespace
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import datetime
from .models import *

import json

#Metodo para selecionar i enviar todas las categoria o modulos al formulario de creacion de video  
def curso(request, idCurso):    
    
    #curso actual
    cursoActual = MongoCursos.objects.filter(id=idCurso).first()   
    
    #cursos relacionados
    cursosRelacionados = MongoCursos.objects(
        categoria_clase=cursoActual.categoria_clase,
        id__ne=idCurso
    ).limit(3)

    

    #cursos recomendados
    cursosRecomendados = MongoCursos.objects(
        categoria_clase=cursoActual.categoria_clase,
        id__ne=idCurso
    ).limit(4)

    #obtener los videos del curso actual
    videosCurso = MongoVideos.objects.filter(idCurso=idCurso).order_by('fecha_creacion')
    primerVideo =  MongoVideos.objects.filter(idCurso=idCurso).first()
    #total de videos del curso
    total_videos = videosCurso.count()
    #obtener el progreso del usuario en el curso actual
    username = request.user.username
    progreso_usuario = UserVideosCurso.objects(
        idCurso=idCurso,
        usuario__in=[username]
    ).first()
    
    # Determinar videos vistos por el usuario
    videos_vistos_nombres = set()
    videos_vistos_archivos = set()
    if progreso_usuario and progreso_usuario.video:
        videos_vistos_nombres = set(v.nombre for v in progreso_usuario.video if v.fecha_visualizacion)
        videos_vistos_archivos = set(getattr(v, 'ruta', None) for v in progreso_usuario.video if v.fecha_visualizacion)

    lecciones = []
    encontrado_actual = False
    # Construye un set de tuplas (nombre, ruta) de los videos vistos
    videos_vistos = set(
        (v.nombre, getattr(v, 'ruta', None))
        for v in progreso_usuario.video if v.fecha_visualizacion
    ) if progreso_usuario and progreso_usuario.video else set()

    for idx, video in enumerate(videosCurso):
        clave_video = (video.nombre, getattr(video, 'ruta', None))
        visto = clave_video in videos_vistos
        if visto:
            estado = "completed"
        elif not encontrado_actual:
            estado = "locked"
            encontrado_actual = True
        else:
            estado = "current"
        lecciones.append({
            "id": str(video.id), 
            "nombre": video.nombre,
            "duracion": video.duracion,
            "estado": estado,
        })
    return render(request, 'curso.html', {
        'cursoActual':cursoActual,
        'cursosRelacionados':cursosRelacionados,
        'cursosRecomendados':cursosRecomendados,
        'videosCurso':videosCurso,
        'progreso_usuario': progreso_usuario,
        'total_videos': total_videos,
        'lecciones': lecciones,
        'primerVideo': primerVideo,
    })


#reproduccion de los videos
def video_curso_ajax(request, idCurso, idVideo):
    video = MongoVideos.objects.get(id=idVideo)
    primerVideo = MongoVideos.objects.filter(idCurso=idCurso).first()
    username = request.user.username

    # Obtener progreso del usuario
    progreso_usuario = UserVideosCurso.objects(idCurso=idCurso, usuario__in=[username]).first()
    if not progreso_usuario:
        progreso_usuario = UserVideosCurso(idCurso=idCurso, usuario=[username], video=[])

    # Verificar si ya está visto
    ya_visto = any(
        v['nombre'] == video.nombre and v['ruta'] == video.ruta
        for v in progreso_usuario.video
    )
    if not ya_visto:
        progreso_usuario.video.append({
            "nombre": video.nombre,
            "ruta": video.ruta,
            "fecha_visualizacion": datetime.now()
        })
        progreso_usuario.save()

    # Desbloquear la siguiente lección
    videosCurso = list(MongoVideos.objects.filter(idCurso=idCurso).order_by('fecha_creacion'))
    for idx, v in enumerate(videosCurso):
        if v.id == video.id and idx + 1 < len(videosCurso):
            siguiente = videosCurso[idx + 1]
            # Aquí deberías actualizar el estado de la siguiente lección en tu lógica de lecciones
            # Por ejemplo, si tienes una colección de lecciones, actualiza su estado a 'current' o 'unlocked'
            # Esto depende de cómo generas la lista 'lecciones' en tu template

    html = render_to_string('partials/video_player.html', {'video': video, 'primerVideo': primerVideo})
    return HttpResponse(html)

