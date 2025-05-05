import json
from django.conf import settings
from django_seed import Seed
from django.core.management.base import BaseCommand, CommandParser
from evaluacion.models import CuestionarioPreguntas

class Command(BaseCommand):
    help = 'Seeder inicial de Cuestionarios, Data: seeders/cuestionarios.json'

    def add_arguments(self, parser):
        parser.add_argument(
            '--total',
            type=int,
            default=0,
            help='Número adicional de cuestionarios falsos a generar'
        )
        

    def handle(self, *args, **options):
        json_path = settings.BASE_DIR / 'evaluacion' / 'seeders' / 'cuestionarios_preguntas.json'

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                cuestionarios_pregunta_data = json.load(f)

                for cuestionario_pregunta_data in cuestionarios_pregunta_data:
                     CuestionarioPreguntas.objects.create(**cuestionario_pregunta_data)
                self.stdout.write(self.style.SUCCESS(f'{len(cuestionarios_pregunta_data)} cuestionarios_preguntas cargados desde JSON : seeders/cuestionarios_preguntas.json'))
                
        except FileNotFoundError:
            self.stdout.write(self.style.WARNING('Archivo cuestionarios_preguntas.json no encontrado'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Error al leer el archivo JSON'))
            
            