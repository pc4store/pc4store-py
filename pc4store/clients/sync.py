from typing import Callable, Any, TypeVar

from httpx import request

from .base import BaseClient

M = TypeVar("M")


class Pc4StoreClient(BaseClient):
    def _request(
            self, method: str, path: str, json: Any, obj_loader: Callable[[str], M]
    ) -> M:
        response = request(
            method, path, auth=(self.store_id, self.store_key), json=json
        )
        data = response.text
        # from devtools import debug
        # debug(response.json())

        return self._parse_response(obj_loader, data)
