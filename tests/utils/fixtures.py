import random
from decimal import Decimal
from string import ascii_lowercase, digits

CURRENCIES = (
    ('UAHCASH', 'cash.token'),
    ('RUBCASH', 'cash.token'),
    ('USDCASH', 'cash.token')
)


def rand_str(len_=7):
    alphabet = list(ascii_lowercase + digits)
    random.shuffle(alphabet)
    return ''.join(alphabet[:len_])


def rand_letters(len_=7):
    alphabet = list(ascii_lowercase)
    random.shuffle(alphabet)
    return ''.join(alphabet[:len_])


def rand_amount_in_coins(min_value=0, max_value=1000000000):
    return random.randint(min_value, max_value)


def rand_amount(min_value: Decimal = Decimal(0),
                max_value: Decimal = Decimal(10000),
                prec: int = 5):
    amount_in_coins = rand_amount_in_coins(int(min_value * 10 ** prec),
                                           int(max_value * 10 ** prec))
    return Decimal(amount_in_coins) / Decimal(10 ** prec)
