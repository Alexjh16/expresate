from django.urls import path
from . import views

urlpatterns = [
    path('evaluacion/modulo/<str:NME>/', views.evaluacionModulo, name='evaluacion.modulo'),#NME = nombre modulo evaluacion
    path('index/crear/evaluacion/', views.indexCrearPreguntas , name='index.crear.evaluacion'),
    path('crear/pregunta/', views.crearPreguntas , name='crear.pregunta'),
    path('nota/', views.notas, name='notas'),
]