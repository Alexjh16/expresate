import time
import psycopg2
from django.core.management.base import BaseCommand
from faker import Faker
import random
import string
from django.utils import timezone
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from pymongo import MongoClient
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Generador de usuarios falsos guardados en MongoDB y PostgreSQL'

    def add_arguments(self, parser):
        parser.add_argument('--total', type=int, default=100, help='Número de usuarios a generar')
        parser.add_argument('--clear', action='store_true', help='Eliminar todos los usuarios existentes')

    def handle(self, *args, **options):
        start_time = time.time()

        # Conexión a MongoDB
        client = MongoClient("mongodb://localhost:27017")
        db_mongo = client["expresate"]
        usuarios_mongo = db_mongo["users"]

        # Conexión a PostgreSQL
        conn_pg = psycopg2.connect(
            dbname="expresate",
            user="postgres",
            password="12345",
            host="localhost",
            port="5432"
        )
        cursor_pg = conn_pg.cursor()

        fake = Faker('es_ES')
        total = options['total']

        # Limpiar si se solicita (RECOMENDACIÓN: cuidado con relaciones foráneas)
        if options['clear']:
            self.stdout.write(self.style.WARNING('Eliminando todos los usuarios existentes...'))
            usuarios_mongo.delete_many({})
            try:
                cursor_pg.execute("DELETE FROM users;")
                conn_pg.commit()
            except psycopg2.errors.ForeignKeyViolation as e:
                conn_pg.rollback()
                self.stdout.write(self.style.ERROR(
                    f'Error eliminando usuarios en PostgreSQL: {str(e)}\nAsegúrate de eliminar registros relacionados (como cuestionarios).'))

        dispositivos = ['smartphone', 'tablet', 'laptop', 'desktop', 'other']

        # Crear admin si no existe
        cursor_pg.execute("SELECT 1 FROM users WHERE username = %s", ('admin',))
        admin_pg_exists = cursor_pg.fetchone() is not None
        admin_mongo_exists = usuarios_mongo.find_one({"username": "admin"}) is not None

        if not admin_pg_exists and not admin_mongo_exists:
            admin_data = {
                "username": "admin",
                "first_name": "Admin",
                "last_name": "Principal",
                "email": "admin@mail.com",
                "password": make_password('admin123456'),
                "is_superuser": True,
                "is_staff": False,
                "is_active": True,
                "edad": 30,
                "dispositivo": "smartphone",
                "pais_id": 42,
                "rol_id": 2,
                "date_joined": timezone.now(),
                "last_login": None,
                "foto": None
            }
            usuarios_mongo.insert_one(admin_data)
            cursor_pg.execute("""
                INSERT INTO users (username, first_name, last_name, email, password, is_superuser, is_staff, is_active,
                                   edad, dispositivo, pais_id, rol_id, date_joined, last_login, foto)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                admin_data["username"], admin_data["first_name"], admin_data["last_name"], admin_data["email"],
                admin_data["password"], admin_data["is_superuser"], admin_data["is_staff"], admin_data["is_active"],
                admin_data["edad"], admin_data["dispositivo"], admin_data["pais_id"], admin_data["rol_id"],
                admin_data["date_joined"], admin_data["last_login"], admin_data["foto"]
            ))
            conn_pg.commit()
            self.stdout.write(self.style.SUCCESS('Usuario admin creado en ambos sistemas'))
        else:
            self.stdout.write(self.style.WARNING('Usuario admin ya existe en MongoDB o PostgreSQL'))

        # Generar usuarios falsos
        def generar_usuario(i):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            email = f'{first_name.lower()}.{last_name.lower()}{i}@mail.com'
            password = make_password('admin123456')

            return {
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "password": password,
                "is_superuser": False,
                "is_staff": False,
                "is_active": True,
                "edad": random.randint(7, 120),
                "dispositivo": random.choice(dispositivos),
                "pais_id": random.randint(1, 193),
                "rol_id": random.randint(1, 6),
                "date_joined": fake.date_time_between(start_date='-2y', end_date='now'),
                "last_login": None,
                "foto": None
            }

        usuarios_a_insertar = []

        with ThreadPoolExecutor(max_workers=12) as executor:
            futures = [executor.submit(generar_usuario, i) for i in range(1, total + 1)]
            for future in tqdm(as_completed(futures), total=total, desc="Generando usuarios"):
                try:
                    usuarios_a_insertar.append(future.result())
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error generando usuario: {str(e)}'))

        # Insertar en MongoDB
        if usuarios_a_insertar:
            self.stdout.write(self.style.SUCCESS(f'Insertando {len(usuarios_a_insertar)} usuarios...'))
            usuarios_mongo.insert_many(usuarios_a_insertar)

            # Insertar en PostgreSQL
            for u in usuarios_a_insertar:
                try:
                    cursor_pg.execute("""
                        INSERT INTO users (username, first_name, last_name, email, password, is_superuser, is_staff, is_active,
                                           edad, dispositivo, pais_id, rol_id, date_joined, last_login, foto)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        u["username"], u["first_name"], u["last_name"], u["email"], u["password"],
                        u["is_superuser"], u["is_staff"], u["is_active"], u["edad"], u["dispositivo"],
                        u["pais_id"], u["rol_id"], u["date_joined"], u["last_login"], u["foto"]
                    ))
                except psycopg2.errors.UniqueViolation:
                    conn_pg.rollback()
                    self.stdout.write(self.style.WARNING(f'Usuario duplicado: {u["username"]}'))
                except Exception as e:
                    conn_pg.rollback()
                    self.stdout.write(self.style.ERROR(f'Error insertando en PostgreSQL: {str(e)}'))

            conn_pg.commit()

        elapsed_time = time.time() - start_time
        self.stdout.write(self.style.SUCCESS(f'\n{total} usuarios creados exitosamente en {elapsed_time:.2f} segundos.'))

        cursor_pg.close()
        conn_pg.close()
