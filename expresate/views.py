from django.shortcuts import render
#prueba para redis
from django.core.cache import cache
from django.shortcuts import get_object_or_404 as findObject
from django.http import JsonResponse
from users.models import Paises, RolesUser
from contenidos.models import CategoriaClases
from mongoData.models import Paises as MongoPaises
from mongoData.models import Cursos as MongoCursos
from mongoData.models import Videos as MongoVideos
from mongoData.models import Cuestionario as MongoCuestionarios
from django.core.paginator import Paginator



#functiones de las vistas : Jhon Alexander
def index(request):
    return render(request, 'index.html', {})

def clases(request):
    #Retornar las clases
    listCategoriasClases = CategoriaClases.objects.all().order_by('nombre_categoria');
    return render(request, 'clases.html', {
        'listCategoriasClases': listCategoriasClases
    })
#
def nosotros(request):
    return render(request, 'nosotros.html', {})

def cursos(request, categoria):
    categoriaActual = findObject(CategoriaClases, nombre_categoria=categoria)
    listCategoriasClases = CategoriaClases.objects.all().order_by('nombre_categoria');

    otrasCategorias = CategoriaClases.objects.exclude(nombre_categoria=categoria).order_by('?')[:3]
    totalCursosOtros = []
    for otraCategoria in otrasCategorias:
        countCurso = MongoCursos.objects.filter(categoria_clase=otraCategoria.nombre_categoria).count()
        totalCursosOtros.append(countCurso)

    

    #paginar los cursos para no saturar el DOM : Jhon Alexander
    listCursos = MongoCursos.objects.filter(categoria_clase=categoria)
    paginator = Paginator(listCursos, 8) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Agregar countVideos a cada curso del page_obj
    for curso in page_obj:
        curso.countVideos = MongoVideos.objects.filter(idCurso=curso.id).count()

    totalCursos = MongoCursos.objects.filter(categoria_clase=categoria).count()
    totalCuestionarios = MongoCursos.objects.filter(
        categoria_clase=categoria,
        idCuestionario__ne=None
    ).count()
    return render(request, 'cursos.html', {
        'categoriaActual': categoriaActual,
        'listCategoriasClases': listCategoriasClases,
        'listCursos': listCursos,
        'totalCursos': totalCursos,
        'page_obj': page_obj,
        'totalCuestionarios': totalCuestionarios,
        'otrasCategorias': otrasCategorias,
        'totalCursosOtros': totalCursosOtros
        
        
    })
def curso(request):
    return render(request, 'curso.html', {})

def descripcionCurso(request, idCurso):
    descripcionCurso = MongoCursos.objects.get(id=idCurso)
    countVideos = MongoVideos.objects.filter(idCurso=idCurso).count()
    return render(request, 'descripcion-curso.html', {
        'descripcionCurso': descripcionCurso,
        'countVideos': countVideos
    })

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