from pydantic import BaseModel, TypeAdapter
from decimal import Decimal
from .enums import FiatMethodDirection, FiatMethodLocation
from typing import List


class ExchangeRate(BaseModel):
    currency_id: str
    rate: Decimal


class FiatMethod(BaseModel):
    currency_name: str
    direction: FiatMethodDirection
    fee_fix: Decimal
    fee_percentage: Decimal
    id: str
    location: FiatMethodLocation
    name: str
    rates: List[ExchangeRate]


FiatMethodList = TypeAdapter(list[FiatMethod])