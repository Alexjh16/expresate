import json
from django.conf import settings
from django_seed import Seed
from django.core.management.base import BaseCommand, CommandParser
from seguimiento.models import PermisosVideos

class Command(BaseCommand):
    help = 'Seeder inicial de Permisos Videos, Data: seeders/permisosvideos.json'

    def add_arguments(self, parser):
        parser.add_argument(
            '--total',
            type=int,
            default=0,
            help='Número adicional de permisos videos falsos a generar'
        )
        

    def handle(self, *args, **options):
        json_path = settings.BASE_DIR / 'seguimiento' / 'seeders' / 'permisosvideos.json'

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                permisos_videos_data = json.load(f)

                for permiso_video_data in permisos_videos_data:
                    PermisosVideos.objects.create(**permiso_video_data)
                self.stdout.write(self.style.SUCCESS(f'{len(permisos_videos_data)} niveles cargados desde JSON : seeders/permisosvideos.json'))
                
        except FileNotFoundError:
            self.stdout.write(self.style.WARNING('Archivo permisosvideos.json no encontrado'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Error al leer el archivo JSON'))
            
            