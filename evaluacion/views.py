from django.shortcuts import render
from evaluacion.models import Cuestionarios

#CRUD de cuestionarios
def formCreateCuestionario(request):
    print('formCreateCuestionario', request)
    return render(request, 'view_admin/form_cuestionarios.html', {})

def createCuestionario(request):
    print('createCuestionario', request)
    if request.method == 'POST':
        cuestionario = Cuestionarios.objects.create(
            titulo = request.POST['titulo'],
            descripcion = request.POST['descripcion'],
            limite_intentos = request.POST['limite_intentos'],
            estado = request.POST['estado'],
            calificacion_aprobacion = request.POST['calificacion_aprobacion'],
            duracion_estimada = request.POST['duracion_estimada'],
            autor = request.user
        )
        return render(request, 'view_admin/form_cuestionarios.html', {})