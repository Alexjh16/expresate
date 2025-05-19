from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from .models import *
import json

# Método para seleccionar y enviar todas las categorías o módulos al formulario de creación de video
def selectCategoria(request, nombreCurso):
    try:
        categorias = CategoriaClases.objects.all()
        cursos_videos = Videos.objects.filter(curso__categoria_clase__nombre_categoria=nombreCurso).values(
            'id', 'edad_minima', 'descripcion', 'duracion', 'video_url', 'imagen_portada', 'curso__id',
            'curso__titulo', 'curso__descripcion', 'curso__icono', 'curso__duracion', 'curso__estado_curso',
            'curso__cuestionario__titulo', 'curso__cuestionario__id', 'curso__nivel__nombre')
       
        #print('contenidos_categorias', cursos_videos)
        nombre_categoria = categorias.first().nombre_categoria if categorias.exists() else None
        return render(request, 'curso.html', {
            'categorias': categorias,
            'nombre_categoria': nombreCurso,
            'cursos_videos': cursos_videos
        })
    except Exception as e:
        print(f"Error en selectCategoria: {e}")
        return HttpResponse('Error en selectCategoria', {'error_message': 'Ocurrió un error al cargar las categorías.'})

def selectContenidos(request):
    try:
        cursos = Videos.objects.filter(curso__categoria_clase__nombre_categoria='Familia').values(
            'id',
            'edad_minima',
            'descripcion',
            'duracion',
            'video_url',
            'imagen_portada',
            'curso__id',
            'curso__titulo',
            'curso__descripcion',
            'curso__icono',
            'curso__duracion',
            'curso__estado_curso',
            'curso__cuestionario__titulo',
            'curso__cuestionario__id',
            'curso__nivel__nombre'
        )
        return HttpResponse(json.dumps(list(cursos)), content_type="application/json")
    except Exception as e:
        print(f"Error en contenidos: {e}")
        return HttpResponse(json.dumps({'error_message': 'Ocurrió un error al cargar los contenidos.'}), content_type="application/json")
    
# Método para seleccionar un video por su ID
def selectVideo(request, idVideo):
    print(idVideo)
    selectVideo = Videos.objects.get(id = idVideo)
    atributosVideo = {
        'selectVideo' : selectVideo,
        'video_url' : selectVideo.video_url,
        'descripcion' : selectVideo.descripcion,
        'duracion' : selectVideo.duracion
    }
    print(atributosVideo)
    return render(request, 'components/play_video.html', {'atributosVideo':atributosVideo})