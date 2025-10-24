from django.db import models
from django.contrib.auth.models import AbstractUser


#tablas o entidades

#paises
#roles_user
#users

class Paises(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10)
    indicativo = models.CharField(max_length=10)
    codigo_iso = models.CharField(max_length=5)
    idioma_principal = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.nombre} - {self.codigo_iso}'

    class Meta:
        db_table = "paises"
        verbose_name = 'Pais'
        verbose_name_plural = 'Paises'
        ordering = ['nombre']

class RolesUser(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'roles_user'
        verbose_name_plural = 'Roles_user'

    def __str__(self):
        return f'{self.nombre} - {self.descripcion}'

class Users(AbstractUser):
    foto = models.URLField(null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    dispositivo = models.CharField(max_length=100, null=True, blank=True)
    pais = models.ForeignKey(Paises, on_delete=models.SET_NULL, null=True, blank=True)
    rol = models.ForeignKey(RolesUser, on_delete=models.PROTECT)
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='users_user_permissions',
        related_query_name='users',
    )
    
    class Meta:
        db_table = 'users'

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="users_groups",
        related_query_name="users",
    )

    permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='permissions',
        blank=True,
        help_text='Specific permissions for this  user.',
        related_name="users_permissions", 
        related_query_name="users",
    )