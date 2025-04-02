import logging
from asyncio import sleep

from app.services.tor_proxy import TorProxy
from app.repositories.proxy_repository import ProxyRepository

class ProxyService:
    def __init__(self, proxy_client: str):
        self.proxy_client = proxy_client
        self.repository=ProxyRepository(
            self.proxy_client
        )
        self.proxy = None
        self.proxy_host=None
        self.max_retries = 3 

    async def _initialize(self) -> None:
        """Initialize the proxy service asynchronously."""
        try:
            self.proxy_host = await self.repository.get_proxy()
            await self._initialize_proxy()
        except Exception as e:
            raise e

    async def _initialize_proxy(self):
        try: 
            if self.proxy_client == 'tor':
                self.proxy = TorProxy(self.proxy_host)
            elif self.proxy_client == 'smart_proxy':
                # Implementar lógica para SmartProxy
                raise NotImplementedError("SmartProxy no está implementado")
            else:
                raise ValueError(f"Proxy client no soportado: {self.proxy_client}")
        except Exception as e:
            raise e

    async def proxy_request(self, method: str, url: str, headers: dict, params: dict, body: dict):
        last_exception = None
        await self._initialize()
        
        for attempt in range(self.max_retries):
            try:
                result = await self.proxy.proxy_request(method, url, headers, params, body)

                if result:
                    await self.repository.increment_succed_attempts(self.proxy_host)
                return result
            except Exception as e:
                last_exception = e
                # logging.warning(f" {self.proxy_host} ~ Intento {attempt + 1} fallido. Error: {str(e)}")
                
                # Si es error 500, no reintentar
                if "500" in str(e):  # Busca "500" en el mensaje de error
                    await self.repository.increment_failed_attempts(self.proxy_host)
                    raise e  # Rompe el ciclo y lanza el error
                
                # Si no es el último intento, esperamos antes de reintentar
                if attempt < self.max_retries - 1:
                    self.proxy.request_new_ip()
                    continue
                
                # Si llegamos aquí, todos los intentos fallaron
                await self.repository.increment_failed_attempts(self.proxy_host)
                logging.error(f"No se proceso {self.proxy_host} - {e} ")
                raise last_exception
        
    async def proxy_register(self,proxy):
        try:
            return await self.repository.add_proxy_record(proxy)
        except Exception as e:
            raise e
        