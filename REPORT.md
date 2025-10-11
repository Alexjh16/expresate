# Informe de análisis — Proyecto Expresate

Fecha: 10 de octubre de 2025

## Resumen ejecutivo

Este informe resume la arquitectura, dependencias, puntos de riesgo y recomendaciones para desplegar el backend del proyecto Expresate. He preparado una configuración para ejecutar el proyecto con Docker Compose (Postgres, Mongo, Redis y la app Django con Gunicorn). También ajusté `settings.py` para usar variables de entorno.

## Arquitectura y componentes

- Framework: Django 5.1.1
- Bases de datos:
  - PostgreSQL (relacional): usuarios, roles, categorías, niveles.
  - MongoDB (NoSQL via mongoengine): cursos, videos, preguntas, seguimiento.
- Cache / sesiones: Redis (django-redis).
- Frontend: plantillas Django + Tailwind + Alpine + htmx (no SPA completo).
- Otras: altcha para desafío (captcha-like), django_browser_reload en dev.

## Archivos clave añadidos/actualizados

- `Dockerfile`, `docker-compose.yml`, `entrypoint.sh` — despliegue local con Docker Compose.
- `.env.example` — variables de entorno ejemplo.
- `README.md` — instrucciones de despliegue.
- `.gitignore` — actualizado.
- `REPORT.md` — este informe.
- `settings.py` — ahora lee credenciales desde variables de entorno.
- `requirements.txt` — se añadieron `gunicorn` y `psycopg2-binary`.

## Riesgos y problemas detectados

1. SECRET_KEY expuesto en el repo (mitigado: ahora se lee desde env, pero actualizar .env en el host).
2. DEBUG por defecto True (mitigado parcialmente: ahora lee DJANGO_DEBUG desde env; asegurarse de poner False en prod).
3. Endpoints con `@csrf_exempt` que modifican datos (riesgo de CSRF): `crearCategoria`, `editarCategoria`, `eliminarCategoria`, `crearNivel`, `editarNivel`, `eliminarNivel`, `crearCurso`, `crearVideo`, `editarVideo`, `eliminarVideo`, etc.
4. Doble fuente de usuarios (Postgres y Mongo) — riesgo de inconsistencia.
5. Manejo de archivos/media: `default_storage` sin backend de producción (usar S3 o similar en producción).
6. Falta de tests automatizados y pipeline CI.

## Acciones priorizadas (alto impacto, bajo esfuerzo)

1. Mover variables sensibles fuera del repo y configurar `DJANGO_DEBUG=False` en producción. (`.env` + secrets manager)
2. Proteger endpoints que usan `@csrf_exempt`: reemplazarlos por vistas que requieran `login_required` y verificación CSRF (o tokens de API).
3. Añadir `.env` al `.gitignore` (ya hecho).
4. Configurar backups para Postgres y Mongo (cron o servicio gestionado).
5. Revisión de sincronización Postgres↔Mongo (decidir cuál es el "source of truth" para usuarios).

## Acciones de mediano plazo

- Configurar almacenamiento de Media/Static en S3 y CDN.
- Añadir tests unitarios y de integración, y un pipeline CI (GitHub Actions) que ejecute tests y lint.
- Contenerizar de forma preparada para producción (multi-stage Dockerfile, compresión de assets).
- Monitorización (Sentry, Prometheus/Grafana) y alertas.

## Instrucciones para desplegar localmente (Docker Compose)

1. Copia el ejemplo de entorno y edítalo:

```bash
cp .env.example .env
# Edita .env con un DJANGO_SECRET_KEY seguro y ajusta DJANGO_DEBUG si necesitas
```

2. Levantar servicios:

```bash
docker compose up --build
```

3. Ver logs y verificar que las migraciones se aplicaron:

```bash
# Ver logs del contenedor web
docker compose logs -f web
```

4. Acceder: http://localhost:8000

## Checklist de preparación para producción

- [ ] `DJANGO_DEBUG=False` en entorno
- [ ] `DJANGO_SECRET_KEY` gestionado por secrets manager
- [ ] `ALLOWED_HOSTS` configurado
- [ ] Storage para media está en S3 u otro almacenamiento persistente
- [ ] Backup programado para Postgres y Mongo
- [ ] Revisión de CSRF y autenticación en endpoints críticos
- [ ] Tests automatizados y pipeline CI

## Siguientes pasos recomendados (puedo implementarlos)

- Implementar CI básico (GitHub Actions) con: lint, tests y build Docker.
- Añadir tests unitarios básicos (registro de usuario + CRUD de categorías).
- Reemplazar `@csrf_exempt` por protección adecuada en endpoints que modifican la DB.
- Construir multi-stage Dockerfile optimizado para producción.

Si quieres, puedo empezar por cualquiera de estas tareas. Por ejemplo:

- Generar un workflow de GitHub Actions que construya la imagen y ejecute tests (si quieres, lo creo ahora).
- Quitar `@csrf_exempt` y añadir `login_required` donde corresponde (haría cambios prudentes y los validaría).
- Añadir tests básicos y ejecutar `pytest` (hay que instalar pytest y configurar entorno o usar Docker).

---

Resumen final: el proyecto ya puede arrancar localmente con Docker Compose. Recomiendo priorizar seguridad (DEBUG, SECRET_KEY), protección CSRF, y tests/CI. Dime cuál de las tareas siguientes quieres que implemente y la hago: CI / tests / endurecer CSRF / sincronización Postgres-Mongo / otro.
