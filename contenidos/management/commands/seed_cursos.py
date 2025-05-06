import json
from django.conf import settings
from django_seed import Seed
from django.core.management.base import BaseCommand, CommandParser
from contenidos.models import Cursos

class Command(BaseCommand):
    help = 'Seeder inicial de Cursos, Data: seeders/cursos.json'

    def add_arguments(self, parser):
        parser.add_argument(
            '--total',
            type=int,
            default=0,
            help='Número adicional de cursos falsos a generar'
        )
        

    def handle(self, *args, **options):
        json_path = settings.BASE_DIR / 'contenidos' / 'seeders' / 'cursos.json'

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                cursos_data = json.load(f)

                for curso_data in cursos_data:
                    Cursos.objects.get_or_create(
                        titulo=curso_data['titulo'],
                        defaults=curso_data
                    )
                self.stdout.write(self.style.SUCCESS(f'{len(cursos_data)} cursos cargados desde JSON : seeders/cursos.json'))
                
        except FileNotFoundError:
            self.stdout.write(self.style.WARNING('Archivo cursos.json no encontrado'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Error al leer el archivo JSON'))
            
            