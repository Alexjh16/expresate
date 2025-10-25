# Generated manually to alter FK to users

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evaluacion', '0002_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calificaciones',
            name='user',
            field=models.ForeignKey(on_delete=models.CASCADE, to='users.users'),
        ),
        migrations.AlterField(
            model_name='cuestionarios',
            name='autor',
            field=models.ForeignKey(on_delete=models.CASCADE, to='users.users'),
        ),
        migrations.AlterField(
            model_name='intentoscuestionario',
            name='user',
            field=models.ForeignKey(on_delete=models.CASCADE, to='users.users'),
        ),
        migrations.AlterField(
            model_name='preguntas',
            name='autor',
            field=models.ForeignKey(on_delete=models.CASCADE, to='users.users'),
        ),
    ]