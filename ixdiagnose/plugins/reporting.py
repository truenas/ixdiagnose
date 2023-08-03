from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import MiddlewareClientMetric
from .prerequisites import ServiceRunningPrerequisite


class Reporting(Plugin):
    name = 'reporting'
    metrics = [
        MiddlewareClientMetric(
            'graphs', [MiddlewareCommand(
                'reporting.netdata_graphs', result_key='all_graphs',
            )], prerequisites=[ServiceRunningPrerequisite('netdata')],
        ),
    ]
