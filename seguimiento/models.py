from django.db import models
from users.models import RolesUser, Users
from contenidos.models import Videos

# Create your models here.
#tablas o entidades

#user_videos_curso
#comentario
#permiso_video

class UserVideosCursos(models.Model):
    estado_video = models.BooleanField(default=False)
    fecha_video_visto = models.DateTimeField(null=True, blank=True)
    cantidad_vistas = models.IntegerField(default=0)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    video = models.ForeignKey(Videos, on_delete=models.CASCADE)
    porcentaje_video = models.FloatField(default=0)

    def __str__(self):
        return f'{self.estado_video} - {self.user.email} - {self.video.video_url}'
    
    class Meta:
        db_table = 'user_videos_cursos'

class Comentarios(models.Model):
    comentario = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    cantidad_likes = models.IntegerField(default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    video = models.ForeignKey(Videos, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.comentario} - {self.parent_id} - {self.user.email}'
    
    class Meta:
        db_table = 'comentarios'

class PermisosVideos(models.Model):
    rol_user = models.ForeignKey(RolesUser, on_delete=models.CASCADE)
    video = models.ForeignKey(Videos, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.rol_user.nombre_rol} - {self.video.video_url}'
    
    class Meta:
        db_table = 'permisos_video'

