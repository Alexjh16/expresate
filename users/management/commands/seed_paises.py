import json
from django.conf import settings
from django_seed import Seed
from django.core.management.base import BaseCommand, CommandParser
from users.models import Paises

class Command(BaseCommand):
    help = 'Seeder inicial de Paises, Data: seeders/paises.json'

    def add_arguments(self, parser):
        parser.add_argument(
            '--total',
            type=int,
            default=0,
            help='Número adicional de paises falsos a generar'
        )
        

    def handle(self, *args, **options):
        json_path = settings.BASE_DIR / 'users' / 'seeders' / 'paises.json'

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                paises_data = json.load(f)

                for pais_data in paises_data:
                    Paises.objects.get_or_create(
                        codigo_iso=pais_data['codigo_iso'],
                        defaults=pais_data
                    )
                self.stdout.write(self.style.SUCCESS(f'{len(paises_data)} paises cargados desde JSON : seeders/paises.json'))
                
        except FileNotFoundError:
            self.stdout.write(self.style.WARNING('Archivo paises.json no encontrado'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Error al leer el archivo JSON'))
            
            