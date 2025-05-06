from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Ejecuta todos los comandos seed de la aplicación'

    def handle(self, *args, **options):
        # Lista de todos los comandos seed a ejecutar en orden
        seed_commands = [
            'seed_paises',
            'seed_roles_user',
            'seed_users',
            'seed_tipos_preguntas',
            'seed_preguntas',
            'seed_respuestas',
            'seed_niveles',
            'seed_categorias',
            'seed_cuestionarios',
            'seed_cuestionarios_preguntas',
            'seed_calificaciones',
            'seed_intentos_cuestionarios',
            'seed_cursos',
            'seed_videos',
            'seed_users_videos_cursos',
            'seed_comentarios',
            'seed_permisos_videos'

        ]

        for command in seed_commands:
            self.stdout.write(self.style.SUCCESS(f'Ejecutando {command}...'))
            try:
                call_command(command)
                self.stdout.write(self.style.SUCCESS(f'{command} completado exitosamente'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error ejecutando {command}: {str(e)}'))