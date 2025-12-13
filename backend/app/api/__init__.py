"""API routes."""

from fastapi import APIRouter

from app.api.endpoints import data, session, upload

router = APIRouter()

router.include_router(upload.router, prefix="/upload", tags=["upload"])
router.include_router(data.router, prefix="/data", tags=["data"])
router.include_router(session.router, prefix="/session", tags=["session"])
