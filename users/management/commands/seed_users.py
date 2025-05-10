import time
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from users.models import Users
from expresate.redisUtil import redisClient
from mongoData.models import Paises as MongoPaises
from mongoData.models import Users as MongoUsers
from faker import Faker
import random
import string
from django.utils import timezone
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

class Command(BaseCommand):
    help = 'Generador de usuarios con datos falsos usando Faker'

    def add_arguments(self, parser):
        parser.add_argument('--total', type=int, default=100, help='Número de usuarios a generar')
        parser.add_argument('--clear', action='store_true', help='Eliminar todos los usuarios existentes')

    def handle(self, *args, **options):
        start_time = time.time()

        fake = Faker('es_ES')
        total = options['total']

        if options['clear']:
            self.stdout.write(self.style.WARNING('Eliminando todos los usuarios existentes...'))
            Users.objects.all().delete()

        dispositivos = ['smartphone', 'tablet', 'laptop', 'escritorio', 'other']

        if not Users.objects.filter(username='admin').exists():
            Users.objects.create(
                username='admin',
                first_name='Admin',
                last_name='Principal',
                email='admin@mail.com',
                password=make_password('admin123456'),
                is_superuser=True,
                is_staff=False,
                is_active=True,
                edad=30,
                dispositivo='smartphone',
                pais_id=42,
                rol_id=2,
                date_joined=timezone.now()
            )

            # Guardar el usuario admin en MongoDB
            MongoUsers(
                first_name='Admin',
                last_name='Principal',
                username='admin',
                email='admin@mail.com',
                password=make_password('admin123456'),
                foto_perfil="https://example.com/admin.jpg",  # Foto de perfil predeterminada
                edad=30,
                rol="admin",
                idPais=None,  # Si no tienes un país específico para el admin
                dispositivo='smartphone'
            ).save()

            # Guardar en Redis el administrador
             
            redisClient.set('admin', make_password('admin123456'), ex=3000)  # 5 minutos de expiración
            self.stdout.write(self.style.SUCCESS('Usuario admin creado'))

        def generar_usuario(i):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            email = f'{first_name.lower()}.{last_name.lower()}{i}@mail.com'
            password = make_password('123456789a*')

            # Guardar en Redis
            redisClient.set(username, password, ex=3000)

            # Guardar en MongoDB
            # Contar el total de países
            total_paises = MongoPaises.objects.count()

            # Seleccionar un índice aleatorio
            random_index = random.randint(0, total_paises - 1)

            # Obtener el país aleatorio
            MongoPais = MongoPaises.objects[random_index]
            
            MongoUsers(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
                foto_perfil="https://example.com/foto.jpg",
                edad=random.randint(7, 120),
                rol=random.choice(["estudiante", "docente", "niño", "universitario", "madre", "padre"]),
                idPais=MongoPais,
                dispositivo=random.choice(["smartphone", "tablet", "laptop", "escritorio", "otro"]),
            ).save()

            return Users(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                is_superuser=False,
                is_staff=False,
                is_active=True,
                edad=random.randint(7, 120),
                dispositivo=random.choice(dispositivos),
                pais_id=random.randint(1, 193),
                rol_id=random.randint(1, 6),
                date_joined=fake.date_time_between(start_date='-2y', end_date='now'),
                last_login=None,
                foto=None
            )

        users_to_create = []

        with ThreadPoolExecutor(max_workers=12) as executor:
            futures = [executor.submit(generar_usuario, i) for i in range(1, total + 1)]
            for future in tqdm(as_completed(futures), total=total, desc="Generando usuarios"):
                try:
                    users_to_create.append(future.result())
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error generando usuario: {str(e)}'))

        Users.objects.bulk_create(users_to_create, batch_size=1000)

        elapsed_time = time.time() - start_time
        self.stdout.write(self.style.SUCCESS(f'\n{total} usuarios creados exitosamente [mongo, pgsql, redis] en {elapsed_time:.2f} segundos.'))
