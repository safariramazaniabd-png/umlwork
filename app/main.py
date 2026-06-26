from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api import donateurs, dons, campagnes, paiements, recus


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(donateurs.router, prefix="/api/v1/donateurs", tags=["Donateurs"])
app.include_router(dons.router, prefix="/api/v1/dons", tags=["Dons"])
app.include_router(campagnes.router, prefix="/api/v1/campagnes", tags=["Campagnes"])
app.include_router(paiements.router, prefix="/api/v1/paiements", tags=["Paiements"])
app.include_router(recus.router, prefix="/api/v1/recus", tags=["Recus"])


@app.get("/health")
async def health():
    return {"status": "ok", "app": settings.app_name}
