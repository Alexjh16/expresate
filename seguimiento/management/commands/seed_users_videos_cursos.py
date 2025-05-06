import json
from django.conf import settings
from django_seed import Seed
from django.core.management.base import BaseCommand, CommandParser
from seguimiento.models import UserVideosCursos

class Command(BaseCommand):
    help = 'Seeder inicial de Users Videos Cursos, Data: seeders/usersvideoscursos.json'

    def add_arguments(self, parser):
        parser.add_argument(
            '--total',
            type=int,
            default=0,
            help='Número adicional de users-videos-cursos falsos a generar'
        )
        

    def handle(self, *args, **options):
        json_path = settings.BASE_DIR / 'seguimiento' / 'seeders' / 'usersvideoscursos.json'

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                users_videos_cursos_data = json.load(f)

                for user_video_curso_data in users_videos_cursos_data:
                    UserVideosCursos.objects.create(**user_video_curso_data)
                self.stdout.write(self.style.SUCCESS(f'{len(users_videos_cursos_data)} videos cargados desde JSON : seeders/usersvideoscursos.json'))
                
        except FileNotFoundError:
            self.stdout.write(self.style.WARNING('Archivo usersvideoscursos.json no encontrado'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Error al leer el archivo JSON'))
            
            