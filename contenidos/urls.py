from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
       path('curso/<str:idCurso>/', views.curso, name='curso'),   
       path('curso/<str:idCurso>/video/<str:idVideo>/', views.video_curso_ajax, name='video-curso-ajax'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
