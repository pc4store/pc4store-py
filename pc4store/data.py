import dataclasses
from dataclasses import dataclass, fields
from datetime import datetime
from enum import Enum


@dataclass
class CreateOrderInput:
    currency_name: str
    currency_smart_contract: str
    amount_to_pay: str
    response_url: str
    expiration_time: int = None
    merchant_order_id: str = None
    description: str = None
    success_payment_redirect_url: str = None
    failed_payment_redirect_url: str = None

    @classmethod
    def from_dict(cls, input_: dict):
        expected_fields = cls.__dataclass_fields__.items()
        required_fields = [field for field, type_ in expected_fields if
                           type_.default == dataclasses.MISSING]
        for field in required_fields:
            assert input_.get(
                field) is not None, f'Missing required field {field}'
        unexpected = set(input_) - set([field for field, _ in expected_fields])
        assert not unexpected, f'Got unexpected params: {list(unexpected)}'
        return cls(**input_)


class OrderStatus(Enum):
    CREATED = 'CREATED'
    MONEY_RECEIVED = 'MONEY_RECEIVED'
    PAID = 'PAID'
    EXPIRED = 'EXPIRED'
    CANCELLED = 'CANCELLED'


class TxnType(Enum):
    ORDER_PAYMENT = 'ORDER_PAYMENT'
    PAYBACK = 'PAYBACK'


class TxnStatus(Enum):
    INITIATED = 'INITIATED'  # initiated payback
    SENDED = 'SENDED'  # sended payback
    RECEIVED = 'RECEIVED'  # txn found and start proccess
    ACCEPTED = 'ACCEPTED'  # txn processed with success


@dataclass
class Amount:
    full_amount: str
    amount_after_tax: str
    fee: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


@dataclass
class Currency:
    name: str
    smart_contract: str
    precission: int

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


@dataclass
class OrderDetails:
    merchant_order_id: str = None
    description: str = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


@dataclass
class Action:
    txid: str
    block_number: str
    global_sequence: str
    is_irreversible: str
    is_reversed: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


@dataclass
class Transfer:
    id: str
    amount: Amount
    currency: Currency
    sender: str
    receiver: str
    txn_type: TxnType
    status: TxnStatus
    action: Action
    memo: str = ''

    @classmethod
    def from_dict(cls, data: dict):
        return cls(amount=Amount.from_dict(data.pop('amount')),
                   currency=Currency.from_dict(data.pop('currency')),
                   action=Action.from_dict(data.pop('action')),
                   **data)


@dataclass
class OrderData:
    id: str
    sequent_number: str
    amount: Amount
    currency: Currency
    status: OrderStatus
    expiration_date: datetime
    payment_url: str
    response_url: str
    is_test: bool
    details: OrderDetails
    success_payment_redirect_url: str = None
    failed_payment_redirect_url: str = None
    payment_transfer: Transfer = None

    @classmethod
    def from_dict(cls, data: dict):
        payment_transfer = Transfer.from_dict(
                       data.pop('payment_transfer')
                   ) if 'payment_transfer' in data else None
        return cls(amount=Amount.from_dict(data.pop('amount')),
                   currency=Currency.from_dict(data.pop('currency')),
                   payment_transfer=payment_transfer,
                   **data)


@dataclass
class Payload:
    order: OrderData

    @classmethod
    def from_dict(cls, data: dict):
        return cls(order=OrderData.from_dict(data['order']))


@dataclass
class SuccessResponse:
    payload: Payload
    status = 'OK'

    @classmethod
    def from_dict(cls, data: dict):
        return cls(payload=Payload.from_dict(data['payload']))


@dataclass
class ErrorResponse:
    error: str
    status = 'ERROR'


@dataclass
class CreateOrderSuccess(SuccessResponse):
    ...


@dataclass
class CreateOrderError(ErrorResponse):
    ...
