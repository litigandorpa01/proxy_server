from fastapi import APIRouter, HTTPException

from app.services.proxy_services import ProxyService
from app.models.proxie_model import ProxyRequest,ProxyResponse, ProxyRegisterRequest, ProxyRegisterResponse

router = APIRouter()

@router.post("/request")
async def proxy_request(request:ProxyRequest ):
    try:
        proxy_service=ProxyService(request.proxy_client)
        result = await proxy_service.proxy_request(
            request.method, request.url, request.headers, 
            request.params, request.body
        )
        return ProxyResponse(**result)
    except ValueError as e: 
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/register")
async def proxy_register(request:ProxyRegisterRequest):
    try:
        proxy_service=ProxyService(request.proxy_client)
        result = await proxy_service.proxy_register(
            request.proxy
        )
        return ProxyRegisterResponse(**result)
    except ValueError as e: 
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
