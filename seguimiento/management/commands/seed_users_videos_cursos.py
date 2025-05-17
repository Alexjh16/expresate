import time
from django.core.management.base import BaseCommand
from faker import Faker
from bson import ObjectId
import random
import datetime
from mongoData.models import UserVideosCurso, VideoInfo
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

class Command(BaseCommand):
    help = 'Generador de datos falsos para UserVideosCurso usando ThreadPoolExecutor'

    def add_arguments(self, parser):
        parser.add_argument('--total', type=int, default=5, help='Número de documentos a generar')
        parser.add_argument('--clear', action='store_true', help='Eliminar todos los documentos existentes')

    def handle(self, *args, **options):
        start_time = time.time()

        fake = Faker('es_ES')
        categorias = ["Animales", "Familia", "Paises", "Numeros"]

        total = options['total']

        # Limpiar la colección si se pasa el parámetro --clear
        if options['clear']:
            self.stdout.write(self.style.WARNING('Eliminando todos los documentos existentes en UserVideosCurso...'))
            UserVideosCurso.objects.delete()

        def generar_user_video_curso(i):
            # Generar un ObjectId falso para idCurso
            id_curso = ObjectId()

            

            # Generar un porcentaje de visualización aleatorio
            porcentaje_visto = random.randint(0, 100)

            #si porcentaje_visto es 0, los videos son vacios
            if porcentaje_visto == 0:
                videos = []

            if porcentaje_visto > 0:
                # Generar una lista de videos aleatorios (de 0 a n elementos)
                num_videos = random.randint(1, 5)  # Número de videos (puede ser 0)
                videos = [
                    VideoInfo(
                        nombre=f"Video {j + 1} - {fake.word()}",
                        ruta=f"media/videos/video{j + 1}.mp4",
                        fecha_visualizacion=fake.date_time_between(start_date='-1y', end_date='now')
                    )
                    for j in range(num_videos)
                ]
            # Determinar el estado en función del porcentaje
            estado = "bloqueado" if porcentaje_visto == 0 else "desbloqueado"

            # Generar un documento en UserVideosCurso
            UserVideosCurso(
                categoria_clase=random.choice(categorias),
                idCurso=id_curso,
                video=videos,
                usuario=[
                    fake.user_name(),
                    f"{fake.first_name()} {fake.last_name()}",
                    fake.email()
                ],
                estado=estado,
                porcentaje_visto=porcentaje_visto
            ).save()

        # Usar ThreadPoolExecutor para generar documentos en paralelo
        with ThreadPoolExecutor(max_workers=12) as executor:
            futures = [executor.submit(generar_user_video_curso, i) for i in range(1, total + 1)]
            for future in tqdm(as_completed(futures), total=total, desc="Generando UserVideosCurso"):
                try:
                    future.result()
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error generando UserVideosCurso: {str(e)}'))

        elapsed_time = time.time() - start_time
        self.stdout.write(self.style.SUCCESS(f'\n{total} documentos creados exitosamente en {elapsed_time:.2f} segundos.'))