import json
from uuid import uuid4

import respx
from httpx import Response

from pc4store.clients import Pc4StoreClient
from pc4store.schema import FiatMethod, Currency
from tests.utils.fabrics import rand_currencies_response, rand_fiat_methods_response


@respx.mock
def test_get_fiat_methods():
    methods = rand_fiat_methods_response()

    get_fiat_route = respx.get("https://api.pc4.store/v1/fiat_methods").mock(
        return_value=Response(200, content=json.dumps(methods))
    )

    client = Pc4StoreClient(
        store_id=str(uuid4()),
        store_key=str(uuid4()),
    )

    result = client.get_fiat_methods().root
    assert get_fiat_route.call_count == 1

    assert isinstance(result, list)
    assert all(isinstance(obj, FiatMethod) for obj in result)
    assert len(result) == len(methods)


@respx.mock
def test_get_currencies():
    currencies = rand_currencies_response()

    get_currency_route = respx.get("https://api.pc4.store/v1/currencies").mock(
        return_value=Response(200, content=json.dumps(currencies))
    )

    client = Pc4StoreClient(
        store_id=str(uuid4()),
        store_key=str(uuid4()),
    )

    result = client.get_currencies().root
    assert get_currency_route.call_count == 1

    assert isinstance(result, list)
    assert all(isinstance(obj, Currency) for obj in result)
    assert len(result) == len(currencies)
