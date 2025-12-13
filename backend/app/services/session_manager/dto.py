from datetime import datetime
from typing import Any, TypedDict


class Session(TypedDict):
    id: str
    filename: str
    created_at: datetime
    expires_at: datetime
    data: Any | None
