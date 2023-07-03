from typing import Callable, Any, TypeVar

import requests

from .base import BaseClient

M = TypeVar('M')


class Pc4StoreClient(BaseClient):
    def _request(self, method: str, path: str, json: Any, obj_loader: Callable[[dict], M]) -> M:
        response = requests.request(method, path, auth=(self.store_id, self.store_key), json=json)
        data = response.json()
        result_obj = obj_loader(data)
        return result_obj
