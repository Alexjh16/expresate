from . import views
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
    path('contacto/', views.contacto, name='contacto'),
    path('mision/', views.mision, name='mision'),
    
    path('vision/', views.vision, name= 'vision'),
    #
    path('menu/clases/', views.clasesOld, name='menu.clase'),
    
    path('menu/nosotros/', views.nosotrosOld, name='menu.nosotros'),
    path('menu/contacto/', views.contactoOld, name='menu.contacto'),
    path('registrar/', views.registrar, name='registrar'),
    path('login/', views.login, name='login'),
    
    #Ruta plantilla modulo
    path('modulo/clases', views.moduloClases, name='modulo.clase'),
    
    #Rutas Administrativas 
    path('base/admin/', TemplateView.as_view(template_name='view_admin/app_admin/base_admin.html'), name='base_admin'),
    path('agregar/clase', TemplateView.as_view(template_name='view_admin/agregar_categoriaClase.html'), name='categoria.clase'),
    
    #Ruta a los modulos
    path('models/expresate/', include('modelos_expresate.urls')),
    path('models/evaluacion/estudiante/', include('modulo_evaluacionEstudiante.urls')), #modulo evaliacion

    #Rutas anteriores
    path('indexOld/', views.indexOld, name='indexOld'),

    path("__reload__/", include("django_browser_reload.urls")),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
