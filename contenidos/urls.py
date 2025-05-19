from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
       path('select-categorias/<str:nombreCurso>/', views.selectCategoria, name='selec.categorias'),   
       path('contenidos/', views.selectContenidos, name='select.contenidos'),
       path('select-video/<int:idVideo>', views.selectVideo, name='select.video')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
