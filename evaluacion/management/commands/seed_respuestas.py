import json
from django.conf import settings
from django_seed import Seed
from django.core.management.base import BaseCommand, CommandParser
from evaluacion.models import Respuestas

class Command(BaseCommand):
    help = 'Seeder inicial de Respuestas, Data: seeders/respuestas.json'

    def add_arguments(self, parser):
        parser.add_argument(
            '--total',
            type=int,
            default=0,
            help='Número adicional de respuestas falsas a generar'
        )
        

    def handle(self, *args, **options):
        json_path = settings.BASE_DIR / 'evaluacion' / 'seeders' / 'respuestas.json'

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                respuestas_data = json.load(f)

                for respuesta_data in respuestas_data:
                    Respuestas.objects.get_or_create(
                        respuesta=respuesta_data['respuesta'],
                        defaults=respuesta_data
                    )
                self.stdout.write(self.style.SUCCESS(f'{len(respuestas_data)} respuestas cargados desde JSON : seeders/respuestas.json'))
                
        except FileNotFoundError:
            self.stdout.write(self.style.WARNING('Archivo respuestas.json no encontrado'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Error al leer el archivo JSON'))
            
            