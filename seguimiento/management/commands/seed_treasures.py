from django.core.management.base import BaseCommand
from mongoData.models import Treasures
from mongoData.models import Users as User
from faker import Faker
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import time
import random
import math


class Command(BaseCommand):
    help = 'Seeder inicial de Tesoros en Bogotá y Cartagena'

    def add_arguments(self, parser):
        parser.add_argument(
            '--total',
            type=int,
            default=30,
            help='Número total de tesoros a generar (se divide entre Bogotá y Cartagena)'
        )

    def handle(self, *args, **options):
        total = options['total']
        start_time = time.time()

        # Coordenadas de las ciudades
        bogota = {"lat": 4.7110, "lng": -74.0721, "name": "Bogotá"}
        cartagena = {"lat": 10.39972, "lng": -75.51444, "name": "Cartagena"}
        cities = [bogota, cartagena]

        # Calcular tesoros por ciudad
        treasures_per_city = total // len(cities)

        def generate_nearby_coordinates(base_lat, base_lng, max_distance_km=30):
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

        def generate_treasure(i, city):
            fake = Faker('es_ES')
            is_found = fake.boolean(chance_of_getting_true=30)  # 30% de probabilidad de ser encontrado

            # Generar coordenadas cercanas a la ciudad especificada
            latitude, longitude = generate_nearby_coordinates(city['lat'], city['lng'], 30)

            # Obtener un usuario real de la base de datos o crear uno si no existe
            try:
                # Intentar obtener un usuario existente aleatorio
                users = list(User.objects.all())
                if users:
                    creator = random.choice(users)
                    creator_id = str(creator.id)  # ID de Django User
                    creator_name = creator.username
                else:
                    # Si no hay usuarios, crear uno básico
                    creator = User.objects.create_user(
                        username=fake.user_name(),
                        email=fake.email(),
                        password='password123',
                        first_name=fake.first_name(),
                        last_name=fake.last_name()
                    )
                    creator_id = str(creator.id)
                    creator_name = creator.username
            except Exception as e:
                print(f"Error obteniendo usuario: {e}")
                # Fallback a datos fake
                creator_id = fake.uuid4()
                creator_name = fake.name()

            return Treasures(
                creator_id=creator_id,  # Usar ID real del usuario
                creator_name=creator_name,
                title=fake.sentence(nb_words=4),
                location={"type": "Point", "coordinates": [longitude, latitude]},
                description=fake.text(max_nb_chars=200),
                image_url=fake.image_url(),
                latitude=str(latitude),
                longitude=str(longitude),
                hint=fake.sentence(nb_words=6),
                difficulty=fake.random_int(min=1, max=5),
                clues=[fake.sentence(nb_words=5) for _ in range(fake.random_int(min=1, max=5))],
                is_found=is_found,
                found_by=fake.uuid4() if is_found else None,
                created_at=fake.date_time_this_decade(),
                found_at=fake.date_time_this_year() if is_found else None,
                points=fake.random_int(min=1, max=100)
            ).save()

        # Generar tesoros para cada ciudad
        total_created = 0
        for city in cities:
            self.stdout.write(f"Generando {treasures_per_city} tesoros en {city['name']}...")

            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = [executor.submit(generate_treasure, i, city) for i in range(treasures_per_city)]
                for future in tqdm(as_completed(futures), total=treasures_per_city, desc=f"Tesoros en {city['name']}"):
                    try:
                        future.result()
                        total_created += 1
                    except Exception as e:
                        self.stderr.write(self.style.ERROR(f"Error al generar tesoro: {e}"))

        elapsed_time = time.time() - start_time
        self.stdout.write(self.style.SUCCESS(
            f'Seeding completado: {total_created} tesoros creados en {elapsed_time:.2f} segundos'
        ))