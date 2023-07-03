from typing import Callable, Any, TypeVar, Optional

# from aiohttp import request, BasicAuth
from httpx import AsyncClient, BasicAuth

from pc4store.clients.base import BaseClient
from pc4store.schema.exceptions import Pc4StoreError, Pc4StoreErrorResponse

from pydantic import ValidationError


M = TypeVar('M')


class Pc4StoreAsyncClient(BaseClient):
    def __init__(self, *args, client: Optional[AsyncClient] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self._client = client or AsyncClient()

    async def __aenter__(self):
        return await self._client.__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return await self._client.__aexit__(exc_type, exc_val, exc_tb)

    async def _request(self, method: str, path: str, json: Optional[dict], obj_loader: Callable[[str], M]) -> M:
        async with self._client.request(method, path,
                                        auth=BasicAuth(self.store_id, self.store_key),
                                        json=json
                                        ) as response:
            data = await response.text()
            return self._parse_response(obj_loader, data)
