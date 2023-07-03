import hashlib
import json
from abc import ABC, abstractmethod
from typing import Union, Callable, TypeVar, Awaitable, Optional

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from pc4store.schema.currency import Currency, CurrencyList
from pc4store.schema.fiat import FiatMethod, FiatMethodList
from pc4store.schema.order import CreateOrderInput, Order, OrderResponse
from pc4store.schema.transfer import CreateTransferInput, Transfer, TransferResponse
from pc4store.schema.exceptions import Pc4StoreError, Pc4StoreErrorResponse

from pydantic import ValidationError

M = TypeVar('M')


class BaseClient(ABC):

    def __init__(self, store_id: str,
                 store_key: str,
                 store_public_key: Union[
                     str, bytes, Ed25519PublicKey] = '69f72437e2e359a3e5c29fe9a7e0d509345cc57b7bfca0b470598d679a349806',
                 store_base_url: str = 'https://api.pc4.store',
                 ):
        self.store_id = store_id
        self.store_key = store_key
        self.base_url = store_base_url
        if isinstance(store_public_key, str):
            store_public_key = bytes(bytearray.fromhex(store_public_key))
        if isinstance(store_public_key, bytes):
            store_public_key = Ed25519PublicKey.from_public_bytes(store_public_key)
        if isinstance(store_public_key, Ed25519PublicKey):
            self.public_key = store_public_key

    def create_order(self, input_: CreateOrderInput) -> Union[Order, Awaitable[Order]]:
        json_ = input_.model_dump(mode='json', exclude_none=True)

        def load_obj(data: str) -> Order:
            resp = OrderResponse.model_validate_json(data)
            return resp.payload.order

        return self._request(
            'POST',
            rf'{self.base_url}/v1/create',
            json_,
            load_obj
        )

    def get_order(self, order_id: str) -> Union[Order, Awaitable[Order]]:
        def load_obj(data: str) -> Order:
            resp = OrderResponse.model_validate_json(data)
            return resp.payload.order

        return self._request(
            'GET',
            rf'{self.base_url}/v1/order_info/{order_id}',
            None,
            load_obj
        )

    def create_transfer(self, input_: CreateTransferInput) -> Union[Transfer, Awaitable[Transfer]]:
        json = input_.model_dump(mode='json', exclude_none=True)

        def load_obj(data: str) -> Transfer:
            resp = TransferResponse.model_validate_json(data)
            return resp.payload.order

        return self._request(
            'POST',
            rf'{self.base_url}/v1/transfer',
            json,
            load_obj
        )

    def get_transfer(self, transfer_id: str) -> Union[Transfer, Awaitable[Transfer]]:
        def load_obj(data: str) -> Transfer:
            resp = TransferResponse.model_validate_json(data)
            return resp.payload.order

        return self._request(
            'GET',
            rf'{self.base_url}/v1/transfer_info/{transfer_id}',
            None,
            load_obj
        )

    def get_currencies(self) -> Union[list[Currency], Awaitable[list[Currency]]]:
        return self._request(
            'GET',
            rf'{self.base_url}/v1/currencies',
            None,
            CurrencyList.validate_json
        )

    def get_fiat_methods(self) -> Union[list[FiatMethod], Awaitable[list[FiatMethod]]]:
        return self._request(
            'GET',
            rf'{self.base_url}/v1/fiat_methods',
            None,
            FiatMethodList.validate_json
        )

    def is_signature_correct(self, json_body: dict, headers: dict) -> bool:
        signature = headers.get('SIGNATURE')
        assert signature is not None
        str_body = json.dumps(json_body, separators=(',', ':'))
        hash_body = hashlib.sha256(str_body.encode()).hexdigest()
        try:
            self.public_key.verify(bytes(bytearray.fromhex(signature)),
                                   bytes(bytearray.fromhex(hash_body)))
        except Exception:
            return False
        return True

    @staticmethod
    def _parse_response(obj_loader: Callable[[str], M], data: str) -> M:
        try:
            result_obj = obj_loader(data)
            return result_obj
        except ValidationError as v_err:
            try:
                pc4store_err = Pc4StoreErrorResponse.model_validate_json(data)
            except ValidationError:
                raise v_err  # trigger initial ValidationError because the response is not an error
            else:
                raise Pc4StoreError(pc4store_err) from None

    @abstractmethod
    def _request(self, method: str, path: str, json: Optional[dict], obj_loader: Callable[[str], M]) -> M:
        ...