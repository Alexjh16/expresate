import redis # redis: Jhon Alexander
from django.conf import settings
# Configuración de Redis
if hasattr(settings, 'REDIS_URL') and settings.REDIS_URL:
    redisClient = redis.from_url(settings.REDIS_URL)
else:
    redisClient = redis.Redis(
        host=settings.REDIS["HOST"],  # Obtiene el host desde settings
        port=settings.REDIS["PORT"],  # Obtiene el puerto desde settings
        db=settings.REDIS["DB"],      # Obtiene la base de datos desde settings
    )

