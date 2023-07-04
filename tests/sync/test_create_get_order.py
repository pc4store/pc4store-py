import json
from uuid import uuid4

import pytest
import respx
from httpx import Response

from pc4store.clients import Pc4StoreClient
from pc4store.schema import CreateOrderInput, Order, Pc4StoreError
from tests.utils.fabrics import rand_order_response, rand_amount, rand_letters


@respx.mock
def test_create_order_success():
    create_order_route = respx.post("https://api.pc4.store/v1/create").mock(
        return_value=Response(201, content=json.dumps(rand_order_response()))
    )

    client = Pc4StoreClient(
        store_id=str(uuid4()),
        store_key=str(uuid4()),
    )

    result = client.create_order(
        CreateOrderInput(
            amount_to_pay=rand_amount(),
            currency_name=rand_letters(),
            currency_smart_contract=rand_letters(),
            response_url="https://my_callback_url.net",
        )
    )

    assert create_order_route.call_count == 1
    assert isinstance(result, Order)


@respx.mock
def test_create_order_error():
    create_order_route = respx.post("https://api.pc4.store/v1/create").mock(
        return_value=Response(
            400, content=json.dumps({"status": "ERROR", "error": "Error message"})
        )
    )

    client = Pc4StoreClient(
        store_id=str(uuid4()),
        store_key=str(uuid4()),
    )

    with pytest.raises(Pc4StoreError):
        result = client.create_order(
            CreateOrderInput(
                amount_to_pay=rand_amount(),
                currency_name=rand_letters(),
                currency_smart_contract=rand_letters(),
                response_url="https://my_callback_url.net",
            )
        )

    assert create_order_route.call_count == 1


@respx.mock
def test_get_order_success():
    order_id = str(uuid4())
    get_order_route = respx.get("https://api.pc4.store/v1/order_info/" + order_id).mock(
        return_value=Response(200, content=json.dumps(rand_order_response()))
    )
    client = Pc4StoreClient(
        store_id=str(uuid4()),
        store_key=str(uuid4()),
    )
    result = client.get_order(order_id=order_id)
    assert get_order_route.call_count == 1
    assert isinstance(result, Order)


@respx.mock
def test_get_order_error():
    order_id = str(uuid4())
    get_order_route = respx.get("https://api.pc4.store/v1/order_info/" + order_id).mock(
        return_value=Response(
            400, content=json.dumps({"status": "ERROR", "error": "Error message"})
        )
    )
    client = Pc4StoreClient(
        store_id=str(uuid4()),
        store_key=str(uuid4()),
    )
    with pytest.raises(Pc4StoreError):
        result = client.get_order(order_id=order_id)

    assert get_order_route.call_count == 1
