from decimal import Decimal
from typing import Optional, List

from pydantic import BaseModel

from .enums import Blockchain


class Currency(BaseModel):
    id: str
    name: str
    blockchain: Blockchain
    smart_contract: str
    precission: int
    min_transfer_amount: Decimal

    is_income_enabled: bool
    is_outcome_enabled: bool

    fee_fix: Decimal
    fee_percentage: Decimal
    withdraw_fee_fix: Decimal
    withdraw_fee_percentage: Decimal

    txn_limit: Optional[Decimal] = None
    account_limit: Optional[Decimal] = None
    day_limit: Optional[Decimal] = None

    txn_cap: Optional[Decimal] = None
    account_cap: Optional[Decimal] = None
    day_cap: Optional[Decimal] = None


class CurrencyList(BaseModel):
    __root__: List[Currency]

