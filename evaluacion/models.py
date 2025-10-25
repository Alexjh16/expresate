from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
#tablas o entidades

#cuestionarios
#tipos_pregunta
#preguntas
#cuestionario_preguntas
#respuestas
#calificaciones
#intentos_cuestionario


class Cuestionarios(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(null=True, blank=True)
    limite_intentos = models.IntegerField(null=True, blank=True)
    estado = models.CharField(max_length=10, choices=[('completo', 'Completo'), ('incompleto', 'Incompleto')])
    calificacion_aprobacion = models.FloatField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    duracion_estimada = models.IntegerField(null=True, blank=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.titulo} - {self.descripcion} - {self.estado}'
    
    class Meta:
        db_table = 'cuestionarios'

class TiposPregunta(models.Model):
    nombre_tipo_pregunta = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.nombre_tipo_pregunta}'
    
    class Meta:
        db_table = 'tipos_pregunta'

class Preguntas(models.Model):
    pregunta = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo_pregunta = models.ForeignKey(TiposPregunta, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.pregunta}'
    
    class Meta:
        db_table = 'preguntas'

class CuestionarioPreguntas(models.Model):
    cuestionario = models.ForeignKey(Cuestionarios, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Preguntas, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'cuestionario_preguntas'

class Respuestas(models.Model):
    respuesta = models.CharField(max_length=250)
    es_correcta = models.BooleanField(default=False)
    veces_seleccionada = models.IntegerField(null=True, blank=True)
    pregunta = models.ForeignKey(Preguntas, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.respuesta} - {self.es_correcta}'
    
    class Meta:
        db_table = 'respuestas'

class Calificaciones(models.Model):
    calificacion = models.FloatField()
    fecha_realizacion = models.DateTimeField(auto_now_add=True)
    tiempo_empleado = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cuestionario = models.ForeignKey(Cuestionarios, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.calificacion} - {self.fecha_realizacion}'
    
    class Meta:
        db_table = 'calificaciones'

class IntentosCuestionario(models.Model):
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    calificacion_obtenida = models.FloatField(null=True, blank=True)
    estado = models.CharField(max_length=10, choices=[('completo', 'Completo'), ('incompleto', 'Incompleto')])
    tiempo_empleado = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cuestionario = models.ForeignKey(Cuestionarios, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.calificacion_obtenida} - {self.user.email}'
    
    class Meta:
        db_table = 'intentos_cuestionario'