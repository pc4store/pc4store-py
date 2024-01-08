import json
from decimal import Decimal
from uuid import uuid4

import pytest
import respx
from httpx import Response

from pc4store.clients import Pc4StoreClient
from pc4store.schema import CreateTransferInput, Transfer, Pc4StoreError
from tests.utils.fabrics import rand_transfer_response


@respx.mock
def test_create_transfer_success():
    transfer_id = str(uuid4())

    create_transfer_route = respx.post("https://api.pc4.store/v1/transfer").mock(
        return_value=Response(
            201,
            content=json.dumps(
                {"status": "OK", "payload": {"transfer_id": transfer_id}}
            ),
        )
    )

    client = Pc4StoreClient(
        store_id=str(uuid4()),
        store_key=str(uuid4()),
    )

    result = client.create_transfer(
        CreateTransferInput(
            amount=Decimal("25.5"),
            currency_name="USDT",
            currency_smart_contract="aabw2r.pcash",
            eos_account="5994532843",
            response_url="https://api.my-store/payment-callback/",
            fiat_method_id="ba94bdbf-b121-4add-b9c8-220af108e48e",
        )
    )

    assert create_transfer_route.call_count == 1
    assert result == transfer_id


@respx.mock
def test_create_transfer_error():
    create_transfer_route = respx.post("https://api.pc4.store/v1/transfer").mock(
        return_value=Response(
            400, content=json.dumps({"status": "ERROR", "error": "Error message"})
        )
    )

    client = Pc4StoreClient(
        store_id=str(uuid4()),
        store_key=str(uuid4()),
    )

    with pytest.raises(Pc4StoreError):
        result = client.create_transfer(
            CreateTransferInput(
                amount=Decimal("25.5"),
                currency_name="USDT",
                currency_smart_contract="aabw2r.pcash",
                eos_account="5994532843",
                response_url="https://api.my-store/payment-callback/",
                fiat_method_id="ba94bdbf-b121-4add-b9c8-220af108e48e",
            )
        )

    assert create_transfer_route.call_count == 1


@respx.mock
def test_get_transfer_success():
    transfer_id = str(uuid4())
    get_transfer_route = respx.get(
        "https://api.pc4.store/v1/transfer_info/" + transfer_id
    ).mock(return_value=Response(200, content=json.dumps(rand_transfer_response())))
    client = Pc4StoreClient(
        store_id=str(uuid4()),
        store_key=str(uuid4()),
    )
    result = client.get_transfer(transfer_id=transfer_id)
    assert get_transfer_route.call_count == 1
    assert isinstance(result, Transfer)


@respx.mock
def test_get_transfer_error():
    transfer_id = str(uuid4())
    get_transfer_route = respx.get(
        "https://api.pc4.store/v1/transfer_info/" + transfer_id
    ).mock(
        return_value=Response(
            400, content=json.dumps({
                "status": "ERROR",
                "error": "Error message",
                "error_type": "ErrorType",
            })
        )
    )
    client = Pc4StoreClient(
        store_id=str(uuid4()),
        store_key=str(uuid4()),
    )
    with pytest.raises(Pc4StoreError) as err:
        client.get_transfer(transfer_id=transfer_id)
    assert get_transfer_route.call_count == 1

    assert err.value.message == "Error message"
    assert err.value.error_type == "ErrorType"


@respx.mock
def test_get_transfer_by_merchant_id_success():
    transfer_id = str(uuid4())
    get_transfer_route = respx.get(
        "https://api.pc4.store/v1/transfer_info_by_merchant_id/" + transfer_id
    ).mock(return_value=Response(200, content=json.dumps(rand_transfer_response())))
    client = Pc4StoreClient(
        store_id=str(uuid4()),
        store_key=str(uuid4()),
    )
    result = client.get_transfer_by_merchant_id(merchant_id=transfer_id)
    assert get_transfer_route.call_count == 1
    assert isinstance(result, Transfer)
