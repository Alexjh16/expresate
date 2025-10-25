import json
from django.conf import settings
from django_seed import Seed
from django.core.management.base import BaseCommand, CommandParser
from evaluacion.models import Cuestionarios
from mongoData.models import Cuestionario as MongoCuestionarios, Preguntas, detallesIntentos
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import time
from faker import Faker


class Command(BaseCommand):
    help = 'Seeder inicial de Cuestionarios, Data: seeders/cuestionarios.json'

    def add_arguments(self, parser):
        parser.add_argument(
            '--total',
            type=int,
            default=20,
            help='Número adicional de cuestionarios falsos a generar'
        )
        

    def handle(self, *args, **options):
        total = options['total']
        start_time = time.time()
        def saveCuestionariosToPostgres():
            json_path = settings.BASE_DIR / 'evaluacion' / 'seeders' / 'cuestionarios.json'

            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    cuestionarios_data = json.load(f)

                    for cuestionario_data in cuestionarios_data:
                        autor_id = cuestionario_data.get('autor_id')
                        if autor_id:
                            Cuestionarios.objects.get_or_create(
                                titulo=cuestionario_data['titulo'],
                                autor_id=autor_id,
                                defaults={
                                    'descripcion': cuestionario_data.get('descripcion'),
                                    'limite_intentos': cuestionario_data.get('limite_intentos'),
                                    'estado': cuestionario_data.get('estado'),
                                    'calificacion_aprobacion': cuestionario_data.get('calificacion_aprobacion'),
                                    'duracion_estimada': cuestionario_data.get('duracion_estimada'),
                                }
                            )
                        else:
                            self.stdout.write(self.style.WARNING(f'Cuestionario sin autor_id: {cuestionario_data["titulo"]}'))
                    self.stdout.write(self.style.SUCCESS(f'{len(cuestionarios_data)} cuestionarios cargados desde JSON : seeders/cuestionarios.json'))
                    
            except FileNotFoundError:
                self.stdout.write(self.style.WARNING('Archivo cuestionarios.json no encontrado'))
            except json.JSONDecodeError:
                self.stdout.write(self.style.ERROR('Error al leer el archivo JSON'))
        
        def generate_cuestionarios(i):
                fake = Faker('es_ES')
                
                preguntas = []
                #get stored preguntas from mongo
                stored_preguntas = list(Preguntas.objects.all())
                #get a random object id from stored_preguntas
                for _ in range(fake.random_int(min=3, max=10)):
                    pregunta = fake.random_element(elements=stored_preguntas)
                    preguntas.append(pregunta)

                intentos = []
                for intento_num in range(1, fake.random_int(min=1, max=5) + 1):
                    intentos.append(
                        detallesIntentos(
                            fecha_inicio=fake.date_time_this_year(),
                            fecha_fin=fake.date_time_this_year(),
                            calificacion=fake.random_int(min=0, max=100),
                            numero_intento=intento_num,
                            estado=fake.random_element(elements=["completado", "incompleto"]),
                            tiempo_empleado=fake.random_int(min=300, max=7200)
                        )
                    )
                estado_cuestionario = fake.random_element(elements=["activo", "inactivo"])
                calificacion = sum(intento.calificacion for intento in intentos) // len(intentos)
                user = [
                    fake.user_name(),
                    fake.name(),
                    fake.email()
                ]
                limite_intentos = fake.random_int(min=1, max=5)
                return MongoCuestionarios(
                        titulo=fake.sentence(nb_words=4),
                        descripcion=fake.paragraph(nb_sentences=3),
                        limite_intentos=limite_intentos,
                        estado=estado_cuestionario,
                        preguntas=preguntas,
                        calificacion=calificacion,
                        fecha_realizacion=fake.date_time_this_year(),
                        user=user,
                        detalles_intentos=intentos
                ).save()
        with ThreadPoolExecutor() as executor:
            total = options['total']
            futures = [executor.submit(generate_cuestionarios, i) for i in range(total)]
            for future in tqdm(as_completed(futures), total=total, desc="Generando cuestionarios falsos"):
                try:
                    future.result()
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error al generar cuestionario: {e}'))
        #save cuestionarios to postgres
        saveCuestionariosToPostgres()
        elapsed_time = time.time() - start_time
        self.stdout.write(self.style.SUCCESS(f'Seeding de cuestionarios completado en {elapsed_time:.2f} segundos'))

            
            