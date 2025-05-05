import json
from django.conf import settings
from django_seed import Seed
from django.core.management.base import BaseCommand, CommandParser
from evaluacion.models import TiposPregunta

class Command(BaseCommand):
    help = 'Seeder inicial de Tipos Preguntas, Data: seeders/tipos_preguntas.json'

    def add_arguments(self, parser):
        parser.add_argument(
            '--total',
            type=int,
            default=0,
            help='Número adicional de tipos de preguntas falsos a generar'
        )
        

    def handle(self, *args, **options):
        json_path = settings.BASE_DIR / 'evaluacion' / 'seeders' / 'tipos_preguntas.json'

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                tipos_preguntas_data = json.load(f)

                for tipo_pregunta_data in tipos_preguntas_data:
                    TiposPregunta.objects.get_or_create(
                        nombre_tipo_pregunta=tipo_pregunta_data['nombre_tipo_pregunta'],
                        defaults=tipo_pregunta_data
                    )
                self.stdout.write(self.style.SUCCESS(f'{len(tipos_preguntas_data)} tipos preguntas cargados desde JSON : seeders/tipos_preguntas.json'))
                
        except FileNotFoundError:
            self.stdout.write(self.style.WARNING('Archivo tipos_preguntas.json no encontrado'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Error al leer el archivo JSON'))
            
            