from motor.motor_asyncio import AsyncIOMotorClient
from app.constants import __url_client__, __name_database__

# Configuración del cliente MongoDB
__client__ = AsyncIOMotorClient(__url_client__)
__database__ = __client__.get_database(__name_database__)

# Colecciones
def get_collection(name: str):
    """Obtiene la colección de MongoDB por nombre."""
    return __database__.get_collection(name)

