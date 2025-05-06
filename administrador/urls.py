from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('base-admin/', views.index, name='index.admin'),   
    path('create/categoria-clase/', views.createCategoriaClases, name='create.categoriaClases'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
