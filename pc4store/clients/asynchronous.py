from dataclasses import asdict
from typing import Union, Optional
from aiohttp import request, BasicAuth

from pc4store.data import (
    CreateOrderInput, CreateOrderSuccess, CreateOrderError, OrderData
)
from .base import BaseClient


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
