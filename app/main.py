from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.v1 import router as v1_router
from app.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Structured AI service skeleton for Valthera analysis endpoints.",
    )
    app.include_router(health_router)
    app.include_router(v1_router, prefix="/v1")
    return app


app = create_app()
