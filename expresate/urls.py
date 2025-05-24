from . import views
from users.views import altcha_challenge
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    
    #Rutas a clases y a usuarios 


    
    #ruta de inicio para / y para /index
    path('', views.index, name='index'),

    #path('bds/', views.dbs, name='bds'),
    

    #Rutas agregadas por Jhon Alexander
    path('index/', views.index, name='index'),
    path('clases/', views.clases, name='clases'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('cursos/<str:categoria>/', views.cursos, name='cursos'),
    path('descripcion-curso/<str:idCurso>/', views.descripcionCurso, name='descripcion-curso'),
    path('registrar/', views.registrar, name='registrar'),
    path('login/', views.login, name='login'),

    #Ruta a la vista de admin
    path('login-admin/', views.adminLogin, name='login-admin'),
    path('dashboard-admin/', views.adminDashboard, name='dashboard-admin'),
    path('dashboard-admin/usuarios/', views.adminUsuarios, name='admin-usuarios'),
    path('dashboard-admin/categorias/', views.adminCategorias, name='admin-categorias'),
    #ruta para listar categorias
    path('admin/categorias/json/', views.categoriasJson, name='admin-categorias-json'),
    #ruta para crear categorias
    path('admin/categorias/crear/', views.crearCategoria, name='admin-categorias-crear'),
    #ruta para editar categorias
    path('admin/categorias/editar/<int:id>/', views.editarCategoria, name='admin-categorias-editar'),
    #ruta para eliminar categorias
    path('admin/categorias/eliminar/<int:id>/', views.eliminarCategoria, name='admin-categorias-eliminar'),
    path('dashboard-admin/niveles/', views.adminNiveles, name='admin-niveles'),
    #ruta para listar niveles
    path('admin/niveles/json/', views.nivelesJson, name='admin-niveles-json'),
    #ruta para crear niveles
    path('admin/niveles/crear/', views.crearNivel, name='admin-niveles-crear'),
    #ruta para editar niveles
    path('admin/niveles/editar/<int:id>/', views.editarNivel, name='admin-niveles-editar'),
    #ruta para eliminar niveles
    path('admin/niveles/eliminar/<int:id>/', views.eliminarNivel, name='admin-niveles-eliminar'),
    path('dashboard-admin/cursos/', views.adminCursos, name='admin-cursos'),
    #ruta para listar cursos
    path('admin/cursos/json/', views.cursosJson, name='admin-cursos-json'),
    #ruta para crear cursos
    path('admin/cursos/crear/', views.crearCurso, name='admin-cursos-crear'),
    #ruta para editar cursos
    path('admin/cursos/editar/<str:id>/', views.editarCurso, name='admin-cursos-editar'),
    path('dashboard-admin/videos/', views.adminVideos, name='admin-videos'),  
    #ruta para listar videos
    path('admin/videos/json/', views.videosJson, name='admin-videos-json'),
    #ruta para cursos por categoria para admin de videos
    path('admin/cursos/categoria/json/', views.cursos_por_categoria_json, name='admin-cursos-cateogoria-json'),
    #ruta para crear videos
    path('admin/videos/crear/', views.crearVideo, name='admin-videos-crear'),
    #ruta para editar videos
    path('admin/videos/editar/<str:id>/', views.editarVideo, name='admin-videos-editar'),
    #ruta para eliminar videos
    path('admin/videos/eliminar/<str:id>/', views.eliminarVideo, name='admin-videos-eliminar'),

    
    
    #Ruta a al modulo de Registro de usuarios
    path('altcha-challenge/', altcha_challenge, name='altcha_challenge'),
    path('users/', include('users.urls')),
    
    #
    path('menu/clases/', views.clasesOld, name='menu.clase'),
    
    path('menu/nosotros/', views.nosotrosOld, name='menu.nosotros'),
    path('menu/contacto/', views.contactoOld, name='menu.contacto'),
    path('registrarOld/', views.registrarOld, name='registrarOld'),
    path('loginOld/', views.loginOld, name='loginOld'),
    
    #Ruta plantilla modulo
    path('modulo/clases', views.moduloClases, name='modulo.clase'),
    
    #Rutas Administrativas 
    path('base/admin/', TemplateView.as_view(template_name='view_admin/app_admin/base_admin.html'), name='base_admin'),
    path('agregar/clase', TemplateView.as_view(template_name='view_admin/agregar_categoriaClase.html'), name='categoria.clase'),
    
    #Ruta a contenidos
    path('contenido/', include('contenidos.urls')),

    
    path('models/evaluacion/estudiante/', include('modulo_evaluacionEstudiante.urls')), #modulo evaliacion

    #Rutas anteriores
    path('indexOld/', views.indexOld, name='indexOld'),

    path("__reload__/", include("django_browser_reload.urls")),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
