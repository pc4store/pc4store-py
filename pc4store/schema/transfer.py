from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from .enums import FiatMethodLocation, TxnType, TransferStatus, ResponseStatus


class Amount(BaseModel):
    full_amount: Decimal
    amount_after_tax: Decimal
    fee: Decimal


class FiatAmount(BaseModel):
    amount: Decimal
    fee: Decimal
    fiat_method_id: str


class FiatMethodInfo(BaseModel):
    name: str
    currency_name: str
    location: FiatMethodLocation


class CurrencyInfo(BaseModel):
    name: str
    smart_contract: str
    precission: int


class Transfer(BaseModel):
    id: str
    merchant_id: str
    amount: Amount
    fiat_amount: FiatAmount
    fiat_method: FiatMethodInfo

    currency: CurrencyInfo

    sender: str
    receiver: str
    txn_type: TxnType
    status: TransferStatus
    memo: str
    action: dict


class TransferPayload(BaseModel):
    transfer: Transfer


class TransferResponse(BaseModel):
    status: ResponseStatus
    payload: TransferPayload


class CreateTransferInput(BaseModel):
    amount: Decimal
    currency_name: str
    currency_smart_contract: str
    eos_account: str
    response_url: str
    fiat_method_id: Optional[str] = None

