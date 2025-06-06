# Generated by Django 5.2.1 on 2025-05-08 01:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenidos', '0001_initial'),
        ('evaluacion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cursos',
            name='cuestionario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='evaluacion.cuestionarios'),
        ),
        migrations.AddField(
            model_name='cursos',
            name='nivel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenidos.niveles'),
        ),
        migrations.AddField(
            model_name='videos',
            name='curso',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenidos.cursos'),
        ),
    ]
