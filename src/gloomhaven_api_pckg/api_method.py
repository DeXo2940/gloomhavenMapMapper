from __future__ import annotations
from typing import Callable

from .http_method import HttpMethod


class ApiMethod:
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"

    def __init__(
        self,
        http_method: HttpMethod,
        callable_method: Callable,
        parameters: str = "",
        endpoint_sufix: str = "",
    ) -> None:
        self._http_method = http_method
        self._callable_method = callable_method
        self._parameters = parameters
        self._endpoint_sufix = endpoint_sufix

    @staticmethod
    def create(
        http_method: HttpMethod,
        callable_method: Callable,
        parameters: str = "",
        endpoint_sufix: str = "",
    ) -> ApiMethod:
        return ApiMethod(http_method, callable_method, parameters, endpoint_sufix)

    @property
    def http_method(self) -> str:
        return self._http_method.name

    @property
    def callable_method(self) -> Callable:
        return self._callable_method

    @property
    def endpoint_sufix(self) -> str:
        return (
            f"_{self.http_method.lower()}"
            if self._endpoint_sufix == ""
            else f"_{self.http_method.lower()}_{self._endpoint_sufix}"
        )

    @property
    def parameters(self) -> str:
        return f"/{self._parameters}" if self._parameters != "" else ""
