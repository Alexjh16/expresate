from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('create/categoria/clase/', views.createCategoriaClases, name='create.categoriaClases'),
    path('video/clase/', views.indexCreateVideo, name='video.clases'),
    path('create/video/clase/', views.createVideoClases, name='create.videoClases'),
    path('categoria/<str:NM>/', views.moduloClase, name='categoria.clase'),
    path("clase/seletc/idVideo/", views.seletcVideo, name="clase.select"),
        
    #Ruta evaluacion de modulos
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
