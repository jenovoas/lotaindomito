"""
App principal — FastAPI con lifespan, CORS y routers.

Lifespan:
    startup  → log de inicio
    shutdown → close_db()
"""
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db import close_db
from app.routers.zonas import router as zonas_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifecycle — startup y shutdown."""
    print("[lifespan] Startup: Lota Indómito backend")
    yield
    await close_db()
    print("[lifespan] Shutdown: conexión DB cerrada")


app = FastAPI(
    title="Lota Indómito API",
    description="Backend para el piloto de concepto — zonas, wallet, NPCs",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS — orígenes configurables via CORS_ORIGINS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(zonas_router)


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check — GET /health."""
    return {"status": "ok"}
