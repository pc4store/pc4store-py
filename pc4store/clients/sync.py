import hashlib
import json
from dataclasses import asdict
from typing import Union, Optional
import requests
from aiohttp import request, BasicAuth

from pc4store import config

from pc4store.data import CreateOrderInput, CreateOrderSuccess, \
    CreateOrderError, OrderData
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey


class BaseClient:
    CREATE_ORDER = f'{config.HOST}/create'
    GET_ORDER = f'{config.HOST}/order'

    def __init__(self, store_id: str, store_key: str):
        self.store_id = store_id
        self.store_key = store_key
        self.public_key: Ed25519PublicKey = Ed25519PublicKey.from_public_bytes(
            bytes(bytearray.fromhex(config.PUBLIC_KEY)))

    @classmethod
    def _get_validated_create_input(cls, params: Union[CreateOrderInput, dict]
                                    ) -> CreateOrderInput:
        assert isinstance(params, (CreateOrderInput, dict))
        if isinstance(params, dict):
            return CreateOrderInput.from_dict(params)

    @classmethod
    def _get_formatted_create_res(
            cls, data: dict
    ) -> Union[CreateOrderSuccess, CreateOrderError]:
        if data['status'] == 'OK':
            return CreateOrderSuccess.from_dict(**data)
        else:
            return CreateOrderError(error=data.get('error'))

    def is_signature_correct(self, json_body: dict, signature: str) -> bool:
        str_body = json.dumps(json_body, separators=(',', ':'))
        hashlib.sha256(str_body.encode()).hexdigest()
        try:
            self.public_key.verify(bytes(bytearray.fromhex(signature)),
                                   bytes(bytearray(str_body)))
        except Exception:
            return False
        return True


class Pc4StoreClient(BaseClient):
    def create_order(
            self,
            params: Union[CreateOrderInput, dict]
    ) -> Union[CreateOrderSuccess, CreateOrderError]:
        params = self._get_validated_create_input(params)
        response = requests.post(self.CREATE_ORDER,
                                 auth=(self.store_id, self.store_key),
                                 json=asdict(params))
        try:
            data = response.json()
            return self._get_formatted_create_res(data)
        except Exception as e:
            return CreateOrderError(error=str(e))

    def get_order(self, order_id: str) -> Optional[OrderData]:
        response = requests.get(f'{self.GET_ORDER}/{order_id}',
                                auth=(self.store_id, self.store_key))
        data = response.json()
        order_dict = data.pop('payload', {}).pop('order', None)
        return OrderData.from_dict(order_dict) if order_dict else None


class Pc4StoreAsyncClient(BaseClient):
    async def create_order(
            self,
            params: Union[CreateOrderInput, dict]
    ) -> Union[CreateOrderSuccess, CreateOrderError]:
        params = self._get_validated_create_input(params)
        async with request('POST', self.CREATE_ORDER,
                           auth=BasicAuth(self.store_id, self.store_key),
                           json=asdict(params)
                           ) as response:
            try:
                data = await response.json()
                return self._get_formatted_create_res(data)
            except Exception as e:
                return CreateOrderError(error=str(e))

    async def get_order(self, order_id: str) -> Optional[OrderData]:
        async with request('GET', f'{self.GET_ORDER}/{order_id}',
                           auth=BasicAuth(self.store_id, self.store_key),
                           ) as response:
            data = await response.json()
            order_dict = data.pop('payload', {}).pop('order', None)
            return OrderData.from_dict(order_dict) if order_dict else None
