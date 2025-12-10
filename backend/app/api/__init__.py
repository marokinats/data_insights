"""API routes."""

from fastapi import APIRouter

from app.api.endpoints import upload

router = APIRouter()

router.include_router(upload.router, prefix="/upload", tags=["upload"])
