"""API v1 Routes."""

from fastapi import APIRouter

from app.api.v1 import decisions, health

router = APIRouter()

router.include_router(health.router, tags=["health"])
router.include_router(decisions.router, prefix="/decisions", tags=["decisions"])
