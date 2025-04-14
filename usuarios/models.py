from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
#tablas o entidades

#auth_user
#rol_user
#pais



class Pais(models.Model):
    nombre_pais = models.CharField(max_length=100)
    codigo_pais = models.CharField(max_length=10)
    codigo_iso = models.CharField(max_length=5)
    idioma_principal = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.nombre_pais} - {self.codigo_iso}'

    class Meta:
        db_table = "paises"
        verbose_name = 'Pais'
        verbose_name_plural = 'Paises'
        ordering = ['nombre_pais']

class RolUser(models.Model):
    nombre_rol = models.CharField(max_length=50)
    descripcion_rol = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'rol_user'

    def __str__(self):
        return f'{self.nombre_rol} - {self.descripcion_rol}'

class Usuario(AbstractUser):
    foto = models.CharField(max_length=128, blank=True, null=True)
    edad = models.IntegerField(null=True, blank=True)
    dispositivo = models.CharField(max_length=100, null=True, blank=True)
    pais = models.ForeignKey(Pais, on_delete=models.SET_NULL, null=True, blank=True)
    rol = models.ForeignKey(RolUser, on_delete=models.PROTECT)
    
    class Meta:
        db_table = 'usuarios'

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="usuarios_groups",
        related_query_name="usuario",
    )

    permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='permissions',
        blank=True,
        help_text='Specific permissions for this  user.',
        related_name="usuarios_permissions", 
        related_query_name="usuario",
    )