from datetime import datetime
from decimal import Decimal
from typing import Optional, List

from pydantic import BaseModel, AnyUrl, AnyHttpUrl

from .enums import OrderStatus, PaymentMethod, ResponseStatus
from .transfer import Amount, CurrencyInfo, Transfer


class CreateOrderInput(BaseModel):
    amount_to_pay: Decimal
    currency_name: str
    currency_smart_contract: str
    response_url: AnyHttpUrl
    expiration_time: Optional[int] = None
    merchant_order_id: Optional[str] = None
    description: Optional[str] = None
    success_payment_redirect_url: Optional[AnyUrl] = None
    failed_payment_redirect_url: Optional[AnyUrl] = None
    allowed_methods: Optional[List[PaymentMethod]] = None


class OrderDetails(BaseModel):
    merchant_order_id: Optional[str] = None
    description: Optional[str] = None


class Order(BaseModel):
    id: str
    sequent_number: int
    amount: Amount
    currency: CurrencyInfo
    status: OrderStatus
    expiration_date: datetime
    payment_url: str
    response_url: Optional[str] = None
    success_payment_redirect_url: Optional[str] = None
    failed_payment_redirect_url: Optional[str] = None
    is_test: bool
    details: OrderDetails
    payment_transfer: Optional[Transfer] = None
    transfers: Optional[List[Transfer]] = None
    allowed_methods: list[PaymentMethod]


class OrderPayload(BaseModel):
    order: Order


class OrderResponse(BaseModel):
    status: ResponseStatus
    payload: OrderPayload
