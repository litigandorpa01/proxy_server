import logging
import time
from asyncio import sleep

import socket 
from stem import Signal
from aiohttp import ClientSession
from stem.control import Controller
from aiohttp_socks import ProxyConnector
from app.constants import TOR_CONTROL_PASSWORD

class TorProxy:
    def __init__(self, proxy:dict):
        self.proxy=proxy
        self.control_host = proxy['host']
        self.control_password = TOR_CONTROL_PASSWORD
        self.control_port = proxy.get('control_port', 9051)

    def request_new_ip(self):
        try:
            tor_ip = socket.gethostbyname(self.control_host)
            controller= Controller.from_port(address=tor_ip, port=self.control_port)
            controller.authenticate(password=self.control_password)
            # logging.info("✅ Autenticación exitosa")

            # Obtener el tiempo de espera necesario antes de cambiar la IP
            wait_time = controller.get_newnym_wait()
            if wait_time > 0:
                # logging.info(f"Esperando {wait_time} segundos antes de solicitar una nueva IP...")
                time.sleep(wait_time)  # Esperar el tiempo recomendado por Tor

            # Enviar señal para cambiar de identidad
            controller.signal(Signal.NEWNYM)            
            time.sleep(0.5)
    
        except Exception as e:
            logging.error(f"Error crítico: {str(e)}")
        finally:
            if controller:
                controller.close()

    async def proxy_request(self, method, url, headers, params, body):
        connector = ProxyConnector.from_url(f"socks5://{self.proxy['host']}:{self.proxy['port']}")

        # logging.info(f'~ Proxy:{self.proxy}')

        async with ClientSession(connector=connector) as session:
            try:
                # Obtener la IP pública de la proxy
                async with session.get("https://check.torproject.org/api/ip", timeout=18) as ip_response:
                    proxy_ip = await ip_response.json()
                    # logging.info(f'~ Proxy: {self.proxy} | IP Pública: {proxy_ip.get("IP", "No disponible")}')

                async with session.request(
                    method=method,
                    url=str(url),
                    headers=headers,
                    params=params,
                    json=body if method in ['POST', 'PUT', 'PATCH'] else None,
                    timeout=10
                ) as response:
                    data = await response.json()
                    # logging.info(f'~ data:{await response.text()}')
                    return {"data": data, "proxy_used": self.proxy, "status": response.status,"method":method}
            except Exception as e:
                # logging.error(f"{self.proxy} ~ Error en proxy_request: {str(e)}")
                raise e
