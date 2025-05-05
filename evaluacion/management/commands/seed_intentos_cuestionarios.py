import json
from django.conf import settings
from django_seed import Seed
from django.core.management.base import BaseCommand, CommandParser
from evaluacion.models import IntentosCuestionario

class Command(BaseCommand):
    help = 'Seeder inicial de Intento cuestionarios, Data: seeders/intentos_cuestionarios.json'

    def add_arguments(self, parser):
        parser.add_argument(
            '--total',
            type=int,
            default=0,
            help='Número adicional de cuestionarios falsos a generar'
        )
        

    def handle(self, *args, **options):
        json_path = settings.BASE_DIR / 'evaluacion' / 'seeders' / 'intentos_cuestionarios.json'

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                intentos_cuestionarios_data = json.load(f)

                for cuestionario_data in intentos_cuestionarios_data:
                    IntentosCuestionario.objects.create(**cuestionario_data)
                self.stdout.write(self.style.SUCCESS(f'{len(intentos_cuestionarios_data)} intentos cuestionarios cargados desde JSON : seeders/intentos_cuestionarios.json'))
                
        except FileNotFoundError:
            self.stdout.write(self.style.WARNING('Archivo intentos_cuestionarios.json no encontrado'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Error al leer el archivo JSON'))
            
            