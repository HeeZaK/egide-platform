from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine

import app.models  # noqa: F401  # register ORM metadata


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.auto_create_tables:
        Base.metadata.create_all(bind=engine)
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="Egide HRM API",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )
    _cors = [o.strip() for o in settings.cors_origins.split(",") if o.strip()]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=_cors,
        allow_credentials=True,
        # FIX: restreindre aux méthodes réellement utilisées (was ["*"])
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        # FIX: restreindre aux headers nécessaires (was ["*"])
        allow_headers=["Authorization", "Content-Type", "Accept"],
    )
    app.include_router(api_router, prefix="/api/v1")
    return app


app = create_app()
