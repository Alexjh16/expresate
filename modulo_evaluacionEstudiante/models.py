from django.db import models
from django.contrib.auth.models import User
from modelos_expresate.models import CategoriaClases

#Modelos de Evaluation students
class Preguntas(models.Model):
    pregunta = models.CharField(max_length=255, null=False, blank=True)
    imagen = models.ImageField(upload_to='imagenes/imagenes_evaluacion', blank=True, null=True)
    video = models.FileField(upload_to='videos/videos_evaluacion', blank=True, null=True)
    
    respuesta1 = models.CharField(max_length=255, blank=False, null=False)
    respuesta2 = models.CharField(max_length=255, blank=False, null=False)
    respuesta3 = models.CharField(max_length=255, blank=False, null=False)
    respuesta4 = models.CharField(max_length=255, blank=False, null=False)
    
    respuesta_correcta = models.CharField(null=False, blank=False, max_length=100)
    categoriaClases = models.ForeignKey(CategoriaClases, on_delete=models.CASCADE)
        
    def __str__(self):
        return self.categoriaClases.nombre_categoria

"""class Notas(models.Model):
    nombre_categoria = models.CharField(null=False, blank=True, max_length=50)
    respuestas_buenas = models.IntegerField(null=False, blank=True)
    respuestas_malas = models.IntegerField(null=False, blank=True)
    nota = models.FloatField(null=False, blank=True, default= 0.0)
    estado = models.CharField(null=False, blank=True, max_length=15)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre_categoria
   """ 