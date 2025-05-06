from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('create/usuario/', views.createRegistroUsuario, name='createRegistroUsuario'),
    
    path('video/clase/', views.indexCreateVideo, name='video.clases'),
    path('create/video/clase/', views.createVideoClases, name='create.videoClases'),
    path('modulo/family/<str:NM>/', views.moduloClase, name='modulo.family'),
    path("clase/seletc/idVideo/", views.seletcVideo, name="clase.select"),
    path('login/session/', views.login, name='login.session'),
    path('cerrar/session/', views.logout, name='logout.session'),
    
    #Ruta evaluacion de modulos
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)