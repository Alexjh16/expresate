from django.shortcuts import render

from contenidos.models import CategoriaClases, Cursos, Niveles
from evaluacion.models import Cuestionarios

def index(request):
    return render(request, 'view_admin/app_admin/base_admin.html', {})

def createCategoriaClases(request):
    print('createCategoriaClases', request)
    if request.method == 'POST':
        categoriaClase = CategoriaClases.objects.create(
            nombre_categoria = request.POST['nombre'],
            descripcion = request.POST['descripcion'],
            edad_minima = request.POST['edad_minima'],
            icono = request.POST['icono']
        )
        return render(request, 'view_admin/agregar_categoriaClase.html', {})
#CRUD de niveles
def formCreateNivele(request):
        return render(request, 'view_admin/form_niveles.html', {})
    
def createNivele(request):
    print('createNivele', request)
    if request.method == 'POST':
        nivel = Niveles.objects.create(
            nombre = request.POST['nombre'],
            descripcion = request.POST['descripcion'],
            icono = request.POST['icono']
        )
        return render(request, 'view_admin/form_niveles.html', {})
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
            duracion_estimada = request.POST['duracion_estimada']
        )
        return render(request, 'view_admin/form_cuestionarios.html', {})
#CRUD de cursos
def formCreateCurso(request):
    print('formCreateCurso', request)
    return render(request, 'view_admin/form_cursos.html', {})

def createCurso(request):
    print('createCurso', request)
    if request.method == 'POST':
        curso = Cursos.objects.create(
            titulo = request.POST['titulo'],
            descripcion = request.POST['descripcion'],
            duracion = request.POST['duracion'],
            icono = request.POST['icono'],
            estado_curso = request.POST['estado_curso'],
            categoria_clase = request.POST['categoria_clase'],
            cuestionario = request.POST['cuestionario'],
            nivel = request.POST['nivel']
        )
        return render(request, 'view_admin/agregar_cursos.html', {})