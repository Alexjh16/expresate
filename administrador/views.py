from django.http import HttpResponse
from django.shortcuts import render
from contenidos.models import CategoriaClases, Cursos, Niveles, Videos
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
#CRUD de videos
def formCreateVideo(request):    
    #print('curso', curso[4])
    #nombre_categoria = categorias[0].nombre_categoria if categorias.exists() else None
    return render(request, 'view_admin/form_videos.html', {'cursos': Cursos.objects.all()})
def createVideo(request):
    print('createVideo', request)
    if request.method == 'POST':
        video = Videos.objects.create(
            descripcion = request.POST['descripcion'],
            edad_minima = request.POST['edad_minima'],
            duracion = request.POST['duracion'],
            video_url = request.FILES.get('video_url'),
            imagen_portada = request.FILES.get('imagen_portada'),
        )
        return render(request, 'view_admin/form_videos.html', {'cursos': Cursos.objects.all()})
        
#CRUD de cursos
def formCreateCurso(request):
    print('formCreateCurso', request)
    categorias = CategoriaClases.objects.all()
    niveles = Niveles.objects.all()
    cuestionarios = Cuestionarios.objects.all()
    videos = Videos.objects.all()
    return render(request, 'view_admin/form_cursos.html', {'videos':videos,'categorias': categorias, 'niveles': niveles, 'cuestionarios': cuestionarios})

def createCurso(request):
    print('createCurso', request)
    if request.method == 'POST':
        curso = Cursos.objects.create(
            titulo = request.POST['titulo'],
            descripcion = request.POST['descripcion'],
            duracion = request.POST['duracion'],
            icono = request.POST['icono'],
            #estado_curso = request.POST['estado_curso'],
            categoria_clase = CategoriaClases.objects.get(id=request.POST['categoria']),
            cuestionario = Cuestionarios.objects.get(id=request.POST['cuestionario']),
            nivel = Niveles.objects.get(id=request.POST['nivel']),
            #video = Videos.objects.get(id=request.POST['video'])
        )
        categorias = CategoriaClases.objects.all()
        niveles = Niveles.objects.all()
        cuestionarios = Cuestionarios.objects.all()
        #videos = Videos.objects.all()
        return render(request, 'view_admin/form_cursos.html', {''''videos': videos,''' 'categorias': categorias, 'niveles': niveles, 'cuestionarios': cuestionarios})