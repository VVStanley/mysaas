from ._base import BaseClient
import logging
from typing import Any, Dict, Optional, TypeVar, Type, Union
import httpx
from pydantic import BaseModel, ValidationError

T = TypeVar("T", bound=BaseModel)


class AsyncClient(BaseClient):
    def __init__(
        self,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=self.headers,
            timeout=self.timeout,
            trust_env=self.trust_env,
        )

    async def __aenter__(self) -> "AsyncClient":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self._client.aclose()

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Any] = None,
        data: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_model: Optional[Type[T]] = None,
    ) -> Union[httpx.Response, T]:
        url = self.build_url(path)
        response = await self._client.request(
            method,
            url,
            params=params,
            json=json,
            data=data,
            headers=headers or self.headers,
            timeout=self.timeout,
        )
        return self.handle_response(response, expected_model)

    async def get(self, path: str, **kwargs) -> Union[httpx.Response, T]:
        return await self.request("GET", path, **kwargs)

    async def post(self, path: str, **kwargs) -> Union[httpx.Response, T]:
        return await self.request("POST", path, **kwargs)

    async def put(self, path: str, **kwargs) -> Union[httpx.Response, T]:
        return await self.request("PUT", path, **kwargs)

    async def delete(self, path: str, **kwargs) -> Union[httpx.Response, T]:
        return await self.request("DELETE", path, **kwargs)
