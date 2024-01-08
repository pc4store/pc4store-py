from typing import Literal, Optional

from pydantic import BaseModel


class Pc4StoreErrorResponse(BaseModel):
    status: Literal["ERROR"]
    error: str
    error_type: Optional[str] = None


class Pc4StoreError(Exception):
    def __init__(self, error: Pc4StoreErrorResponse):
        self.message = error.error
        self.error_type = error.error_type or "Unknown"

    def __repr__(self) -> str:
        return f"PC4StoreError('{self.message}')"
