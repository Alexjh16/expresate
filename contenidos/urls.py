from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
       path('curso/<str:nombreCurso>/', views.curso, name='curso'),   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
