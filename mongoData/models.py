import mongoengine
from mongoengine import Document, StringField, ListField, DateTimeField, EmbeddedDocument, IntField, EmbeddedDocumentField, ReferenceField, BooleanField
from bson import ObjectId
import datetime

mongoengine.connect('expresate')


#Clases embeddeds : Jhon Alexander Ramos
# Definir un EmbeddedDocument para los videos
class VideoInfo(EmbeddedDocument):
    nombre = StringField(required=True)  # Nombre del video
    ruta = StringField(required=True)    # Ruta del video
    fecha_visualizacion = DateTimeField(required=True)  # Fecha de visualización


class Respuestas(EmbeddedDocument):
    respuesta = StringField(required=True)
    esCorrecta = BooleanField(default=False)

class detallesIntentos(EmbeddedDocument):
    fecha_inicio = DateTimeField()
    fecha_fin = DateTimeField()
    calificacion = IntField(default=0)
    numero_intento = IntField(default=1)
    estado = StringField(choices=["completado", "incompleto"], default="incompleto")
    tiempo_empleado = IntField(default=0)  # en segundos

#clases principales : Jhon Alexander Ramos
class Preguntas(Document):
    pregunta = StringField(required=True)
    tipo_pregunta = StringField(required=True, choices=["opcion_multiple", "verdadero_falso"])
    respuestas = ListField(EmbeddedDocumentField('Respuestas'))
    categoria_clase = StringField(required=True)
    fechaCreacion = DateTimeField()
    fechaModificacion = DateTimeField()

class Comentarios(Document):
    comentario = StringField(required=True)
    video = ListField(StringField()) #nombre, ruta
    usuario = ListField(StringField()) #username, nombres, email
    parent_id = ReferenceField('Comentarios', null=True)
    fechaCreacion = DateTimeField()
    fechaModificacion = DateTimeField()

class Paises(Document):
    nombre = StringField(required=True)
    codigo = StringField(required=True)
    indicativo = StringField(required=True)
    codigo_iso = StringField(required=True)
    idioma_principal = StringField(required=True)

class Users(Document):
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    email = StringField(required=True, unique=True)
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    foto_perfil = StringField()
    edad = IntField()
    rol = StringField(choices=["admin", "estudiante", "docente", "niño", "universitario", "madre", "padre"], default="estudiante")
    idPais = ReferenceField(Paises)
    dispositivo = StringField(choices=["smartphone", "tablet", "laptop", "escritorio", "otro"], default="escritorio")

class Cuestionario(Document):
    titulo = StringField(required=True)
    descripcion = StringField()
    limite_intentos = IntField(default=3)
    estado = StringField(choices=["activo", "inactivo"], default="activo")
    preguntas = ListField(ReferenceField(Preguntas))
    calificacion = IntField(default=0)
    fecha_realizacion = DateTimeField()
    user = ListField(StringField()) #username, nombres, email
    detalles_intentos=ListField(EmbeddedDocumentField('detallesIntentos'))

class Cursos(Document):
    titulo = StringField(required=True)
    descripcion = StringField()
    icono = StringField()
    duracion = IntField()
    fecha_creacion = DateTimeField()
    estado = StringField(choices=["activo", "inactivo"], default="incompleto")
    categoria_clase = StringField(required=True)
    idCuestionario = ReferenceField(Cuestionario)
    nivel = StringField(choices=["introductorio", "básico", "intermedio", "avanzado", "experto"], default="introductorio")


class Videos(Document):
    nombre = StringField(required=True)
    ruta = StringField(required=True)
    descripcion = StringField()
    edadMinima = IntField()
    idCurso = ReferenceField(Cursos)
    duracion = IntField() # en segundos
    fecha_creacion = DateTimeField()
    fecha_modificacion = DateTimeField()
    imagen = StringField() #url de la imagen
    cantidad_vistas = IntField(default=0)
    cantidad_likes = IntField(default=0)

#coleccion para seguimiento de videos por cursos de los usuarios : Jhon Alexander Ramos
class UserVideosCurso(Document):
    categoria_clase = StringField(required=True)
    idCurso = ReferenceField(Cursos)
    video = ListField(EmbeddedDocumentField(VideoInfo))  # Lista de videos con información estructurada#nombre, ruta, fecha_video_visualizado
    usuario = ListField(StringField()) #username, nombres, email
    estado = StringField(choices=["bloqueado", "desbloqueado"], default="bloqueado")
    porcentaje_visto = IntField(default=0) #porcentaje visto pero del curso
    

#Ejemplo de uso : Jhon Alexander Ramos
now = datetime.datetime.now()
now_str = now.strftime("%Y-%m-%d %H:%M:%S")  # Formato: Año-Mes-Día Hora:Minuto:Segundo



"""
Videos(
    nombre="Señas en 5 minutos",
    ruta="videos/video2.mp4",
    descripcion="Aprende las señas básicas en 5 minutos",
    edadMinima=7,
    idCurso=ObjectId(),  # Reemplaza con el ID del curso correspondiente
    duracion=720,  # Duración en formato HH:MM:SS
    fecha_creacion=now,
    fecha_modificacion=now,
    imagen="https://example.com/imagen.png",  # URL de la imagen
    cantidad_vistas=100,
    cantidad_likes=10
).save()




Cursos(
    titulo="Curso de Python",
    descripcion="Aprende Python desde cero",
    icono="https://example.com/icono.png",
    duracion=1024,
    fecha_creacion=now,
    estado="incompleto",
    categoria_clase="Programación",
    idCuestionario=ObjectId(),
    nivel="básico"
).save()

UserVideosCurso(
    categoria_clase="Animales",
    idCurso='64b8f13e8f1b2c3d4e5f6789',  # Reemplaza con el ID del curso correspondiente ej: Señas en 5 minutos
    video=[
        VideoInfo(nombre="Señas en 5 minutos", ruta="videos/video2.mp4", fecha_visualizacion=now_str),
        VideoInfo(nombre="Señas en 10 minutos", ruta="videos/video3.mp4", fecha_visualizacion=now_str),
        VideoInfo(nombre="Señas en 15 minutos", ruta="videos/video4.mp4", fecha_visualizacion=now_str)
    ],
    usuario=["alexander196", "Alexander Ramos", "alexx@mail.com"],
    estado="bloqueado",
    porcentaje_visto=3
).save()


Users(
    first_name="Jhon",
    last_name="Ramos",
    email="alexx@mail.com",
    username="alexx",
    password="12345678",
    foto_perfil="https://example.com/foto.jpg",
    edad=25,
    rol="admin",
    idPais=Paises.objects.get(nombre="Colombia"),
    dispositivo="smartphone"
).save()

Comentarios(
    comentario="Este es un comentario de prueba",
    video=["Señas en 5 minutos", "videos/video2.mp4"],
    usuario=["alexander196", "Alexander Ramos", "alexx@mail.com"],
    # parent_id=Comentarios.objects.first(),  # Referencia a otro comentario (opcional)
    #partent_id=None,  # Referencia a otro comentario (opcional)
    parent_id=Comentarios.objects.first(),  # Referencia a otro comentario (opcional)
    fechaCreacion=datetime.datetime.now(),
    fechaModificacion=datetime.datetime.now()
).save()

Preguntas(
    pregunta="¿Cuál es la capital de Francia?",
    tipo_pregunta="opcion_multiple",
    respuestas=[
        Respuestas(respuesta="París", esCorrecta=True),
        Respuestas(respuesta="Londres", esCorrecta=False),
        Respuestas(respuesta="Berlín", esCorrecta=False),
        Respuestas(respuesta="Madrid", esCorrecta=False)
    ],
    categoria_clase="Geografía",
    fechaCreacion=datetime.datetime.now(),
    fechaModificacion=datetime.datetime.now()
).save()

"""