from decimal import Decimal
from typing import List

from pydantic import BaseModel, RootModel

from .enums import FiatMethodDirection, FiatMethodLocation


class ExchangeRate(BaseModel):
    currency_id: str
    rate: Decimal


class FiatMethod(BaseModel):
    currency_name: str
    direction: FiatMethodDirection
    fee_fix: Decimal
    fee_percentage: Decimal
    minimal_amount: Decimal
    maximal_amount: Decimal
    minimal_coin: Decimal = Decimal("0.01")
    id: str
    location: FiatMethodLocation
    name: str
    rates: List[ExchangeRate]


class FiatMethodList(RootModel):
    root: List[FiatMethod]
