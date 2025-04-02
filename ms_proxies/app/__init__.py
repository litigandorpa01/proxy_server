import logging

from fastapi import FastAPI

# Configurar logging con formato y nivel de logs
logging.basicConfig(
    format="%(asctime)s - %(levelname)s : %(module)s - %(funcName)s | %(message)s",
    level=logging.INFO
)
logging.getLogger("stem").disabled = True

app = FastAPI(
    title="Proxies API Service",
    description=(
        "Proxies app"
    ),
    version="0.1.0",
    contact={
        "name": "Dev",
        "email": "dev@lit.com.co",
    },
    license_info={
        "name": "Dev",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_url="/api/openapi.json", 
    docs_url="/api/docs",  
    redoc_url="/api/redoc",  
)

from .views import *