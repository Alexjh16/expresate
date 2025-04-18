import json
from django.conf import settings
from django_seed import Seed
from django.core.management.base import BaseCommand, CommandParser
from users.models import RolesUser

class Command(BaseCommand):
    help = 'Seeder inicial de Roles User, Data: seeders/roles_user.json'

    def add_arguments(self, parser):
        parser.add_argument(
            '--total',
            type=int,
            default=0,
            help='Número adicional de roles falsos a generar'
        )
        

    def handle(self, *args, **options):
        json_path = settings.BASE_DIR / 'users' / 'seeders' / 'roles_user.json'

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                roles_user_data = json.load(f)

                for rol_data in roles_user_data:
                    RolesUser.objects.get_or_create(
                        nombre=rol_data['nombre'],
                        defaults=rol_data
                    )
                self.stdout.write(self.style.SUCCESS(f'{len(roles_user_data)} roles cargados desde JSON : seeders/roles_user.json'))
                
        except FileNotFoundError:
            self.stdout.write(self.style.WARNING('Archivo roles_user.json no encontrado'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Error al leer el archivo JSON'))
            