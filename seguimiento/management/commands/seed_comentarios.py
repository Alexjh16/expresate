import json
from django.conf import settings
from django_seed import Seed
from django.core.management.base import BaseCommand, CommandParser
from seguimiento.models import Comentarios
from mongoData.models import Comentarios as MongoComentarios
from faker import Faker
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import time

class Command(BaseCommand):
    help = 'Seeder inicial de Comentarios, Data: seeders/comentarios.json'

    def add_arguments(self, parser):
        parser.add_argument(
            '--total',
            type=int,
            default=10,
            help='Número adicional de comentarios falsos a generar'
        )
        

    def handle(self, *args, **options):
        total = options['total']
        start_time = time.time()
        def saveComentariosToPostgreSQL():
            json_path = settings.BASE_DIR / 'seguimiento' / 'seeders' / 'comentarios.json'

            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    comentarios_data = json.load(f)

                    for comentario_data in comentarios_data:
                        Comentarios.objects.create(**comentario_data)
                    self.stdout.write(self.style.SUCCESS(f'{len(comentarios_data)} comentarios cargados desde JSON : seeders/comentarios.json'))
                    
            except FileNotFoundError:
                self.stdout.write(self.style.WARNING('Archivo comentarios.json no encontrado'))
            except json.JSONDecodeError:
                self.stdout.write(self.style.ERROR('Error al leer el archivo JSON'))
        def generate_comentarios(i):
                fake = Faker('es_ES')
                usuario = [
                    fake.user_name(),
                    fake.name(),
                    fake.email()
                ]
                video = [
                    fake.sentence(nb_words=3),
                    f"videos/{fake.file_name(extension='mp4')}"
                ]
                parent_comment = None
                if MongoComentarios.objects.count() > 0 and fake.boolean(chance_of_getting_true=30):
                    parent_comment = fake.random_element(elements=MongoComentarios.objects.all())
                return MongoComentarios(
                    comentario=fake.sentence(nb_words=10),
                    video=video,
                    usuario=usuario,
                    parent_id=parent_comment,
                    fechaCreacion=fake.date_time_this_year(),
                    fechaModificacion=fake.date_time_this_year()
                ).save()

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(generate_comentarios, i) for i in range(total)]
            for future in tqdm(as_completed(futures), total=total, desc="Generando comentarios falsos"):
                try:
                    future.result()
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error al generar comentario: {e}'))
        #save comentarios to postgreSQL
        saveComentariosToPostgreSQL()
        elapsed_time = time.time() - start_time
        self.stdout.write(self.style.SUCCESS(f'Seeding de comentarios completado en {elapsed_time:.2f} segundos'))

            
            