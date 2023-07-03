from enum import Enum


class ResponseStatus(Enum):
    OK = 'OK'
    ERROR = 'ERROR'


class PaymentMethod(Enum):
    EOS = 'EOS'
    TRON = 'TRON'
    ETHER = 'ETHER'
    RUS_PAY = 'RUS_PAY'
    WORLD_PAY = 'WORLD_PAY'


class Blockchain(Enum):
    EOS = 'EOS'
    TRON = 'TRON'
    ETHER = 'ETHER'


class FiatMethodLocation(Enum):
    RUS_PAY = 'RUS_PAY'
    WORLD_PAY = 'WORLD_PAY'


class FiatMethodDirection(Enum):
    IN = 'IN'
    OUT = 'OUT'


class TxnType(Enum):
    ORDER_PAYMENT = 'ORDER_PAYMENT'
    PAYBACK = 'PAYBACK'
    DEPOSIT = 'DEPOSIT'
    WITHDRAW = 'WITHDRAW'


class OrderStatus(Enum):
    CREATED = 'CREATED'
    MONEY_RECEIVED = 'MONEY_RECEIVED'
    PAID = 'PAID'
    CANCELLED = 'CANCELLED'
    EXPIRED = 'EXPIRED'


class TransferStatus(Enum):
    INITIATED = 'INITIATED'
    SENDED = 'SENDED'
    RECEIVED = 'RECEIVED'
    ACCEPTED = 'ACCEPTED'
    DECLINED = 'DECLINED'
    FAILED = 'FAILED'
    PENDING = 'PENDING'
    RETRY = 'RETRY'
