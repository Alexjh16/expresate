from django.core.management.base import BaseCommand
from pymongo import MongoClient
from django.conf import settings

class BaseSeederCommand(BaseCommand):
    """
    Clase base para los seeders que maneja la conexión a MongoDB
    """
    def __init__(self):
        super().__init__()
        self.mongo_client = None
        self.mongo_db = None
        self.mongo_collection = None

    def connect_mongodb(self, collection_name):
        """
        Establece la conexión con MongoDB
        """
        try:
            mongo_uri = getattr(settings, 'MONGO_URI', None)
            print(f"MONGO_URI: {mongo_uri}")  # Debug
            if mongo_uri:
                self.mongo_client = MongoClient(mongo_uri)
            else:
                self.mongo_client = MongoClient(
                    host=settings.MONGO_DB['HOST'],
                    port=settings.MONGO_DB['PORT']
                )
            self.mongo_db = self.mongo_client[settings.MONGO_DB['NAME']]
            self.mongo_collection = self.mongo_db[collection_name]
            return True
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error al conectar con MongoDB: {str(e)}'))
            return False

    def save_to_mongodb(self, data, unique_field):
        """
        Guarda o actualiza un documento en MongoDB
        """
        if self.mongo_collection is not None:
            try:
                self.mongo_collection.update_one(
                    {unique_field: data[unique_field]},
                    {'$set': data},
                    upsert=True
                )
                return True
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error al guardar en MongoDB: {str(e)}'))
                return False
        return False

    def close_mongodb_connection(self):
        """
        Cierra la conexión con MongoDB
        """
        if self.mongo_client is not None:
            self.mongo_client.close() 