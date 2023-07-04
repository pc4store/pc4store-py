import hashlib
from uuid import uuid4

import pytest
from cryptography.exceptions import InvalidSignature

from pc4store.clients import Pc4StoreClient
from tests.utils.fabrics import rand_str


class MockPublicKey:
    def verify(self, *args, **kwargs):
        return True


class MockInvalidPublicKey:
    def verify(self, *args, **kwargs):
        raise InvalidSignature()


def test_is_signature_correct_success():
    client = Pc4StoreClient(
        store_id=str(uuid4()),
        store_key=str(uuid4()),
    )
    headers = {'SIGNATURE': hashlib.sha256(rand_str().encode()).hexdigest()}
    client.public_key = MockPublicKey()
    is_correct = client.is_signature_correct({}, headers)
    assert is_correct


def test_is_signature_correct_invalid_publickey():
    client = Pc4StoreClient(
        store_id=str(uuid4()),
        store_key=str(uuid4()),
    )
    headers = {'SIGNATURE': hashlib.sha256(rand_str().encode()).hexdigest()}
    client.public_key = MockInvalidPublicKey()
    is_correct = client.is_signature_correct({}, headers)
    assert not is_correct


def test_is_signature_correct_no_header():
    client = Pc4StoreClient(
        store_id=str(uuid4()),
        store_key=str(uuid4()),
    )
    with pytest.raises(AssertionError):
        client.is_signature_correct({}, {})
