from dataclasses import asdict
from typing import Union, Optional
import requests

from pc4store.data import (
    CreateOrderInput, CreateOrderSuccess, CreateOrderError, OrderData
)
from .base import BaseClient


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
