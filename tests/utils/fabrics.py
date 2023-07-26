import random
from decimal import Decimal
from string import ascii_lowercase, digits
from uuid import uuid4

CURRENCIES = (
    ("UAHCASH", "cash.token"),
    ("RUBCASH", "cash.token"),
    ("USDCASH", "cash.token"),
)


def rand_str(len_=7):
    alphabet = list(ascii_lowercase + digits)
    random.shuffle(alphabet)
    return "".join(alphabet[:len_])


def rand_letters(len_=7):
    alphabet = list(ascii_lowercase)
    random.shuffle(alphabet)
    return "".join(alphabet[:len_])


def rand_amount_in_coins(min_value=0, max_value=1000000000):
    return random.randint(min_value, max_value)


def rand_amount(
        min_value: Decimal = Decimal(0), max_value: Decimal = Decimal(10000), prec: int = 5
):
    amount_in_coins = rand_amount_in_coins(
        int(min_value * 10 ** prec), int(max_value * 10 ** prec)
    )
    return Decimal(amount_in_coins) / Decimal(10 ** prec)


def rand_order_response():
    return {
        "status": "OK",
        "payload": {
            "order": {
                "id": str(uuid4()),
                "sequent_number": 36,
                "amount": {
                    "full_amount": "999.0000",
                    "amount_after_tax": "999.0000",
                    "fee": "0.0000",
                },
                "currency": {
                    "name": rand_str(),
                    "smart_contract": rand_str(),
                    "precission": 3,
                },
                "status": "CREATED",
                "expiration_date": "2023-07-05T16:23:52",
                "response_url": "https://api.my-store/payment-callback/",
                "payment_url": "https://pc4.store/payment/" + str(uuid4()),
                "success_payment_redirect_url": "https://my-store/orders/12345/success",
                "failed_payment_redirect_url": "https://my-store/orders/12345/failed",
                "is_test": False,
                "details": {
                    "merchant_order_id": "12345",
                    "description": "optional description for this order",
                },
                "allowed_methods": [
                    "TRON",
                    "WORLD_PAY",
                    "RUS_PAY",
                    "EOS",
                    "ETHER",
                ],
                'payment_transfer': {
                    'action': {
                        'block_number': 54321,
                        'global_sequence': 500400,
                        'is_irreversible': True,
                        'is_reversed': False,
                        'txid': '5a8e6360bc7372370000000000000000000001771a74127242b87ce1cac10513'
                    },
                    'amount': {'amount_after_tax': '10.00000',
                               'fee': '0.00000',
                               'full_amount': '10.00000'},
                    'currency': {'name': 'USDT',
                                 'precission': 5,
                                 'smart_contract': 'SC'},
                    'fiat_amount': None,
                    'fiat_method': None,
                    'id': '06dbefaf-6fa9-4799-b74d-ce0bab531d0a',
                    'memo': None,
                    'merchant_id': None,
                    'receiver': 'store.pcash',
                    'sender': 'esaxv659ul',
                    'status': 'ACCEPTED',
                    'txn_type': 'ORDER_PAYMENT'
                },
                'transfers': [
                    {
                        'action': {
                            'block_number': 54322,
                            'global_sequence': 500401,
                            'is_irreversible': True,
                            'is_reversed': False,
                            'txid': '4a8e6460b47374370000000000000000000001741a74127242b874e4cac14514'
                        },
                        'amount': {'amount_after_tax': '10.00000',
                                   'fee': '0.00000',
                                   'full_amount': '10.00000'},
                        'currency': {'name': 'USDT',
                                     'precission': 5,
                                     'smart_contract': 'SC'},
                        'fiat_amount': None,
                        'fiat_method': None,
                        'id': '06dbefaf-6fa9-4799-b74d-ce0bab531d0a',
                        'memo': None,
                        'merchant_id': None,
                        'receiver': 'store.pcash',
                        'sender': 'esaxv659ul',
                        'status': 'ACCEPTED',
                        'txn_type': 'PAYBACK'
                    },
                ]
            },
        },
    }


def rand_transfer_response():
    return {
        "status": "OK",
        "payload": {
            "transfer": {
                "id": str(uuid4()),
                "amount": {
                    "full_amount": str(rand_amount()),
                    "amount_after_tax": str(rand_amount()),
                    "fee": str(rand_amount()),
                },
                "fiat_amount": {
                    "amount": str(rand_amount()),
                    "fee": str(rand_amount()),
                    "fiat_method_id": str(uuid4()),
                },
                "fiat_method": {
                    "name": rand_letters(),
                    "currency_name": rand_letters(),
                    "location": "WORLD_PAY",
                },
                "currency": {
                    "name": rand_letters(),
                    "smart_contract": rand_letters(),
                    "precission": 4,
                },
                "sender": rand_letters(),
                "receiver": rand_letters(),
                "txn_type": "WITHDRAW",
                "status": "FAILED",
                "memo": rand_letters(),
                "action": {},
            }
        },
    }


def rand_fiat_methods_response():
    return [
        {
            "currency_name": rand_str(),
            "direction": "IN",
            "fee_fix": "1.00",
            "fee_percentage": "0.010000",
            "id": str(uuid4()),
            "location": "RUS_PAY",
            "minimal_amount": "0.10",
            "maximal_amount": "10000.00",
            "name": rand_str(),
            "rates": [
                {
                    "currency_id": "02fda23b-67be-45fd-b2ee-85ebafa059f6",
                    "rate": "85.000000",
                }
            ],
        }
    ] * random.randint(0, 5)


def rand_currencies_response():
    return [
        {
            "id": str(uuid4()),
            "name": rand_letters(),
            "blockchain": "EOS",
            "smart_contract": rand_letters(),
            "precission": 6,
            "min_transfer_amount": "0.010000",
            "is_income_enabled": True,
            "is_outcome_enabled": True,
            "fee_fix": "0",
            "fee_percentage": "0",
            "withdraw_fee_fix": "0",
            "withdraw_fee_percentage": "0",
            "txn_limit": None,
            "account_limit": None,
            "day_limit": None,
            "txn_cap": None,
            "account_cap": None,
            "day_cap": None,
        }
    ] * random.randint(0, 5)
