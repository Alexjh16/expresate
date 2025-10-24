from django.core.management.base import BaseCommand
from mongoData.models import Treasures
from faker import Faker
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import time
import os
import django
from faker import Faker
import random
import math


class Command(BaseCommand):
    help = 'Seeder inicial de Tesoros, Data: seeders/tesoros.json'

    def add_arguments(self, parser):
        parser.add_argument(
            '--total',
            type=int,
            default=256,
            help='Número adicional de tesoros falsos a generar'
        )
    
    def handle(self, *args, **options):
        total = options['total']
        start_time = time.time()

        def generate_nearby_coordinates(base_lat, base_lng, max_distance_km=50):
            """
            Genera coordenadas aleatorias dentro de un radio máximo desde una ubicación base.
            """
            # Convertir km a grados (aproximadamente)
            max_distance_degrees = max_distance_km / 111.32  # 1 grado ≈ 111.32 km

            # Generar ángulo y distancia aleatorios
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(0, max_distance_degrees)

            # Calcular nuevas coordenadas
            delta_lat = distance * math.cos(angle)
            delta_lng = distance * math.sin(angle) / math.cos(math.radians(base_lat))

            new_lat = base_lat + delta_lat
            new_lng = base_lng + delta_lng

            return new_lat, new_lng

        def generate_treasure(i, base_lat=4.7110, base_lng=-74.0721, max_radius_km=50):
                fake = Faker('es_ES')
                is_found=fake.boolean(chance_of_getting_true=30)  # 10% de probabilidad de ser encontrado,
                # Generar coordenadas cercanas a Bogotá
                latitude, longitude = generate_nearby_coordinates(base_lat, base_lng, max_radius_km)
                return Treasures(
                    creator_id=fake.uuid4(),
                    creator_name=fake.name(),
                    title=fake.sentence(nb_words=4),
                    #send fake location in float
                    location={"type": "Point", "coordinates": [longitude, latitude]},
                    description=fake.text(max_nb_chars=200),
                    image_url=fake.image_url(),
                    latitude=str(latitude),
                    longitude=str(longitude),
                    hint=fake.sentence(nb_words=6),
                    difficulty=fake.random_int(min=1, max=5),
                    clues=[fake.sentence(nb_words=5) for _ in range(fake.random_int(min=1, max=5))],
                    #if found is false then found_by and found_at should be None
                    is_found=is_found,
                    found_by=fake.uuid4() if is_found else None,
                    created_at=fake.date_time_this_decade(),
                    found_at=fake.date_time_this_year() if is_found else None,
                    points=fake.random_int(min=1, max=100)
                ).save()
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(generate_treasure, i) for i in range(total)]
            for future in tqdm(as_completed(futures), total=total, desc="Generando tesoros"):
                try:
                    future.result()
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f"Error al generar tesoro: {e}"))
        elapsed_time = time.time() - start_time
        self.stdout.write(self.style.SUCCESS(f'Seeding de tesoros completado en {elapsed_time:.2f} segundos'))