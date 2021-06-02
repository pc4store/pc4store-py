from dataclasses import asdict
from typing import Union, Optional
import requests

from pc4store.data import (
    CreateOrderInput, CreateOrderSuccess, CreateOrderError, OrderData, Transfer,
    TransferInput, TransferSuccess, TransferError
)
from .base import BaseClient


class Pc4StoreClient(BaseClient):
    def create_order(
            self,
            params: Union[CreateOrderInput, dict]
    ) -> Union[CreateOrderSuccess, CreateOrderError]:
        params = self._get_validated_create_order_input(params)
        response = requests.post(self.CREATE_ORDER,
                                 auth=(self.store_id, self.store_key),
                                 json=asdict(params))
        try:
            data = response.json()
            return self._get_formatted_create_order_res(data)
        except Exception as e:
            return CreateOrderError(error=str(e))

    def get_order(self, order_id: str) -> Optional[OrderData]:
        response = requests.get(f'{self.GET_ORDER}/{order_id}',
                                auth=(self.store_id, self.store_key))
        data = response.json()
        order_dict = data.pop('payload', {}).pop('order', None)
        return OrderData.from_dict(order_dict) if order_dict else None

    def transfer(
            self,
            params: Union[TransferInput, dict]
    ) -> Union[TransferSuccess, TransferError]:
        params = self._get_validated_transfer_input(params)
        response = requests.post(self.TRANSFER,
                                 auth=(self.store_id, self.store_key),
                                 json=asdict(params))
        try:
            data = response.json()
            return self._get_formatted_transfer_res(data)
        except Exception as e:
            return TransferError(error=str(e))

    def get_transfer(self, transfer_id: str) -> Optional[Transfer]:
        response = requests.get(f'{self.GET_TRANSFER}/{transfer_id}',
                                auth=(self.store_id, self.store_key))
        data = response.json()
        transfer_dict = data.pop('payload', {}).pop('transfer', None)
        return Transfer.from_dict(transfer_dict) if transfer_dict else None
