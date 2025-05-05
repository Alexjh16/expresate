import json
from django.conf import settings
from django_seed import Seed
from django.core.management.base import BaseCommand, CommandParser
from evaluacion.models import Calificaciones

class Command(BaseCommand):
    help = 'Seeder inicial de Calificaciones, Data: seeders/calificaciones.json'

    def add_arguments(self, parser):
        parser.add_argument(
            '--total',
            type=int,
            default=0,
            help='Número adicional de calificaciones falsas a generar'
        )
        

    def handle(self, *args, **options):
        json_path = settings.BASE_DIR / 'evaluacion' / 'seeders' / 'calificaciones.json'

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                calificaciones_data = json.load(f)

                for calificacion_data in calificaciones_data:
                    Calificaciones.objects.create(**calificacion_data)
                self.stdout.write(self.style.SUCCESS(f'{len(calificaciones_data)} calificaciones cargados desde JSON : seeders/calificaciones.json'))
                
        except FileNotFoundError:
            self.stdout.write(self.style.WARNING('Archivo calificaciones.json no encontrado'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Error al leer el archivo JSON'))
            
            