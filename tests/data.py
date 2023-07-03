import random
from datetime import datetime, timedelta
from uuid import uuid4

import pytest

from tests.utils.fixtures import rand_str, CURRENCIES, rand_amount
from pc4store.data import CreateOrderInput, Amount, OrderStatus, TxnType, \
    TxnStatus


def min_input():
    currency_name, currency_smart = random.choice(CURRENCIES)
    return {
        'currency_name': currency_name,
        'currency_smart_contract': currency_smart,
        'amount_to_pay': str(rand_amount()),
        'response_url': rand_str(),
    }


def full_input():
    return {
        'currency_name': random.choice(CURRENCIES),
        'currency_smart_contract': 'cash.token',
        'amount_to_pay': str(rand_amount()),
        'response_url': rand_str(),
        'expiration_time': random.randint(10, 40),
        'merchant_order_id': rand_str(),
        'description': rand_str(),
        'success_payment_redirect_url': rand_str(),
        'failed_payment_redirect_url': rand_str()
    }


def rand_formatted_amount():
    return {
        'full_amount': str(rand_amount()),
        'amount_after_tax': str(rand_amount()),
        'fee': str(rand_amount())
    }


def rand_curency():
    currency_name, currency_smart = random.choice(CURRENCIES)
    return {
        'name': currency_name,
        'smart_contract': currency_smart,
        'precission': 5
    }


def order_details():
    return {
        'merchant_order_id': rand_str(),
        'description': rand_str()
    }


def rand_action():
    return {
        'txid': rand_str(),
        'block_number': str(random.randint(1, 100)),
        'global_sequence': str(random.randint(1, 100)),
        'is_irreversible': random.choice((True, False)),
        'is_reversed': random.choice((True, False))
    }


def rand_transfer():
    return {
        'id': str(uuid4()),
        'amount': rand_formatted_amount(),
        'currency': rand_curency(),
        'sender': rand_str(),
        'receiver': rand_str(),
        'txn_type': TxnType.ORDER_PAYMENT.name,
        'status': TxnStatus.ACCEPTED.name,
        'action': rand_action(),
        'memo': rand_str()
    }


def order_data():
    return {
        'id': str(uuid4()),
        'sequent_number': str(random.randint(1, 100)),
        'amount': rand_formatted_amount(),
        'currency': rand_curency(),
        'status': random.choice(list(OrderStatus)).name,
        'expiration_date': (datetime.utcnow() + timedelta(
            minutes=random.randint(1, 100))).isoformat(),
        'payment_url': rand_str(),
        'response_url': rand_str(),
        'is_test': random.choice((True, False)),
        'details': order_details(),
        'payment_transfer': rand_transfer()
    }


def rand_payload():
    return {
        'order': order_data()
    }


def success_response():
    return {
        'status': 'OK',
        'payload': rand_payload()
    }


def error_response():
    return {
        'status': 'ERROR',
        'error': rand_str()
    }


@pytest.fixture
def min_dict_input():
    return min_input()


@pytest.fixture
def full_dict_input():
    return full_input()


@pytest.fixture
def min_dataclass_input():
    return CreateOrderInput(**min_input())


@pytest.fixture
def full_dataclass_input():
    return CreateOrderInput(**full_input())
