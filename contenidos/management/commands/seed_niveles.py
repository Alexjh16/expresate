import json
from django.conf import settings
from django_seed import Seed
from django.core.management.base import BaseCommand, CommandParser
from contenidos.models import Niveles

class Command(BaseCommand):
    help = 'Seeder inicial de Niveles, Data: seeders/niveles.json'

    def add_arguments(self, parser):
        parser.add_argument(
            '--total',
            type=int,
            default=0,
            help='Número adicional de niveles falsos a generar'
        )
        

    def handle(self, *args, **options):
        json_path = settings.BASE_DIR / 'contenidos' / 'seeders' / 'niveles.json'

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                niveles_data = json.load(f)

                for nivel_data in niveles_data:
                    Niveles.objects.get_or_create(
                        nombre=nivel_data['nombre'],
                        defaults=nivel_data
                    )
                self.stdout.write(self.style.SUCCESS(f'{len(niveles_data)} niveles cargados desde JSON : seeders/niveles.json'))
                
        except FileNotFoundError:
            self.stdout.write(self.style.WARNING('Archivo niveles.json no encontrado'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Error al leer el archivo JSON'))
            
            