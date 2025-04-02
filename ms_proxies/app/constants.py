import os
from dotenv import load_dotenv

load_dotenv()

#DataBase
__url_client__     =  os.getenv("MONGO_CLIENT")
__name_database__  =  os.getenv("DATABASE")

#Colecciones
__proxies_collection__        =  os.getenv("PROXIES_COLLECTION")

#Smartproxy
SMART_PROXY          = os.getenv("SMART_PROXY")

#Tor
TOR_CONTROL_PASSWORD = os.getenv("TOR_CONTROL_PASSWORD")
