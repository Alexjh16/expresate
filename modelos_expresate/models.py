from django.db import models
#from django.contrib.auth.models import User
 
class CategoriaClases(models.Model):
    nombre_categoria = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.nombre_categoria


class Videos(models.Model):
    imagen = models.ImageField(upload_to='imagenes', blank=False, null=False)
    video = models.FileField(upload_to='videos', blank=False, null=False)
    nombre_sena = models.CharField(max_length=50, blank=False, null=True)
    
    def __str__(self):
        return self.nombre_sena


"""class Usuarios_videos_categoria(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    videos = models.ForeignKey(Videos, on_delete=models.CASCADE)
    estadoVideo = models.BooleanField(default=False, blank=False, null=False)
    
    def __str__(self):
        return f'{self.usuario.nombre} - {self.videos.nombre_sena} - {self.videos.id}'
"""
    
class VideosCategoriaClase(models.Model):  
    categoriaClases = models.ForeignKey(CategoriaClases, on_delete=models.CASCADE)  
    videos = models.ForeignKey(Videos, on_delete=models.CASCADE) 

    def __str__(self):
        return f'{self.categoriaClases} - {self.videos}'  


class NotasCategoria(models.Model):
    nombre_categoria_notas = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.nombre_categoria_notas