import time
from django.core.management.base import BaseCommand
from faker import Faker
import random
import json
import datetime
from bson import ObjectId
from mongoData.models import Cursos
from mongoData.models import Videos
from contenidos.models import Videos as SQLVideos
from django.conf import settings
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

class Command(BaseCommand):
    help = 'Generador de datos falsos para Videos'

    def add_arguments(self, parser):
        parser.add_argument('--total', type=int, default=100, help='Número de videos a generar')
        parser.add_argument('--clear', action='store_true', help='Eliminar todos los videos existentes')

    def handle(self, *args, **options):
        start_time = time.time()
        fake = Faker('es_ES')
        total = options['total']

        # Limpiar la colección si se pasa el parámetro --clear
        if options['clear']:
            self.stdout.write(self.style.WARNING('Eliminando todos los videos existentes...'))
            Videos.objects.delete()

        # Obtener todos los cursos existentes
        total_cursos = Cursos.objects.count()
        random_index = random.randint(0, total_cursos - 1)

         # Obtener el país aleatorio
        IdCurso = Cursos.objects[random_index]

        cursos_ids = list(Cursos.objects.only('id').scalar('id'))
        if not cursos_ids:
            self.stdout.write(self.style.ERROR('No hay cursos en la base de datos.'))
            return
        
        def saveVideosToPosgreSQL():
            json_path = settings.BASE_DIR / 'contenidos' / 'seeders' / 'videos.json'

            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    videos_data = json.load(f)

                    for video_data in videos_data:
                        SQLVideos.objects.create(**video_data)
                    self.stdout.write(self.style.SUCCESS(f'{len(videos_data)} videos cargados desde JSON : seeders/videos.json'))

            except FileNotFoundError:
                self.stdout.write(self.style.WARNING('Archivo videos.json no encontrado'))
            except json.JSONDecodeError:
                self.stdout.write(self.style.ERROR('Error al leer el archivo JSON'))

        def generar_video(i):
            now = datetime.datetime.now()
            video = Videos(
                nombre=fake.sentence(nb_words=4),
                ruta=f"videos/video{random.randint(1, 20)}.mp4",
                descripcion=fake.paragraph(nb_sentences=3),
                edadMinima=random.randint(7, 120),
                idCurso=IdCurso,
                #idCurso=ObjectId('68294a14b2321e6f5903ac28'),  # Seleccionar un curso aleatorio
                duracion=random.randint(60, 7200),  # 1 min a 2 horas en segundos
                fecha_creacion=now,
                fecha_modificacion=now,
                imagen=fake.image_url(),
                cantidad_vistas=random.randint(0, 10000),
                cantidad_likes=random.randint(0, 1000)
            )
            video.save()

        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = [executor.submit(generar_video, i) for i in range(1, total + 1)]
            for future in tqdm(as_completed(futures), total=total, desc="Generando videos"):
                try:
                    future.result()
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error generando video: {str(e)}'))
        # Guardar videos en PostgreSQL desde JSON
        saveVideosToPosgreSQL()
        elapsed_time = time.time() - start_time
        self.stdout.write(self.style.SUCCESS(f'\n{total} videos creados exitosamente en {elapsed_time:.2f} segundos.'))