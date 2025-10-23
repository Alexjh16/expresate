import json
from django.conf import settings
from django_seed import Seed
from faker import Faker
from django.core.management.base import BaseCommand, CommandParser
from evaluacion.models import Preguntas
from mongoData.models import Preguntas as MongoPreguntas, Respuestas
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import time

class Command(BaseCommand):
    help = 'Seeder inicial de Preguntas, Data: seeders/preguntas.json'

    def add_arguments(self, parser):
        parser.add_argument(
            '--total',
            type=int,
            default=100,
            help='Número adicional de preguntas falsas a generar'
        )
        
        

    def handle(self, *args, **options):
        total = options['total']
        start_time = time.time()
        def savePreguntasToPostgreSQL():
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

        #generate fake preguntas to save in mongo
        def generate_preguntas(i):
            fake = Faker('es_ES')
            tipo_pregunta = fake.random_element(elements=('opcion_multiple', 'verdadero_falso'))
            categoria_clase = fake.random_element(elements=('Animales', 'Familia', 'Paises', 'Numeros'))
            respuestas = [
                Respuestas(
                    respuesta=fake.sentence(nb_words=4),
                    esCorrecta=(j == 0)  # Primera respuesta es correcta
                )
                for j in range(4)
            ]
            MongoPreguntas(
                pregunta=fake.sentence(nb_words=6),
                tipo_pregunta=tipo_pregunta,
                categoria_clase=categoria_clase,
                respuestas=respuestas
            ).save()
        # Usar ThreadPoolExecutor para generar documentos en paralelo
        with ThreadPoolExecutor(max_workers=12) as executor:
            futures = [executor.submit(generate_preguntas, i) for i in range(1, total + 1)]
            for future in tqdm(as_completed(futures), total=total, desc="Generando Preguntas"):
                try:
                    future.result()
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error generando Preguntas: {str(e)}'))

        # Guardar preguntas en PostgreSQL desde JSON
        savePreguntasToPostgreSQL()
        elapsed_time = time.time() - start_time
        self.stdout.write(self.style.SUCCESS(f'\n{total} documentos creados exitosamente en {elapsed_time:.2f} segundos.'))