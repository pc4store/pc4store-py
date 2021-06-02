import hashlib
import json
import random
from uuid import uuid4

import mock

import pytest
from cryptography.exceptions import InvalidSignature

from pc4store.clients.base import BaseClient
from pc4store.data import CreateOrderInput, ErrorResponse, CreateOrderSuccess

from tests.data import full_input, min_input, success_response, error_response
from tests.data import order_data
from tests.utils.fixtures import rand_str


@pytest.mark.parametrize('input_data', [full_input(),
                                        min_input(),
                                        CreateOrderInput(**full_input()),
                                        CreateOrderInput(**min_input()),
                                        ])
def test__get_validated_create_input__correct_input(input_data):
    res = BaseClient._get_validated_create_order_input(input_data)
    assert isinstance(res, CreateOrderInput)


def test__get_validated_create_input__incorrect_input_type():
    with pytest.raises(AssertionError):
        BaseClient._get_validated_create_order_input(list())


@mock.patch('pc4store.data.CreateOrderInput.from_dict', side_effect=ValueError)
def test__get_validated_create_input__invalid_input(from_dict_mock):
    with pytest.raises(ValueError):
        BaseClient._get_validated_create_order_input(min_input())


def test__get_formatted_create_res__succress():
    resp_dict = success_response()
    resp = BaseClient._get_formatted_create_order_res(resp_dict)
    assert isinstance(resp, CreateOrderSuccess)


def test__get_formatted_create_res__error():
    resp_dict = error_response()
    resp = BaseClient._get_formatted_create_order_res(resp_dict)
    assert isinstance(resp, ErrorResponse)


class MockPublicKey:
    def verify(self, *args, **kwargs):
        return True


class MockPublicKeyFaile:
    def verify(self, *args, **kwargs):
        raise InvalidSignature()


class TestIsSignatureCorrectMethod:
    @classmethod
    def setup(cls):
        cls.client = BaseClient(str(uuid4()), str(uuid4()))
        cls.data = order_data()
        cls.headers = {
            'SIGNATURE': hashlib.sha256(rand_str().encode()).hexdigest()}

    def test__is_signature_correct__success(self):
        self.client.public_key = MockPublicKey()
        is_correct = self.client.is_signature_correct(self.data, self.headers)
        assert is_correct

    def test__is_signature_correct__invalid_signature(self):
        self.client.public_key = MockPublicKeyFaile()
        is_correct = self.client.is_signature_correct(self.data, self.headers)
        assert not is_correct

    def test__is_signature_correct__has_no_header(self):
        del self.headers['SIGNATURE']
        with pytest.raises(AssertionError):
            self.client.is_signature_correct(self.data, self.headers)
