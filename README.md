```
# Expresate - Backend

Este repositorio contiene el backend (Django) del proyecto Expresate.

Ahora la configuración está preparada para desplegar en Render (https://render.com). Se han eliminado los artefactos de Docker Compose del repositorio por petición.

Resumen rápido
-------------
- Backend: Django 5.1
- Bases de datos: PostgreSQL (recomendado usar Render Managed Postgres) y MongoDB (usar MongoDB Atlas o proveedor externo)
- Cache: Redis (puedes usar Render Redis o un servicio gestionado)

Variables de entorno
--------------------
Copia `.env.example` a `.env` si deseas mantener un archivo local para desarrollo. En Render deberás configurar las variables de entorno en el Dashboard del servicio.

Despliegue en Render (guía mínima)
---------------------------------
1. Crea un nuevo Web Service en Render y conecta tu repositorio.
2. Configura los parámetros del servicio:
	- Environment: `Python`
	- Build Command: `pip install -r requirements.txt`
	- Start Command: `gunicorn expresate.wsgi:application --bind 0.0.0.0:$PORT`
	- Branch: la rama que quieras desplegar (por ejemplo `main`).
3. Agrega variables de entorno en la sección Environment (Render Dashboard):
	- `DJANGO_SECRET_KEY` (valor seguro)
	- `DJANGO_DEBUG=False` (en producción)
	- `DJANGO_ALLOWED_HOSTS` (por ejemplo: `your-service.onrender.com`)
	- Postgres connection variables si usas Render Managed Postgres: `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`.
	- MongoDB: recomendamos usar MongoDB Atlas y configurar `MONGO_HOST` (connection string o host), `MONGO_PORT` y `MONGO_DB_NAME`, o `MONGO_URI` si usas una URI completa.
	- Redis: si usas Render Redis, configura `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD`.
	- RECOMENDADO: usar `MONGO_URI` (por ejemplo la URI de MongoDB Atlas) y `REDIS_URL` para simplificar la conexión desde Render.
4. Bases de datos:
	- Render ofrece Managed Postgres: crea una instancia e introduce las credenciales en las env vars de tu Web Service.
	- Para MongoDB, Render no ofrece un servicio gestionado nativo: usa MongoDB Atlas o un proveedor que prefieras y añade su URI a `MONGO_URI` o las variables separadas.
5. Storage de medios y estáticos:
	- Para producción recomendamos configurar un storage externo (S3, Cloud Storage) y usar django-storages.
	- Alternativa rápida: servir media desde una bucket y configurar `MEDIA_URL` apropiadamente.
6. Migraciones y collectstatic:
	- En Render puedes añadir un `Deploy Hook` o un `build` command que ejecute `python manage.py migrate` y `python manage.py collectstatic --noinput` durante el build/deploy. Otra opción es ejecutar manualmente `deploy hooks` o conectarte vía `render shell`.

Recomendaciones para producción
--------------------------------
- Usa `DJANGO_DEBUG=False` y una `DJANGO_SECRET_KEY` segura (gestor de secretos).
- Usa Render Managed Postgres para la base relacional y MongoDB Atlas para Mongo.
- Configura backups automáticos para ambas bases.
- Protege endpoints que usen `@csrf_exempt`.
- Añade tests y CI para validar antes de hacer deploy automático.

Ejemplo de `render.yaml` (opcional)
-----------------------------------
He añadido un archivo `render.yaml` básico en el repo que puedes usar como punto de partida para infraestructura como código en Render (ajusta valores según tu cuenta). Si prefieres, puedes configurar todo desde el Dashboard.

Siguientes pasos sugeridos
-------------------------
1. Dime si quieres que yo genere automática y completamente el `render.yaml` (incluyendo Managed Postgres) o prefieres configurarlo desde el Dashboard.
2. Puedo añadir un script para ejecutar migraciones automáticamente desde un `deploy` command en Render.
3. Quieres que remueva también archivos relacionados con Docker en git history o crear una rama con los cambios? (opcional)

Si quieres que configure el `render.yaml` ahora (con Managed Postgres), indícame: (a) nombre del proyecto en Render y (b) si quieres crear base Postgres gestionada desde el `render.yaml`.

## Configuración del Proyecto

Sigue los pasos a continuación para configurar y ejecutar el proyecto:

### Requisitos Previos

Asegúrate de tener lo siguiente configurado antes de continuar:
- Una base de datos PostgreSQL creada y configurada.
- Una base de datos MongoDB creada y configurada.
- Redis corriendo en tu sistema.

### Pasos para Configurar el Proyecto

```
1. **Crear un entorno virtual**:
   ```bash
   python -m venv venv
   ```

2. **Activar el entorno virtual**:
   - En Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - En Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

3. **Instalar las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Aplicar las migraciones**:
   ```bash
   python manage.py migrate
   ```

5. **Cargar los seeders**:
   ```bash
   python manage.py seed_db
   ```

6. **Ejecutar el servidor de desarrollo**:
   ```bash
   python manage.py runserver
   ```

El proyecto estará disponible en `http://127.0.0.1:8000/`.

## API Documentation

### Treasure Endpoints

#### 1. Get Nearby Treasures
Obtiene tesoros cercanos a una ubicación específica.

**URL:** `http://localhost:8000/api/treasures/nearby/`

**Método:** `GET`

**Parámetros de Query:**
- `lat` (float, requerido): Latitud del punto de referencia.
- `lng` (float, requerido): Longitud del punto de referencia.
- `radius` (float, opcional, default=5): Radio de búsqueda en kilómetros.

**Ejemplo de Request:**
```
GET /api/treasures/nearby/?lat=4.6097&lng=-74.0817&radius=10
```

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "treasures": [
    {
      "id": "60f7b3b3b3b3b3b3b3b3b3b3",
      "creator_id": "user123",
      "creator_name": "Juan Pérez",
      "title": "Tesoro escondido",
      "description": "Un tesoro misterioso",
      "image_url": "http://example.com/image.jpg",
      "latitude": "4.6097",
      "longitude": "-74.0817",
      "hint": "Cerca del árbol",
      "difficulty": 3,
      "clues": ["Mira arriba", "Busca abajo"],
      "is_found": false,
      "found_by": null,
      "created_at": "2023-10-24T10:00:00Z",
      "found_at": null,
      "points": 50,
      "distance_km": 2.5
    }
  ]
}
```

#### 2. Create Treasure
Crea un nuevo tesoro.

**URL:** `http://localhost:8000/api/treasures/create/`

**Método:** `POST`

**Headers:**
- `Content-Type: application/json`

**Body:**
```json
{
  "creator_id": "user123",
  "creator_name": "Juan Pérez",
  "title": "Tesoro del parque",
  "description": "Escondido en el banco del parque",
  "location": {
    "type": "Point",
    "coordinates": [-74.0817, 4.6097]
  },
  "image_url": "http://example.com/treasure.jpg",
  "latitude": "4.6097",
  "longitude": "-74.0817",
  "hint": "Cerca del lago",
  "difficulty": 2,
  "clues": ["Busca en el banco", "Mira debajo"],
  "points": 25
}
```

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "message": "Tesoro creado"
}
```

#### 3. Claim Treasure
Reclama un tesoro encontrado.

**URL:** `http://localhost:8000/api/treasures/{id}/claim/`

**Método:** `POST`

**Parámetros de URL:**
- `id` (string): ObjectId del tesoro en MongoDB.

**Headers:**
- `Content-Type: application/json`

**Body:**
```json
{
  "user_id": "user456"
}
```

**Ejemplo de Request:**
```
POST /api/treasures/60f7b3b3b3b3b3b3b3b3b3b3/claim/
Content-Type: application/json

{
  "user_id": "user456"
}
```

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "message": "Tesoro 60f7b3b3b3b3b3b3b3b3b3b3 reclamado"
}
```

#### 4. Get User Treasures
Obtiene los tesoros encontrados por un usuario.

**URL:** `http://localhost:8000/api/treasures/user/{id}/`

**Método:** `GET`

**Parámetros de URL:**
- `id` (string): ObjectId del usuario en MongoDB.

**Ejemplo de Request:**
```
GET /api/treasures/user/60f7b3b3b3b3b3b3b3b3b3b4/
```

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "treasures": [
    {
      "id": "60f7b3b3b3b3b3b3b3b3b3b3",
      "creator_id": "user123",
      "creator_name": "Juan Pérez",
      "title": "Tesoro encontrado",
      "description": "Ya reclamado",
      "image_url": "http://example.com/image.jpg",
      "latitude": "4.6097",
      "longitude": "-74.0817",
      "hint": "Cerca del árbol",
      "difficulty": 3,
      "clues": ["Mira arriba", "Busca abajo"],
      "is_found": true,
      "found_by": "user456",
      "created_at": "2023-10-24T10:00:00Z",
      "found_at": "2023-10-24T12:00:00Z",
      "points": 50
    }
  ]
}
```

#### 5. Get User Stats
Obtiene estadísticas de un usuario.

**URL:** `http://localhost:8000/api/users/{id}/stats/`

**Método:** `GET`

**Parámetros de URL:**
- `id` (string): ObjectId del usuario en MongoDB.

**Ejemplo de Request:**
```
GET /api/users/60f7b3b3b3b3b3b3b3b3b3b4/stats/
```

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "stats": {
    "treasures_created": 5,
    "treasures_found": 12,
    "total_points": 450,
    "rank": "Explorador Experto"
  }
}
```

### Notas Generales
- Todos los endpoints devuelven respuestas en formato JSON.
- Los IDs son ObjectIds de MongoDB (strings de 24 caracteres hexadecimales).
- Las coordenadas geoespaciales usan el formato GeoJSON.
- Los endpoints están protegidos con `@csrf_exempt` para facilitar el desarrollo, pero en producción considera agregar autenticación y protección CSRF.

## Endpoints de la API

### Login de Usuario
Este endpoint permite autenticar a un usuario mediante un POST con credenciales.

**URL:**  
`http://localhost:8000/users/api/loginUser/`

**Método:**  
`POST`

**Body:**  
El cuerpo de la solicitud debe enviarse en formato JSON con los siguientes campos:

```json
{
    "username": "usuario",
    "password": "clave"
}