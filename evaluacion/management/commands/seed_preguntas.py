import json
from django.conf import settings
from django_seed import Seed
from django.core.management.base import BaseCommand, CommandParser
from evaluacion.models import Preguntas

class Command(BaseCommand):
    help = 'Seeder inicial de Preguntas, Data: seeders/preguntas.json'

    def add_arguments(self, parser):
        parser.add_argument(
            '--total',
            type=int,
            default=0,
            help='Número adicional de preguntas falsas a generar'
        )
        

    def handle(self, *args, **options):
        json_path = settings.BASE_DIR / 'evaluacion' / 'seeders' / 'preguntas.json'

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                preguntas_data = json.load(f)

                for pregunta_data in preguntas_data:
                    Preguntas.objects.get_or_create(
                        pregunta=pregunta_data['pregunta'],
                        defaults=pregunta_data
                    )
                self.stdout.write(self.style.SUCCESS(f'{len(preguntas_data)} preguntas cargados desde JSON : seeders/preguntas.json'))
                
        except FileNotFoundError:
            self.stdout.write(self.style.WARNING('Archivo preguntas.json no encontrado'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Error al leer el archivo JSON'))
            
            