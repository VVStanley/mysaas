from __future__ import annotations

import logging
from typing import Any, Dict, Optional, TypeVar, Type, Union

import httpx
from pydantic import BaseModel, ValidationError
from .exceptions import NotFoundException, APIException, ModelValidateException

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class BaseClient:

    def __init__(
        self,
        base_url: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: Union[float, httpx.Timeout] = 10.0,
        raise_for_status: bool = True,
        trust_env: bool = False,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {}
        self.timeout = timeout
        self.raise_for_status = raise_for_status
        self.trust_env = trust_env

    def build_url(self, path: str) -> str:
        if path.startswith(("http://", "https://")):
            return path
        return f"{self.base_url}/{path.lstrip('/')}"

    def handle_response(
        self,
        response: httpx.Response,
        expected_model: Optional[Type[T]] = None,
    ) -> Union[httpx.Response, T]:
        if self.raise_for_status:
            try:
                response.raise_for_status()
            except httpx.HTTPStatusError as exc:
                logger.error(
                    "HTTP error: %s %s -> %s %s",
                    response.request.method,
                    response.request.url,
                    response.status_code,
                    response.text,
                )
                if response.status_code == 404:
                    raise NotFoundException() from exc
                raise APIException() from exc

        if expected_model:
            try:
                return expected_model.model_validate_json(response.content)
            except ValidationError as e:
                logger.error("Ошибка парсинга модели: %s", e)
                raise ModelValidateException() from exc

        return response
