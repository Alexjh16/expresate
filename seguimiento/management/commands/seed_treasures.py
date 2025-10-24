from django.core.management.base import BaseCommand
from mongoData.models import Treasures
from faker import Faker
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import time


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

        def generate_treasure(i):
                fake = Faker('es_ES')
                is_found=fake.boolean(chance_of_getting_true=30)  # 10% de probabilidad de ser encontrado,
                return Treasures(
                    creator_id=fake.uuid4(),
                    creator_name=fake.name(),
                    title=fake.sentence(nb_words=4),
                    #send fake location in float
                    location={"type": "Point", "coordinates": [float(fake.longitude()), float(fake.latitude())]},
                    description=fake.text(max_nb_chars=200),
                    image_url=fake.image_url(),
                    latitude=str(fake.latitude()),
                    longitude=str(fake.longitude()),
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