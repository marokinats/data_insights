"""API routes."""

from fastapi import APIRouter

from app.api.endpoints import chart, data, export, session, upload

router = APIRouter()

router.include_router(upload.router, prefix="/upload", tags=["upload"])
router.include_router(data.router, prefix="/data", tags=["data"])
router.include_router(session.router, prefix="/session", tags=["session"])
router.include_router(chart.router, prefix="/chart", tags=["chart"])
router.include_router(export.router, prefix="/export", tags=["export"])
