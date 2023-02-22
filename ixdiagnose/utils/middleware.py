import contextlib

from dataclasses import dataclass
from middlewared.client import Client
from typing import Any, Callable, List, Optional


@contextlib.contextmanager
def get_middleware_client() -> Client:
    with Client() as client:
        yield client


@dataclass
class MiddlewareResponse:

    result_key: str
    error: Optional[str] = None
    output: Any = None


class MiddlewareCommand:
    def __init__(
        self, endpoint: str, api_payload: Optional[List] = None, format_output: Optional[Callable] = None,
        result_key: Optional[str] = None
    ):
        self.endpoint: str = endpoint
        self.overridden_format_output: Optional[Callable] = format_output
        self.payload: List = api_payload or []
        self.result_key: str = result_key

    def format_output(self, output: Any) -> Any:
        return self.overridden_format_output(output) if self.overridden_format_output else output

    def execute(self) -> MiddlewareResponse:
        response = MiddlewareResponse(result_key=self.result_key or self.endpoint)
        try:
            with get_middleware_client() as client:
                response.output = client.call(self.endpoint, *self.payload)
        except Exception as e:
            response.error = str(e)
        else:
            try:
                response.output = self.format_output(response.output)
            except Exception as e:
                response.error = f'Failed to clean {self.endpoint!r} output: {e}'

        return response
