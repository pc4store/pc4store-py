from uuid import uuid4

import mock
import pytest

from pc4store.clients import Pc4StoreClient
from pc4store.data import CreateOrderSuccess, CreateOrderError
from tests.data import success_response, full_dict_input, error_response


class MockSuccessResponse:
    def json(self):
        return success_response()


class MockErrorResponse:
    def json(self):
        return error_response()


class MockExceptionResponse:
    def json(self):
        return error_response()


@pytest.mark.usefixtures(full_dict_input.__name__)
class TestCreateOrderMethod:
    """
    Tests for Pc4StoreClient.create_order method
    """

    @classmethod
    def setup(cls):
        cls.client = Pc4StoreClient(str(uuid4()), str(uuid4()))

    @mock.patch('requests.post', return_value=MockSuccessResponse())
    def test_success(self, post_mock, full_dict_input):
        res = self.client.create_order(full_dict_input)
        assert isinstance(res, CreateOrderSuccess)

    @mock.patch('requests.post', return_value=MockErrorResponse())
    def test_error_response(self, post_mock, full_dict_input):
        res = self.client.create_order(full_dict_input)
        assert isinstance(res, CreateOrderError)

    @mock.patch('requests.post', return_value=MockErrorResponse())
    def test_error_response(self, post_mock, full_dict_input):
        res = self.client.create_order(full_dict_input)
        assert isinstance(res, CreateOrderError)
