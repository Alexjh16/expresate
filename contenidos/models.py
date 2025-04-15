from django.db import models
from evaluacion.models import Cuestionarios
# Create your models here.
#tablas o entidades

#video
#categoria_clase
#curso

class CategoriaClases(models.Model):
    nombre_categoria = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    icono = models.URLField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    edad_minima = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.nombre_categoria} - {self.descripcion}'
    
    class Meta:
        db_table = 'categoria_clases'
        
class Cursos(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    icono = models.URLField()
    duracion = models.FloatField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado_curso = models.BooleanField(default=False)
 
    categoria_clase = models.ForeignKey(CategoriaClases, on_delete=models.CASCADE, null=True, blank=True)
    
    cuestionario = models.ForeignKey(Cuestionarios, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        db_table = 'cursos'

class Videos(models.Model):
    video_url = models.URLField()
    descripcion = models.TextField(null=True, blank=True)
    edad_minima = models.IntegerField(null=True, blank=True)
    duracion = models.IntegerField(null=True, blank=True)
    imagen_portada = models.URLField(null=True, blank=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    curso = models.ForeignKey(Cursos, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.video_url} - {self.descripcion} - {self.fecha_subida}'
    
    class Meta:
        db_table = 'videos'


