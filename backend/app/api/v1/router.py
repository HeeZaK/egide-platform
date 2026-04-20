from fastapi import APIRouter

from app.api.v1.endpoints import campaigns, health, osint

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(osint.router, prefix="/osint", tags=["osint"])
api_router.include_router(
    campaigns.router,
    prefix="/campaigns",
    tags=["campaigns"],
)
