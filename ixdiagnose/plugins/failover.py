from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import MiddlewareClientMetric


class Failover(Plugin):
    name = 'failover'
    metrics = [
        MiddlewareClientMetric(
            'failover_config', [
                MiddlewareCommand('failover.config'),
            ]
        ),
    ]
