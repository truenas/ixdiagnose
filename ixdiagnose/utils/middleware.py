import contextlib

from dataclasses import dataclass
from ixdiagnose.config import conf
from truenas_api_client import Client
from typing import Any, Callable, List, Optional, TypeAlias


MiddlewareClient: TypeAlias = Client


@contextlib.contextmanager
def get_middleware_client() -> Client:
    with Client(call_timeout=conf.timeout) as client:
        yield client


@dataclass
class MiddlewareResponse:

    result_key: str
    error: Optional[str] = None
    output: Any = None


class MiddlewareCommand:
    def __init__(
        self, endpoint: str, api_payload: Optional[List] = None, format_output: Optional[Callable] = None,
        result_key: Optional[str] = None, job: bool = False,
    ):
        self.endpoint: str = endpoint
        self.overridden_format_output: Optional[Callable] = format_output
        self.payload: List = api_payload or []
        self.result_key: str = result_key or self.endpoint.replace('.', '_')
        self.job: bool = job

    def format_output(self, output: Any) -> Any:
        return self.overridden_format_output(output) if self.overridden_format_output else output

    def execute(self, middleware_client: Optional[MiddlewareClient] = None) -> MiddlewareResponse:
        response = MiddlewareResponse(result_key=self.result_key)
        try:
            if middleware_client:
                response.output = middleware_client.call(self.endpoint, *self.payload, job=self.job)
            else:
                with get_middleware_client() as client:
                    response.output = client.call(self.endpoint, *self.payload, job=self.job)
        except Exception as e:
            response.error = str(e)
        else:
            try:
                response.output = self.format_output(response.output)
            except Exception as e:
                response.error = f'Failed to clean {self.endpoint!r} output: {e}'

        return response
