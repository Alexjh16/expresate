import json
from django.conf import settings
from django_seed import Seed
from django.core.management.base import BaseCommand, CommandParser
from seguimiento.models import Comentarios

class Command(BaseCommand):
    help = 'Seeder inicial de Comentarios, Data: seeders/comentarios.json'

    def add_arguments(self, parser):
        parser.add_argument(
            '--total',
            type=int,
            default=0,
            help='Número adicional de comentarios falsos a generar'
        )
        

    def handle(self, *args, **options):
        json_path = settings.BASE_DIR / 'seguimiento' / 'seeders' / 'comentarios.json'

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                comentarios_data = json.load(f)

                for comentario_data in comentarios_data:
                    Comentarios.objects.create(**comentario_data)
                self.stdout.write(self.style.SUCCESS(f'{len(comentarios_data)} comentarios cargados desde JSON : seeders/comentarios.json'))
                
        except FileNotFoundError:
            self.stdout.write(self.style.WARNING('Archivo comentarios.json no encontrado'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Error al leer el archivo JSON'))
            
            