from pydantic import BaseModel
from typing import Literal


class Pc4StoreErrorResponse(BaseModel):
    status: Literal['ERROR']
    error: str


class Pc4StoreError(Exception):
    def __init__(self, error: Pc4StoreErrorResponse):
        self.message = error.error

    def __repr__(self) -> str:
        return f"PC4StoreError('{self.message}')"