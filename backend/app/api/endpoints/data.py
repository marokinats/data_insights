"""Data retrieval endpoints."""

import math
from typing import Any

from fastapi import APIRouter, HTTPException, status

from app.core.exceptions import SessionNotFoundError
from app.models.schemas import ErrorResponse, ProcessedData, SeriesData, StatisticsData
from app.services.session_manager import session_manager

router = APIRouter()


def clean_float_values(obj: Any) -> Any:
    """Recursively clean NaN and Infinity values from data structures."""
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return obj
    elif isinstance(obj, dict):
        return {k: clean_float_values(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_float_values(item) for item in obj]
    return obj


@router.get(
    "/{session_id}",
    response_model=ProcessedData,
    responses={
        404: {"model": ErrorResponse, "description": "Session not found"},
    },
)
async def get_processed_data(session_id: str) -> ProcessedData:
    """
    Get processed data for a session.

    Args:
        session_id: Unique session identifier

    Returns:
        Processed data including all series and statistics

    Raises:
        HTTPException: If session is not found
    """
    try:
        session = session_manager.get_session(session_id)

        session_data = session["data"]

        if not session_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session data not found")

        cleaned_data = clean_float_values(session_data)
        # Reconstruct SeriesData objects
        series_list = [SeriesData(**s) for s in cleaned_data["series_list"]]
        # Reconstruct StatisticsData
        stats = StatisticsData(**cleaned_data["statistics"])

        return ProcessedData(
            session_id=session_id,
            series=series_list,
            statistics=stats,
            original_filename=session["filename"],
        )

    except SessionNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error retrieving data: {str(e)}"
        )
