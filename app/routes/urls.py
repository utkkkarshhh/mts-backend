from fastapi import APIRouter

from app.routes.v1 import v1_router

urls = APIRouter()
urls.include_router(v1_router, prefix="/v1/api")
