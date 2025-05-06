import json
from django.conf import settings
from django_seed import Seed
from django.core.management.base import BaseCommand, CommandParser
from contenidos.models import CategoriaClases

class Command(BaseCommand):
    help = 'Seeder inicial de Categorias, Data: seeders/categorias.json'

    def add_arguments(self, parser):
        parser.add_argument(
            '--total',
            type=int,
            default=0,
            help='Número adicional de categorias falsas a generar'
        )
        

    def handle(self, *args, **options):
        json_path = settings.BASE_DIR / 'contenidos' / 'seeders' / 'categorias.json'

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                categorias_data = json.load(f)

                for categoria_data in categorias_data:
                    CategoriaClases.objects.get_or_create(
                        nombre_categoria=categoria_data['nombre_categoria'],
                        defaults=categoria_data
                    )
                self.stdout.write(self.style.SUCCESS(f'{len(categorias_data)} categorias cargadas desde JSON : seeders/categorias.json'))
                
        except FileNotFoundError:
            self.stdout.write(self.style.WARNING('Archivo categorias.json no encontrado'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Error al leer el archivo JSON'))
            
            