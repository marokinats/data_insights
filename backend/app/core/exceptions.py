"""Custom exceptions."""

from fastapi import status


class CustomException(Exception):
    """Base exception for application."""

    def __init__(self, message: str, status_code: int = 500) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class SessionNotFoundError(CustomException):
    """Raised when session is not found."""

    def __init__(self, session_id: str) -> None:
        message = f"Session not found: {session_id}"
        super().__init__(message, status_code=status.HTTP_404_NOT_FOUND)


class FileValidationError(CustomException):
    """Raised when file validation fails."""

    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=status.HTTP_400_BAD_REQUEST)


class DataProcessingError(CustomException):
    """Raised when data processing fails."""

    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
