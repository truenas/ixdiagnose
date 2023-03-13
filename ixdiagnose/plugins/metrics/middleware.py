import time

from ixdiagnose.plugins.prerequisites.base import Prerequisite
from ixdiagnose.utils.formatter import dumps
from ixdiagnose.utils.middleware import MiddlewareClient, MiddlewareCommand
from typing import Any, List, Optional, Tuple

from .base import Metric


class MiddlewareClientMetric(Metric):

    methods_metadata: Optional[dict] = None

    @classmethod
    def get_methods_metadata(cls):
        if cls.methods_metadata is None:
            cls.methods_metadata = MiddlewareCommand('core.get_methods').execute().output or {}
        return cls.methods_metadata

    def __init__(
        self, name: str, middleware_commands: List[MiddlewareCommand], prerequisites: List[Prerequisite] = None
    ):
        super().__init__(name, prerequisites)
        self.middleware_client: Optional[MiddlewareClient] = None
        self.middleware_commands = middleware_commands

    def format_output(self, context: list) -> str:
        if len(context) == 1:
            return dumps(context[0])
        else:
            return dumps({entry['key']: entry['output'] for entry in context})

    def initialize_context(self) -> None:
        self.middleware_client = self.execution_context['middleware_client']

    def execute_impl(self) -> Tuple[Any, str]:
        context = []
        metric_report = []
        for middleware_command in self.middleware_commands:
            start_time = time.time()
            response = middleware_command.execute(self.middleware_client)
            metric_report.append({
                'endpoint': middleware_command.endpoint,
                'error': response.error,
                'execution_time': time.time() - start_time,
                'description': self.get_methods_metadata().get(middleware_command.endpoint, {}).get('description'),
            })
            if response.error:
                continue

            context.append({
                'key': response.result_key,
                'output': response.output,
            })

        return metric_report, self.format_output(context) if context else ''
