from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('base-admin/', views.index, name='index.admin'),   
    path('create/categoria-clase/', views.createCategoriaClases, name='create.categoriaClases'),
    #Rutas para mostrar el formulario de niveles y crearlos
    path('form/nivel-curso/', views.formCreateNivele, name='form.create.nivel'),
    path('create/nivel-curso/', views.createNivele, name='create.nivel'),
    #Rutas para mostrar el formulario de cursos y crearlos
    path('form/curso/', views.formCreateCurso, name='form.create.curso'),
    path('create/curso/', views.createCurso, name='create.curso'),
    #Rutas para mostrar el formulario de videos y crearlos
    path('form/video/', views.formCreateVideo, name='form.create.video'),
    path('create/video/', views.createVideo, name='create.video'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)