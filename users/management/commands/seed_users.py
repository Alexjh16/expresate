import json
from django.conf import settings
from django_seed import Seed
from django.core.management.base import BaseCommand, CommandParser
from users.models import Users
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Seeder inicial de Users, Data: seeders/users.json'

    def add_arguments(self, parser):
        parser.add_argument(
            '--total',
            type=int,
            default=0,
            help='Número adicional de users falsos a generar'
        )
        

    def handle(self, *args, **options):
        json_path = settings.BASE_DIR / 'users' / 'seeders' / 'users.json'

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                users_data = json.load(f)

                for user_data in users_data:
                    # Guardar la contraseña sin encriptar
                    raw_password = user_data.get('password')
                    print(raw_password)
                    # Encriptar la contraseña
                    if 'password' in user_data:
                        user_data['password'] = make_password(user_data['password'])
                    print(user_data['password'])
                    Users.objects.get_or_create(
                        username=user_data['username'],
                        defaults=user_data
                    )
                self.stdout.write(self.style.SUCCESS(f'{len(users_data)} paises cargados desde JSON : seeders/users.json'))
                
        except FileNotFoundError:
            self.stdout.write(self.style.WARNING('Archivo users.json no encontrado'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Error al leer el archivo JSON'))
            
            