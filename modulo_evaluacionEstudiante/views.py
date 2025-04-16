import json
from django.http import JsonResponse
from django.shortcuts import render
from modelos_expresate.models import CategoriaClases
from modulo_evaluacionEstudiante.models import Notas, Preguntas

def indexCrearPreguntas(request):
    arrayCategoriaClases = CategoriaClases.objects.all().order_by('nombre_categoria')
    return render(request, 'view_admin/crear_evaluacion.html', {'arrayCategoriaClases': arrayCategoriaClases})

def crearPreguntas(request):
    if request.method == 'POST':
        arrayCategoriaClases = CategoriaClases.objects.all().order_by('nombre_categoria')
        categoria = CategoriaClases.objects.get(id=request.POST.get('categoriaClase'))
        createPregunta = Preguntas.objects.create(
            pregunta = request.POST['pregunta'],
            
            respuesta_correcta = request.POST['respuestaCorrecta'],
            
            respuesta1 = request.POST['respuesta_1'],
            respuesta2 = request.POST['respuesta_2'],
            respuesta3 = request.POST['respuesta_3'],
            respuesta4 = request.POST['respuesta_4'],
            
            imagen = request.FILES.get('imagen'),
            video =  request.FILES.get('video'),
            
            categoriaClases = categoria,
        )
    return render(request, 'view_admin/crear_evaluacion.html', {'arrayCategoriaClases': arrayCategoriaClases})

def evaluacionModulo(request, NME):
    print(NME)
    respuestas = Preguntas.objects.filter(categoriaClases__nombre_categoria = NME).all()
    return render(request, 'evaluacion.html', {'respuestas': respuestas})

def notas(request):
    if request.method == 'POST':
      datosNota = json.loads(request.body)
            
      nombreCategoria = datosNota.get('nombreCategoria')
      preguntasBuenas = datosNota.get('preguntasBuenas')
      preguntasMalas = datosNota.get('preguntasMalas')
      notaFinalModulo = datosNota.get('notaFinalModulo')
      usuario = request.user
      
      if notaFinalModulo >= 3:
        estado = 'aprobado'
      else:
        estado = 'No aprobado'
          
      notas = Notas.objects.create(
        nombre_categoria = nombreCategoria,
        respuestas_buenas = preguntasBuenas,
        respuestas_malas = preguntasMalas,
        nota = notaFinalModulo,
        estado = estado,
        user = usuario
      )
    return JsonResponse({"success":"'Notas guardadas con exito'"})
    