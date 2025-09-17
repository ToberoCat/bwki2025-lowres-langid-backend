from fastapi import APIRouter

from app.api.v1.routes import classify
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(classify.router)