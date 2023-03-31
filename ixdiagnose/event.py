import inspect
import logging

from ixdiagnose.exceptions import CallError
from typing import Callable, List


logger = logging.getLogger(__name__)


class EventCallback:

    CALLBACKS: List[Callable] = []

    def register(self, callback: Callable):
        if not callable(callback):
            raise CallError('Callback must be a callable')

        if len(inspect.signature(callback).parameters) != 2:
            raise CallError(
                'Only 2 argument must be specified for callback with first being progress percentage and '
                'second being percentage text'
            )

        self.CALLBACKS.append(callback)

    def clear(self):
        self.CALLBACKS = []


event_callbacks = EventCallback()


def send_event(progress: int, text: str):
    for callback in event_callbacks.CALLBACKS:
        try:
            callback(progress, text)
        except Exception:
            logger.debug('Failed to execute callback', exc_info=True)
