from . import app

from fastapi import APIRouter

from app.routes import proxies_routes

api_router = APIRouter(prefix="/api/v1/proxy")
api_router.include_router(proxies_routes.router,tags=["proxies"])

app.include_router(api_router)
