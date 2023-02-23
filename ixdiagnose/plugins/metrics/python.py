import inspect

from ixdiagnose.exceptions import CallError
from ixdiagnose.plugins.prerequisites import Prerequisite
from ixdiagnose.utils.formatter import dumps
from ixdiagnose.utils.middleware import get_middleware_client
from typing import Any, Callable, List, Tuple

from .base import Metric


class PythonMetric(Metric):

    def __init__(
        self, name: str, callback: Callable, context: Any = None, description: str = None,
        prerequisites: List[Prerequisite] = None,
    ):
        super().__init__(name, prerequisites)
        self.callback: Callable = callback
        self.context: Any = context
        self.description: str = description
        if not callable(self.context):
            raise CallError('Callback must be a callable')
        else:
            if len(inspect.signature(self.callback).parameters) == 2:
                raise CallError(
                    'Only 2 argument must be specified for callback with first being middleware client and '
                    'second being any context specified for the callback'
                )

    def execute_impl(self) -> Tuple[Any, str]:
        report = {'error': None}
        output = None
        try:
            with get_middleware_client() as client:
                output = self.callback(client, self.callback)
        except Exception as e:
            report['error'] = f'Failed to execute defined callback: {e!r}'

        return report, report or '' if isinstance(output, str) or output is None else dumps(output)
