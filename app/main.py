from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.v1.rest_controller import api_router
from app.core.config import settings
from app.startup_models import ensure_models


@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_models()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok"}


app.include_router(api_router, prefix=settings.API_V1_STR)
