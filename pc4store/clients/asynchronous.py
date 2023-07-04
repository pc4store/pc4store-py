from typing import Callable, TypeVar, Optional

from httpx import AsyncClient, BasicAuth

from pc4store.clients.base import BaseClient


M = TypeVar('M')


class Pc4StoreAsyncClient(BaseClient):
    def __init__(self, *args, client: Optional[AsyncClient] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self._client: AsyncClient = client or AsyncClient()

    async def _request(self, method: str, path: str, json: Optional[dict], obj_loader: Callable[[str], M]) -> M:
        response = await self._client.request(
            method,
            path,
            auth=BasicAuth(self.store_id, self.store_key),
            json=json
            )
        data = response.text
        return self._parse_response(obj_loader, data)
