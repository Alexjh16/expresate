import json
from django.conf import settings
from django_seed import Seed
from django.core.management.base import CommandParser
from users.models import Paises
from expresate.management.commands.base_seeder import BaseSeederCommand

class Command(BaseSeederCommand):
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
            # Conectar a MongoDB
            if not self.connect_mongodb('paises'):
                return

            with open(json_path, 'r', encoding='utf-8') as f:
                paises_data = json.load(f)

                for pais_data in paises_data:
                    # Guardar en PostgreSQL
                    pais, created = Paises.objects.get_or_create(
                        codigo_iso=pais_data['codigo_iso'],
                        defaults=pais_data
                    )
                    
                    # Guardar en MongoDB
                    self.save_to_mongodb(pais_data, 'codigo_iso')

                self.stdout.write(self.style.SUCCESS(f'{len(paises_data)} paises cargados en PostgreSQL y MongoDB desde JSON : seeders/paises.json'))
                
        except FileNotFoundError:
            self.stdout.write(self.style.WARNING('Archivo paises.json no encontrado'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Error al leer el archivo JSON'))
        finally:
            self.close_mongodb_connection()
            
            
            
            