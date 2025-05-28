import inspect

from ixdiagnose.exceptions import CallError
from ixdiagnose.plugins.prerequisites import Prerequisite
from ixdiagnose.utils.formatter import dumps
from ixdiagnose.utils.middleware import MiddlewareClient
from typing import Any, Callable, Optional, Tuple, TypeVar

from .base import Metric


_Context = TypeVar('_Context')


class PythonMetric(Metric):

    def __init__(
        self, name: str, callback: Callable[[MiddlewareClient, _Context], Any], context: _Context = None,
        description: Optional[str] = None, prerequisites: Optional[list[Prerequisite]] = None,
        serializable: bool = True,
    ):
        super().__init__(name, prerequisites)

        self.callback: Callable = callback
        self.context: Any = context
        self.description: str = description or ''
        self.middleware_client: Optional[MiddlewareClient] = None
        self.serializable: bool = serializable

        if not callable(self.callback):
            raise CallError('Callback must be a callable')
        else:
            if len(inspect.signature(self.callback).parameters) != 2:
                raise CallError(
                    'Only 2 argument must be specified for callback with first being middleware client and '
                    'second being any context specified for the callback'
                )

    @property
    def output_file_extension(self) -> str:
        return '.json' if self.serializable else '.txt'

    def initialize_context(self) -> None:
        self.middleware_client = self.execution_context['middleware_client']

    def execute_impl(self) -> Tuple[Any, str]:
        report = {'error': None if self.middleware_client else 'Failed to initialize middleware client'}
        output = None
        if report['error'] is None:
            try:
                output = self.callback(self.middleware_client, self.context)
            except Exception as e:
                report['error'] = f'Failed to execute defined callback: {e!r}'

        return report, output or '' if isinstance(output, str) or output is None else dumps(output)
