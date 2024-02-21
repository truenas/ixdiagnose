from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import MiddlewareClientMetric
from .prerequisites import FailoverPrerequisite


class Failover(Plugin):
    name = 'failover'
    metrics = [
        MiddlewareClientMetric(
            'failover_config', [
                MiddlewareCommand('failover.config'),
            ],
            prerequisites=[FailoverPrerequisite()],
        ),
        MiddlewareClientMetric(
            'failover_event_config', [
                MiddlewareCommand('failover.events.generate_failover_data'),
            ],
            prerequisites=[FailoverPrerequisite()],
        ),
        MiddlewareClientMetric(
            'failover_status', [
                MiddlewareCommand('failover.status'),
            ],
            prerequisites=[FailoverPrerequisite()],
        ),
        MiddlewareClientMetric(
            'failover_disabled_reasons', [
                MiddlewareCommand('failover.disabled.reasons'),
            ],
            prerequisites=[FailoverPrerequisite()],
        ),
    ]
