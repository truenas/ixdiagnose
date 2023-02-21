import json

from middlewared.client import Client  # FIXME: this is not good
from typing import Any, Callable, List, Optional, Tuple

from .base import Metric


class MiddlewareClientMetric(Metric):

    methods_metadata = {}

    @classmethod
    def get_methods_metadata(cls):
        if not cls.methods_metadata:
            with Client() as client:
                cls.methods_metadata = client.call('core.get_methods')
        return cls.methods_metadata

    def __init__(
        self, name: str, endpoint: str, api_payload: Optional[List] = None, format_output: Optional[Callable] = None
    ):
        super().__init__(name)
        self.endpoint: str = endpoint
        self.overridden_format_output: Optional[Callable] = format_output
        self.payload: List = api_payload or []

    def format_output(self, output: Any) -> Any:
        return self.overridden_format_output(output) if self.overridden_format_output else output

    def execute_impl(self) -> Tuple[Any, str]:
        report = {
            'error': None, 'description': self.methods_metadata.get(self.endpoint),
        }
        try:
            with Client() as client:
                output = client.call(self.endpoint, *self.payload)
        except Exception as e:
            output = None
            report['error'] = f'Failed to retrieve data from {self.endpoint!r}: {e}'

        try:
            output = self.format_output(output)
        except Exception as e:
            output = None
            report['error'] = f'Failed to clean {self.endpoint!r} output: {e}'

        return report, '' if report['error'] else json.dumps(output, indent=4)
