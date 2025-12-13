"""Session management endpoints."""

from fastapi import APIRouter, HTTPException, Response, status

from app.core.exceptions import SessionNotFoundError
from app.models.schemas import ErrorResponse
from app.services.session_manager import session_manager

router = APIRouter()


@router.delete(
    "/{session_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"model": ErrorResponse, "description": "Session not found"},
    },
)
async def reset_session(session_id: str) -> Response:
    """
    Reset/delete a session and all associated data.

    Args:
        session_id: Unique session identifier

    Raises:
        HTTPException: If session is not found
    """
    try:
        if not session_manager.session_exists(session_id):
            raise SessionNotFoundError(session_id)

        session_manager.delete_session(session_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except SessionNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get(
    "/{session_id}/status",
    response_model=dict[str, str],
    responses={
        404: {"model": ErrorResponse, "description": "Session not found"},
    },
)
async def get_session_status(session_id: str) -> dict[str, str]:
    """
    Get session status and metadata.

    Args:
        session_id: Unique session identifier

    Returns:
        Session status information

    Raises:
        HTTPException: If session is not found
    """
    try:
        session = session_manager.get_session(session_id)

        return {
            "session_id": session_id,
            "filename": session["filename"],
            "created_at": session["created_at"].isoformat(),
            "expires_at": session["expires_at"].isoformat(),
            "status": "active",
        }

    except SessionNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
