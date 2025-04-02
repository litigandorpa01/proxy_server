from datetime import datetime,timezone

from pymongo import ReturnDocument

from app.database import get_collection
from app.constants import __proxies_collection__

class ProxyRepository:        
    def __init__(self, proxy_client: str):
        self.proxy_client = proxy_client
        self.collection = get_collection(__proxies_collection__)

    async def add_proxy_record(self, proxy: str):
        try:
            document = {
                "proxy_client": self.proxy_client,
                "proxy": proxy,
                "isUse": False,
                "failedAttempts": 0,
                "succedAttemps":0,
                "lastUse": datetime.now(timezone.utc).isoformat(),
                "createDateTime": datetime.now(timezone.utc).isoformat()
            }
            result = await self.collection.insert_one(document)
            return {"inserted_id": str(result.inserted_id)}
        except Exception as e:
            raise e
    
    async def get_proxy(self):
        try:
            update = {
                "$set": {"isUse": True, "lastUse": datetime.now(timezone.utc).isoformat()}
            }

            # Primera búsqueda: proxies no usados y con 0 fallos
            query_primary = {
                "proxy_client": self.proxy_client,
                "isUse": False,
            }

            proxy = await self.collection.find_one_and_update(
                query_primary,
                update,
                return_document=ReturnDocument.AFTER,
                sort=[("succedAttemps", 1)]  # Ordenar por intentos exitosos ascendente
            )

            if not proxy:
                # Segunda búsqueda: cualquier proxy con 0 fallos (incluso en uso)
                query_secondary = {
                    "proxy_client": self.proxy_client,
                    "failedAttempts": 0
                }
                
                proxy = await self.collection.find_one(
                    query_secondary, 
                    sort=[("succedAttemps", 1), ("lastUse", 1)]
                )

                if proxy:
                    await self.collection.update_one(
                        {"_id": proxy["_id"]}, 
                        update
                    )
                else:
                    # Tercera búsqueda: menor número de failedAttempts (cualquier estado)
                    query_tertiary = {
                        "proxy_client": self.proxy_client
                    }
                    
                    proxy = await self.collection.find_one_and_update(
                        query_tertiary,
                        update,
                        return_document=ReturnDocument.AFTER,
                        sort=[
                            ("failedAttempts", 1),   # Menor número de fallos
                            ("succedAttemps", -1),   # Prioriza proxies con mas éxitos
                            ("lastUse", 1)          # Más antiguo primero
                        ]
                    )

            return proxy["proxy"] if proxy and "proxy" in proxy else None

        except Exception as e:
            raise e

    async def increment_succed_attempts(self, proxy: dict):
        try:
            query = {"proxy": proxy} 
            update_data = {"$inc": {"succedAttemps": 1}} 

            result = await self.collection.update_one(query, update_data)
            return result.modified_count > 0 
        except Exception as e:
            raise e
    
    async def increment_failed_attempts(self, proxy: dict):
        try:
            query = {"proxy": proxy} 
            update_data = {"$inc": {"failedAttempts": 1}} 

            result = await self.collection.update_one(query, update_data)
            return result.modified_count > 0 
        except Exception as e:
            raise e
    
