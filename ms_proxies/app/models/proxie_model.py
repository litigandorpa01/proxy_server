from typing import Optional, Literal, Dict, Any, Union

from pydantic import BaseModel, Field,HttpUrl

#Proxy request
class ProxyRequest(BaseModel):
    proxy_client: Literal['tor', 'smart_proxy'] = Field(..., description="Tipo de proxy a usar")
    method: Literal['GET', 'POST', 'PUT', 'DELETE', 'PATCH'] = Field(..., description="Método HTTP")
    url: HttpUrl = Field(..., description="URL destino válida")
    headers: Optional[Dict[str, Any]] = None
    params: Optional[Dict[str, Any]] = None
    body: Optional[Dict[str, Any]] = None

    class Config:
        extra = "forbid" 


class ProxyResponse(BaseModel):
    data: Dict
    proxy_used: Dict
    status: int
    method: str

#Proxy register
class ProxyRegisterRequest(BaseModel):
    proxy_client: Literal['tor', 'smart_proxy'] = Field(..., description="Tipo de proxy a usar")
    proxy: Dict[str, Union[str, int]] = Field(..., description="Información del proxy, debe contener 'host' y 'port'")

    class Config:
        json_schema_extra = {
            "example": {
                "proxy_client": "tor",
                "proxy": {"host": "tor_1", "port": 9050}
            }
        }

class ProxyRegisterResponse(BaseModel):
    inserted_id:str    