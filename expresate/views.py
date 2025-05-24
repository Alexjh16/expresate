from django.shortcuts import render
#prueba para redis
from django.shortcuts import get_object_or_404 as findObject
from django.http import JsonResponse
from users.models import Paises, RolesUser
from django.http import HttpResponse
from contenidos.models import CategoriaClases, Niveles
from mongoData.models import Paises as MongoPaises
from mongoData.models import Cursos as MongoCursos
from mongoData.models import Videos as MongoVideos
from mongoData.models import Preguntas as MongoPreguntas
from mongoData.models import UserVideosCurso as MongoUserVideosCurso
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from expresate.templatetags import splitfilters
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
from django.utils import timezone
from bson import ObjectId
from datetime import datetime
import os



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
        countCurso = MongoCursos.objects.filter(categoria_clase=otraCategoria.nombre_categoria, estado="activo").count()
        totalCursosOtros.append(countCurso)

    

    #paginar los cursos para no saturar el DOM : Jhon Alexander
    listCursos = MongoCursos.objects.filter(categoria_clase=categoria, estado="activo")
    paginator = Paginator(listCursos, 8) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Agregar countVideos a cada curso del page_obj
    for curso in page_obj:
        curso.countVideos = MongoVideos.objects.filter(idCurso=curso.id).count()

    totalCursos = MongoCursos.objects.filter(categoria_clase=categoria, estado="activo").count()
    totalCuestionarios = MongoCursos.objects.filter(
        categoria_clase=categoria,
        estado="activo",
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
    video_actual = MongoVideos.first() 
    return render(request, 'curso.html', {
        'video_actual': video_actual,
    })

def descripcionCurso(request, idCurso):
    descripcionCurso = MongoCursos.objects.get(id=idCurso)
    countVideos = MongoVideos.objects.filter(idCurso=idCurso).count()
    videos = MongoVideos.objects.filter(idCurso=idCurso)[:3]
    return render(request, 'descripcion-curso.html', {
        'descripcionCurso': descripcionCurso,
        'countVideos': countVideos,
        'videos': videos
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

def adminUsuarios(request):
    return render(request, 'admin/app/usuarios.html', {})

def adminCategorias(request):
    listCategorias = CategoriaClases.objects.all().order_by('id')
    return render(request, 'admin/app/categorias.html', {
        'listCategorias': listCategorias
    })

#read categorias
def categoriasJson(request):
    categorias = CategoriaClases.objects.all().order_by('id')
    data = []
    for categoria in categorias:
        subtitulo = splitfilters.split_before(categoria.descripcion, '-')
        descripcion = splitfilters.split_after(categoria.descripcion, '-')

        # Obtener la URL de la imagen si existe
        if categoria.icono and hasattr(categoria.icono, 'url'):
            icono_url = categoria.icono.url
        else:
            icono_url = None
        data.append({
            'id': categoria.id,
            'nombre': categoria.nombre_categoria,
            'subtitulo': subtitulo,
            'descripcion': descripcion,
            'icono': icono_url,
            'edad_minima': categoria.edad_minima,
        })
    return JsonResponse({'categorias': data})

#create categorias
@csrf_exempt  # Solo para pruebas, en producción usa CSRF correctamente
def crearCategoria(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip()
        subtitulo = request.POST.get("subtitulo", "")
        descripcion = request.POST.get("descripcion", "")
        edad_minima = request.POST.get("edad_minima", "")

        # Validar edad mínima
        try:
            edad_minima_int = int(edad_minima)
            if edad_minima_int < 7 or edad_minima_int > 120:
                return JsonResponse({"error": "La edad mínima debe estar entre 7 y 120."}, status=400)
        except ValueError:
            return JsonResponse({"error": "La edad mínima debe ser un número válido."}, status=400)

        # Validar nombre único (case-insensitive)
        if CategoriaClases.objects.filter(nombre_categoria__iexact=nombre).exists():
            return JsonResponse({"error": "Ya existe una categoría con ese nombre."}, status=400)
        

        # Validar y guardar imagen
        icono = request.FILES.get('icono')
        icono_url = None
        if icono:
            # Validar tamaño (10MB)
            if icono.size > 10 * 1024 * 1024:
                return JsonResponse({"error": "La imagen no debe superar los 10MB."}, status=400)
            # Validar extensión
            ext = os.path.splitext(icono.name)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.avif', '.svg']:
                return JsonResponse({"error": "Solo se permiten imágenes JPG, PNG, GIF, WEBP, AVIF o SVG."}, status=400)
            filename = default_storage.save(f"imagenes/{icono.name}", ContentFile(icono.read()))
            icono_url = filename 

        categoria = CategoriaClases.objects.create(
            nombre_categoria=nombre,
            descripcion=subtitulo + "-" + descripcion,
            edad_minima=edad_minima_int,
            icono=icono_url
        )
        return JsonResponse({
            "id": categoria.id,
            "nombre": categoria.nombre_categoria,
            "subtitulo": splitfilters.split_before(categoria.descripcion, '-'),
            "descripcion": splitfilters.split_after(categoria.descripcion, '-'),
            "edad_minima": categoria.edad_minima,
            "icono": categoria.icono.url if categoria.icono else None
        })
    return JsonResponse({"error": "Método no permitido"}, status=405)

#update categorias
@csrf_exempt
def editarCategoria(request, id):
    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip()
        subtitulo = request.POST.get("subtitulo", "")
        descripcion = request.POST.get("descripcion", "")
        edad_minima = request.POST.get("edad_minima", "")

        # Validar edad mínima
        try:
            edad_minima_int = int(edad_minima)
            if edad_minima_int < 7 or edad_minima_int > 120:
                return JsonResponse({"error": "La edad mínima debe estar entre 7 y 120."}, status=400)
        except ValueError:
            return JsonResponse({"error": "La edad mínima debe ser un número válido."}, status=400)

        if CategoriaClases.objects.filter(nombre_categoria__iexact=nombre).exclude(id=id).exists():
            return JsonResponse({"error": "Ya existe una categoría con ese nombre."}, status=400)


        
        categoria = CategoriaClases.objects.get(id=id)

        #tambien actualizar en las colecciones de mongo, preguntas, user_videos_curso y cursos
        MongoPreguntas.objects.filter(categoria_clase=categoria.nombre_categoria).update(categoria_clase=nombre)
        MongoUserVideosCurso.objects.filter(categoria_clase=categoria.nombre_categoria).update(categoria_clase=nombre)
        MongoCursos.objects.filter(categoria_clase=categoria.nombre_categoria).update(categoria_clase=nombre)

        categoria.nombre_categoria = nombre
        categoria.descripcion = subtitulo + "-" + descripcion
        categoria.edad_minima = edad_minima_int

        # Si hay nueva imagen, reemplaza; si no, deja la actual
        icono = request.FILES.get('icono')
        if icono:
            ext = os.path.splitext(icono.name)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.avif', '.svg']:
                return JsonResponse({"error": "Solo se permiten imágenes JPG, PNG, GIF, WEBP, AVIF o SVG."}, status=400)
            if icono.size > 10 * 1024 * 1024:
                return JsonResponse({"error": "La imagen no debe superar los 10MB."}, status=400)
            categoria.icono = icono  # Django se encarga de guardarla

        #actualizar data en postgres
        categoria.save()

        
        return JsonResponse({
            "id": categoria.id,
            "nombre": categoria.nombre_categoria,
            "subtitulo": splitfilters.split_before(categoria.descripcion, '-'),
            "descripcion": splitfilters.split_after(categoria.descripcion, '-'),
            "edad_minima": categoria.edad_minima,
            "icono": categoria.icono.url if categoria.icono else None
        })
    return JsonResponse({"error": "Método no permitido"}, status=405)

#delete categorias
@csrf_exempt
def eliminarCategoria(request, id):
    if request.method == "POST":
        try:
            categoria = CategoriaClases.objects.get(id=id)
            categoria.delete()
            return JsonResponse({"success": True})
        except CategoriaClases.DoesNotExist:
            return JsonResponse({"error": "Categoría no encontrada."}, status=404)
    return JsonResponse({"error": "Método no permitido"}, status=405)

def adminNiveles(request):
    return render(request, 'admin/app/niveles.html', {})

#read niveles
def nivelesJson(request):
    niveles = Niveles.objects.all().order_by('id')
    data = []
    for nivel in niveles:
        data.append({
            'id': nivel.id,
            'name': nivel.nombre,  # Ajusta el campo según tu modelo
            'description': nivel.descripcion,
        })
    return JsonResponse({'niveles': data})
#create niveles
@csrf_exempt
def crearNivel(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "").strip()

        # Validación básica
        if not name:
            return JsonResponse({"error": "El nombre del nivel es obligatorio."}, status=400)
        # Validar nombre único (case-insensitive)
        if Niveles.objects.filter(nombre__iexact=name).exists():
            return JsonResponse({"error": "Ya existe un nivel con ese nombre."}, status=400)

        #to lowercase
        name = name.lower()
        nivel = Niveles.objects.create(nombre=name, descripcion=description)
        return JsonResponse({
            "id": nivel.id,
            "name": nivel.nombre,
            "description": nivel.descripcion,
        })
    return JsonResponse({"error": "Método no permitido"}, status=405)

#update niveles
@csrf_exempt
def editarNivel(request, id):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "").strip()

        # Validación básica
        if not name:
            return JsonResponse({"error": "El nombre del nivel es obligatorio."}, status=400)
        # Validar nombre único (case-insensitive), excluyendo el actual
        if Niveles.objects.filter(nombre__iexact=name).exclude(id=id).exists():
            return JsonResponse({"error": "Ya existe un nivel con ese nombre."}, status=400)

        try:
            nivel = Niveles.objects.get(id=id)
        except Niveles.DoesNotExist:
            return JsonResponse({"error": "Nivel no encontrado."}, status=404)

        nivel.nombre = name.lower()
        nivel.descripcion = description
        nivel.save()

        return JsonResponse({
            "id": nivel.id,
            "name": nivel.nombre,
            "description": nivel.descripcion,
        })
    return JsonResponse({"error": "Método no permitido"}, status=405)
#delete niveles
@csrf_exempt
def eliminarNivel(request, id):
    if request.method == "POST":
        try:
            nivel = Niveles.objects.get(id=id)
            nivel.delete()
            return JsonResponse({"success": True})
        except Niveles.DoesNotExist:
            return JsonResponse({"error": "Nivel no encontrado."}, status=404)
    return JsonResponse({"error": "Método no permitido"}, status=405)


def adminCursos(request):   
    return render(request, 'admin/app/cursos.html', {})

#read cursos
def cursosJson(request):
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 80)) # Cambia a 80 para pruebas
    search = request.GET.get('search', '').strip().lower()

    # Filtrado por búsqueda (opcional)
    cursos_qs = MongoCursos.objects.all()
    if search:
        cursos_qs = cursos_qs.filter(titulo__icontains=search)  # Ajusta el campo según tu modelo

    cursos_qs = cursos_qs.order_by('-id')
    paginator = Paginator(cursos_qs, page_size)
    page_obj = paginator.get_page(page)

    cursos_data = []
    for curso in page_obj.object_list:
        # Obtener el icono
        icon_value = curso.icono if hasattr(curso, 'icono') else None

        # Determinar si es un link externo o recurso local
        if icon_value:
            if str(icon_value).startswith('http://') or str(icon_value).startswith('https://'):
                icon_type = 'external'
                icon_url = str(icon_value)
            else:
                icon_type = 'media'
                icon_url = icon_value.url if hasattr(icon_value, 'url') else str(icon_value)
        else:
            icon_type = None
            icon_url = None

        cursos_data.append({
            'id': str(curso.id),
            'title': curso.titulo if hasattr(curso, 'titulo') else curso.nombre,
            'description': curso.descripcion,
            'icon': icon_url,
            'icon_type': icon_type,  # <-- Aquí agregas el tipo
            'status': curso.estado if hasattr(curso, 'estado') else "activo",
            'category': curso.categoria_clase,
            'level': curso.nivel if hasattr(curso, 'nivel') else None,
            'students': getattr(curso, 'estudiantes', 0),
            'videos': MongoVideos.objects.filter(idCurso=curso.id).count(),
            'date': curso.fecha_creacion.strftime('%Y-%m-%d') if hasattr(curso, 'fecha_creacion') else "",
        })

    # Categorías y niveles igual que antes
    categorias = CategoriaClases.objects.all().order_by('nombre_categoria')
    categorias_data = [{'id': cat.id, 'name': cat.nombre_categoria} for cat in categorias]
    niveles = Niveles.objects.all().order_by('id')
    niveles_data = [{'id': nivel.id, 'name': nivel.nombre} for nivel in niveles]

    return JsonResponse({
        'cursos': cursos_data,
        'categorias': categorias_data,
        'niveles': niveles_data,
        'total': paginator.count,
        'num_pages': paginator.num_pages,
        'current_page': page_obj.number,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
    })

#create cursos
@csrf_exempt
def crearCurso(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        status = request.POST.get("status", "activo")
        category = request.POST.get("category", "")
        level = request.POST.get("level", "")
        # Manejo de icono (imagen)
        icono = request.FILES.get('icon')
        icon_url = None
        if icono:
            # Validaciones de tamaño y tipo aquí si lo deseas
            from django.core.files.storage import default_storage
            filename = default_storage.save(f"imagenes/{icono.name}", icono)
            icon_url = default_storage.url(filename)

        # Validación básica
        if not title or not category or not level:
            return JsonResponse({"error": "Título, categoría y nivel son obligatorios."}, status=400)
        
        
        # Crear el curso en Mongo
        curso = MongoCursos(
            titulo=title,
            descripcion=description,
            icono=icon_url,
            duracion=0,
            fecha_creacion=datetime.now(),
            estado=status,
            categoria_clase=category,
            idCuestionario=ObjectId(),
            nivel=level,           
        )
        curso.save()

        return JsonResponse({
            "id": str(curso.id),
            "title": curso.titulo,
            "description": curso.descripcion,
            "icon": curso.icono,
            "status": curso.estado,
            "category": curso.categoria_clase,
            "level": curso.nivel,
            "videos": 0,
            "date": curso.fecha_creacion.strftime('%Y-%m-%d'),
        })
    return JsonResponse({"error": "Método no permitido"}, status=405)

#update cursos
def editarCurso(request, id):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        status = request.POST.get("status", "activo")
        category = request.POST.get("category", "")
        level = request.POST.get("level", "")
        icono = request.FILES.get('icon')
        icon_url = None

        # Validación básica
        if not title or not category or not level:
            return JsonResponse({"error": "Título, categoría y nivel son obligatorios."}, status=400)

        # Validar nombre único (case-insensitive), excluyendo el actual
        if MongoCursos.objects.filter(
            titulo__iexact=title,
            categoria_clase=category,
            id__ne=ObjectId(id)
            ).first():
            return JsonResponse({"error": "Ya existe un curso con ese título."}, status=400)

        curso = MongoCursos.objects.get(id=ObjectId(id))
        curso.titulo = title
        curso.descripcion = description
        curso.estado = status
        curso.categoria_clase = category
        curso.nivel = level

        # Manejo de icono (imagen)
        if icono:
            from django.core.files.storage import default_storage
            filename = default_storage.save(f"imagenes/{icono.name}", icono)
            icon_url = default_storage.url(filename)
            curso.icono = icon_url

        curso.save()

        return JsonResponse({
            "id": str(curso.id),
            "title": curso.titulo,
            "description": curso.descripcion,
            "icon": curso.icono,
            "status": curso.estado,
            "category": curso.categoria_clase,
            "level": curso.nivel,
            "videos": MongoVideos.objects.filter(idCurso=curso.id).count(),
            "date": curso.fecha_creacion.strftime('%Y-%m-%d') if curso.fecha_creacion else "",
        })
    return JsonResponse({"error": "Método no permitido"}, status=405)

def adminVideos(request):
    return render(request, 'admin/app/videos.html', {})

#read videos
def videosJson(request):
    # Videos de Mongo
    videos = MongoVideos.objects.all().order_by('-fecha_creacion')
    videos_data = []
    for video in videos:
        videos_data.append({
            'id': str(video.id),
            'name': video.nombre,
            'video_file': video.ruta,
            'description': video.descripcion,
            'min_age': video.edadMinima or 0,
            'course_id': str(video.idCurso.id) if video.idCurso else '',
            'duration': video.duracion or 0,
            'created_at': video.fecha_creacion.strftime('%Y-%m-%d') if video.fecha_creacion else '',
            'thumbnail': video.imagen,
            'video_url': video.ruta,  # o la URL pública si la tienes           
            'views': getattr(video, 'cantidad_vistas', 0),
            'likes': getattr(video, 'cantidad_likes', 0),
            
        })

    # Cursos de Mongo
    cursos = MongoCursos.objects.filter(estado="activo").order_by('titulo')
    cursos_data = []
    for curso in cursos:
        cursos_data.append({
            'id': str(curso.id),
            'name': curso.titulo,
            'category_id': curso.categoria_clase,  # Aquí es el nombre, puedes mapearlo a id si lo necesitas
        })

    # Categorías de Postgres
    categorias = CategoriaClases.objects.all().order_by('nombre_categoria')
    categorias_data = []
    for categoria in categorias:
        categorias_data.append({
            'id': categoria.id,
            'name': categoria.nombre_categoria,
        })

    return JsonResponse({
        'videos': videos_data,
        'courses': cursos_data,
        'categories': categorias_data,
    })
#cursos por categoria para admin de videos
def cursos_por_categoria_json(request):
    category = request.GET.get('category')
    cursos = MongoCursos.objects.filter(estado="activo", categoria_clase=category).order_by('titulo')
    cursos_data = [
        {'id': str(c.id), 'name': c.titulo, 'category_id': c.categoria_clase}
        for c in cursos
    ]
    return JsonResponse({'courses': cursos_data})

#create videos
@csrf_exempt
def crearVideo(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "").strip()
        min_age = int(request.POST.get("min_age", 0))
        course_id = request.POST.get("course_id", "")
        video_file = request.FILES.get("video_file")
        thumbnail = request.FILES.get("thumbnail")
        duration = int(request.POST.get("duration", 0))

        # Validaciones básicas
        if not name or not course_id or not video_file:
            return JsonResponse({"error": "Nombre, curso y archivo de video son obligatorios."}, status=400)

        # Guardar archivo de video
        from django.core.files.storage import default_storage
        video_path = default_storage.save(f"videos/{video_file.name}", video_file)
        video_url = default_storage.url(video_path)

        # Guardar imagen de portada (opcional)
        thumbnail_url = ""
        if thumbnail:
            thumb_path = default_storage.save(f"thumbnails/{thumbnail.name}", thumbnail)
            thumbnail_url = default_storage.url(thumb_path)

        # Buscar curso
        try:
            curso = MongoCursos.objects.get(id=ObjectId(course_id))
        except MongoCursos.DoesNotExist:
            return JsonResponse({"error": "Curso no encontrado."}, status=404)

        # Crear video en Mongo
        video = MongoVideos(
            nombre=name,
            ruta=video_url,
            descripcion=description,
            edadMinima=min_age,
            idCurso=curso,            
            duracion=duration,
            fecha_creacion=datetime.now(),
            fecha_modificacion=datetime.now(),
            imagen=thumbnail_url,           
            cantidad_vistas=0,
            cantidad_likes=0,
        )
        video.save()

        # Sumar duración al curso
        curso.duracion = (curso.duracion or 0) + duration
        curso.save()

        return JsonResponse({
            "id": str(video.id),
            "name": video.nombre,
            "video_url": video.ruta,
            "description": video.descripcion,
            "min_age": video.edadMinima,
            "course_id": str(curso.id),
            "duration": video.duracion,            
            "created_at": video.fecha_creacion.strftime('%Y-%m-%d'),
            "updated_at": video.fecha_modificacion.strftime('%Y-%m-%d'),
            "thumbnail": video.imagen,
            "views": video.cantidad_vistas,
            "likes": video.cantidad_likes,            
        })
    return JsonResponse({"error": "Método no permitido"}, status=405)

#update videos
@csrf_exempt
def editarVideo(request, id):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "").strip()
        min_age = int(request.POST.get("min_age", 0))
        course_id = request.POST.get("course_id", "")
        duration = int(request.POST.get("duration", 0))
        video_file = request.FILES.get("video_file")
        thumbnail = request.FILES.get("thumbnail")

        if not name or not course_id:
            return JsonResponse({"error": "Nombre y curso son obligatorios."}, status=400)

        try:
            video = MongoVideos.objects.get(id=ObjectId(id))
        except MongoVideos.DoesNotExist:
            return JsonResponse({"error": "Video no encontrado."}, status=404)

        try:
            curso_nuevo = MongoCursos.objects.get(id=ObjectId(course_id))
        except MongoCursos.DoesNotExist:
            return JsonResponse({"error": "Curso no encontrado."}, status=404)

        curso_anterior = video.idCurso  # Puede ser el mismo o diferente
        duracion_anterior = video.duracion or 0
        archivo_cambiado = bool(video_file)
        curso_cambiado = str(curso_anterior.id) != str(curso_nuevo.id)

        video.nombre = name
        video.descripcion = description
        video.edadMinima = min_age
        video.idCurso = curso_nuevo

        from django.core.files.storage import default_storage
        if video_file:
            video_path = default_storage.save(f"videos/{video_file.name}", video_file)
            video.ruta = default_storage.url(video_path)
            video.duracion = duration  # Nueva duración
        else:
            video.duracion = duration  # Puede que solo se edite el nombre, etc.

        if thumbnail:
            thumb_path = default_storage.save(f"thumbnails/{thumbnail.name}", thumbnail)
            video.imagen = default_storage.url(thumb_path)

        video.save()

        # --- Actualización de duración en cursos ---
        # Si cambió de curso, restar al anterior y sumar al nuevo
        if curso_cambiado:
            # Restar al curso anterior
            curso_anterior.duracion = (curso_anterior.duracion or 0) - duracion_anterior
            if curso_anterior.duracion < 0:
                curso_anterior.duracion = 0
            curso_anterior.save()
            # Sumar al curso nuevo
            curso_nuevo.duracion = (curso_nuevo.duracion or 0) + video.duracion
            curso_nuevo.save()
        # Si no cambió de curso y cambió el archivo, actualiza la duración
        elif archivo_cambiado:
            curso_nuevo.duracion = (curso_nuevo.duracion or 0) - duracion_anterior + duration
            if curso_nuevo.duracion < 0:
                curso_nuevo.duracion = 0
            curso_nuevo.save()

        return JsonResponse({
            "id": str(video.id),
            "name": video.nombre,
            "description": video.descripcion,
            "min_age": video.edadMinima,
            "course_id": str(curso_nuevo.id),
            "video_url": video.ruta,
            "thumbnail": video.imagen,
            "duration": video.duracion,
            "views": video.cantidad_vistas,
            "likes": video.cantidad_likes,
            "updated_at": video.fecha_modificacion.strftime('%Y-%m-%d'),
            "created_at": video.fecha_creacion.strftime('%Y-%m-%d')
        })
    return JsonResponse({"error": "Método no permitido"}, status=405)
#delete videos
@csrf_exempt
def eliminarVideo(request, id):
    if request.method == "POST":
        try:
            video = MongoVideos.objects.get(id=ObjectId(id))
        except MongoVideos.DoesNotExist:
            return JsonResponse({"error": "Video no encontrado."}, status=404)

        # Guarda datos antes de borrar
        duracion_video = video.duracion or 0
        curso = video.idCurso

        # Elimina el video
        video.delete()

        # Resta la duración al curso
        if curso:
            curso.duracion = (curso.duracion or 0) - duracion_video
            if curso.duracion < 0:
                curso.duracion = 0
            curso.save()

        return JsonResponse({"success": True})
    return JsonResponse({"error": "Método no permitido"}, status=405)

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


