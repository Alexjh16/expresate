# Generated by Django 5.2.1 on 2025-05-08 01:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PermisosVideos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'permisos_video',
            },
        ),
        migrations.CreateModel(
            name='UserVideosCursos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado_video', models.BooleanField(default=False)),
                ('fecha_video_visto', models.DateTimeField(blank=True, null=True)),
                ('cantidad_vistas', models.IntegerField(default=0)),
                ('porcentaje_video', models.FloatField(default=0)),
            ],
            options={
                'db_table': 'user_videos_cursos',
            },
        ),
        migrations.CreateModel(
            name='Comentarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.TextField()),
                ('cantidad_likes', models.IntegerField(default=0)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='seguimiento.comentarios')),
            ],
            options={
                'db_table': 'comentarios',
            },
        ),
    ]
