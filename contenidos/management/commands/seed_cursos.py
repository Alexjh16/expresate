import time
from django.core.management.base import BaseCommand
from faker import Faker
from bson import ObjectId
import random
import datetime
from mongoData.models import Cursos
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

class Command(BaseCommand):
    help = 'Generador de datos falsos para Cursos usando ThreadPoolExecutor'

    def add_arguments(self, parser):
        parser.add_argument('--total', type=int, default=100, help='Número de cursos a generar')
        parser.add_argument('--clear', action='store_true', help='Eliminar todos los cursos existentes')

    def handle(self, *args, **options):
        start_time = time.time()

        fake = Faker('es_ES')
        #categorias = ["Animales", "Familia", "Paises", "Números"]
        categorias = ["Colores"]
        niveles = [
            "introductorio",
            "básico",
            "intermedio",
            "avanzado",
            "experto"
        ]

        total = options['total']

        # Limpiar la colección si se pasa el parámetro --clear
        if options['clear']:
            self.stdout.write(self.style.WARNING('Eliminando todos los cursos existentes...'))
            Cursos.objects.delete()

        def generar_curso(i):
            # Generar un ObjectId falso para idCuestionario
            id_cuestionario = ObjectId()

            # Generar un curso con datos aleatorios
            curso = Cursos(
                titulo=fake.sentence(nb_words=3),  # Título aleatorio con 3 palabras
                descripcion=fake.paragraph(nb_sentences=5),  # Descripción aleatoria con 5 oraciones
                icono=fake.image_url(),  # URL de un icono aleatorio
                duracion=random.randint(3600, 21600),  # Duración en segundos (1 a 6 horas)
                fecha_creacion=datetime.datetime.now(),  # Fecha de creación actual
                estado=random.choice(["activo", "inactivo"]),  # Estado aleatorio
                categoria_clase=random.choice(categorias),  # Categoría aleatoria
                idCuestionario=id_cuestionario,  # ObjectId falso para idCuestionario
                nivel=random.choice(niveles)  # Nivel aleatorio
            )
            curso.save()

        # Usar ThreadPoolExecutor para generar cursos en paralelo
        with ThreadPoolExecutor(max_workers=12) as executor:
            futures = [executor.submit(generar_curso, i) for i in range(1, total + 1)]
            for future in tqdm(as_completed(futures), total=total, desc="Generando cursos"):
                try:
                    future.result()
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error generando curso: {str(e)}'))

        elapsed_time = time.time() - start_time
        self.stdout.write(self.style.SUCCESS(f'\n{total} cursos creados exitosamente en {elapsed_time:.2f} segundos.'))