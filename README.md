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
```
