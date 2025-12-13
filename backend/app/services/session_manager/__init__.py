"""Session management service."""

import uuid
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from app.core.config import settings
from app.core.exceptions import SessionNotFoundError
from app.services.session_manager.dto import Session


class SessionManager:
    """Manage user sessions and temporary data storage."""

    def __init__(self) -> None:
        """Initialize session manager."""
        self._sessions: dict[str, Session] = {}
        self._ensure_upload_dir()

    def _ensure_upload_dir(self) -> None:
        """Ensure upload directory exists."""
        upload_path = Path(settings.UPLOAD_DIR)
        upload_path.mkdir(parents=True, exist_ok=True)

    def create_session(self, filename: str) -> str:
        """
        Create a new session.

        Args:
            filename: Original filename

        Returns:
            Session ID
        """
        session_id = str(uuid.uuid4())
        self._sessions[session_id] = {
            "id": session_id,
            "filename": filename,
            "created_at": datetime.now(UTC),
            "expires_at": datetime.now(UTC) + timedelta(minutes=settings.SESSION_EXPIRE_MINUTES),
            "data": None,
        }
        return session_id

    def get_session(self, session_id: str) -> Session:
        """
        Get session data.

        Args:
            session_id: Session identifier

        Returns:
            Session data

        Raises:
            SessionNotFoundError: If session doesn't exist or expired
        """
        if session_id not in self._sessions:
            raise SessionNotFoundError(session_id)

        session = self._sessions[session_id]

        if datetime.now(UTC) > session["expires_at"]:
            self.delete_session(session_id)
            raise SessionNotFoundError(session_id)

        return session

    def update_session_data(self, session_id: str, data: dict[str, Any]) -> None:
        """
        Update session data.

        Args:
            session_id: Session identifier
            data: Data to store

        Raises:
            SessionNotFoundError: If session doesn't exist
        """
        session = self.get_session(session_id)
        session["data"] = data

    def delete_session(self, session_id: str) -> None:
        """
        Delete a session.

        Args:
            session_id: Session identifier
        """
        if session_id in self._sessions:
            del self._sessions[session_id]

    def session_exists(self, session_id: str) -> bool:
        """
        Check if session exists and is valid.

        Args:
            session_id: Session identifier

        Returns:
            True if session exists and not expired
        """
        try:
            self.get_session(session_id)
            return True
        except SessionNotFoundError:
            return False

    def cleanup_expired_sessions(self) -> int:
        """
        Remove expired sessions.

        Returns:
            Number of sessions removed
        """
        now = datetime.now(UTC)
        expired = [id for id, session in self._sessions.items() if now > session["expires_at"]]

        for session_id in expired:
            self.delete_session(session_id)

        return len(expired)


session_manager = SessionManager()
