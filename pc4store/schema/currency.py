from pydantic import BaseModel
from decimal import Decimal
from .enums import Blockchain
from typing import Optional


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

    txn_limit: Optional[Decimal]
    account_limit: Optional[Decimal]
    day_limit: Optional[Decimal]

    txn_cap: Optional[Decimal]
    account_cap: Optional[Decimal]
    day_cap: Optional[Decimal]
