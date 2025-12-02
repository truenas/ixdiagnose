import contextlib
from dataclasses import dataclass
from typing import Any, Callable, Optional, TypeAlias

from truenas_api_client import Client
from ixdiagnose.config import conf


MiddlewareClient: TypeAlias = Client


@contextlib.contextmanager
def get_middleware_client() -> Client:
    with Client(call_timeout=conf.timeout) as client:
        # Drop privilege set to readonly admin to ensure that API responses with Secret fields are always redacted
        client.call('privilege.become_readonly')
        yield client


@contextlib.contextmanager
def get_admin_middleware_client() -> Client:
    """ This middleware client has the full privilege set of the initiaiting process. Since this tool is typically
    invoked by root, it will have FULL_ADMIN privileges. This is required to call private API methods. """
    with Client(call_timeout=conf.timeout) as client:
        yield client


@dataclass
class MiddlewareResponse:

    result_key: str
    error: Optional[str] = None
    output: Any = None


class MiddlewareCommand:
    def __init__(
        self, endpoint: str, api_payload: Optional[list] = None, format_output: Optional[Callable[[Any], Any]] = None,
        result_key: Optional[str] = None, job: bool = False,
    ):
        """
        :param endpoint: The API method to call.
        :param api_payload: Arguments to pass to `endpoint`.
        :param format_output: Optional function that takes the API method's result and returns it in a new form.
        :param result_key: Defaults to `endpoint` with periods replaced with underscores.
        :param job: `endpoint` is a job.
        """
        self.endpoint = endpoint
        self.overridden_format_output = format_output
        self.payload = api_payload or []
        self.result_key = result_key or self.endpoint.replace('.', '_')
        self.job = job

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


class AdminMiddlewareCommand(MiddlewareCommand):
    """ Execute a middleware command with FULL_ADMIN privileges. This allows calling private endpoints,
    and should be used *very* sparingly since it removes response redaction and can cause sensitive information
    to leak into debug files. """
    def execute(self, unused: Optional[MiddlewareClient] = None) -> MiddlewareResponse:
        with get_admin_middleware_client() as privileged_client:
            return super().execute(privileged_client)
