import json
from django.conf import settings
from django_seed import Seed
from django.core.management.base import BaseCommand, CommandParser
from contenidos.models import Videos

class Command(BaseCommand):
    help = 'Seeder inicial de Videos, Data: seeders/videos.json'

    def add_arguments(self, parser):
        parser.add_argument(
            '--total',
            type=int,
            default=0,
            help='Número adicional de videos falsos a generar'
        )
        

    def handle(self, *args, **options):
        json_path = settings.BASE_DIR / 'contenidos' / 'seeders' / 'videos.json'

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                videos_data = json.load(f)

                for video_data in videos_data:
                    Videos.objects.get_or_create(
                        video_url=video_data['video_url'],
                        defaults=video_data
                    )
                self.stdout.write(self.style.SUCCESS(f'{len(videos_data)} videos cargados desde JSON : seeders/videos.json'))
                
        except FileNotFoundError:
            self.stdout.write(self.style.WARNING('Archivo videos.json no encontrado'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Error al leer el archivo JSON'))
            
            