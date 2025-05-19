from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #Rutas para mostrar el formulario de cuestionarios y crearlos
    path('form/cuestionario/', views.formCreateCuestionario, name='form.create.cuestionario'),
    path('create/cuestionario/', views.createCuestionario, name='create.cuestionario'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)