from typing import Callable, Any, TypeVar

from aiohttp import request, BasicAuth

from pc4store.clients.base import BaseClient

M = TypeVar('M')


class Pc4StoreAsyncClient(BaseClient):
    async def _request(self, method: str, path: str, json: Any, obj_loader: Callable[[dict], M]) -> M:
        async with request(method, path,
                           auth=BasicAuth(self.store_id, self.store_key),
                           json=json
                           ) as response:
            data = await response.json()
            result_obj = obj_loader(data)
            return result_obj
