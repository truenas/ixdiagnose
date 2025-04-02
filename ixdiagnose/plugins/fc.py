from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import MiddlewareClientMetric
from .prerequisites import FibreChannelPrerequisite


class FibreChannel(Plugin):
    name = 'fc'
    metrics = [
        MiddlewareClientMetric(
            'fc_hosts', [
                MiddlewareCommand('fc.fc_hosts'),
            ],
            prerequisites=[FibreChannelPrerequisite()],
        ),
        MiddlewareClientMetric(
            'fc_host_pairs', [
                MiddlewareCommand('fc.fc_host.query'),
            ],
            prerequisites=[FibreChannelPrerequisite()],
        ),
        MiddlewareClientMetric(
            'fcport', [
                MiddlewareCommand('fcport.query'),
            ],
            prerequisites=[FibreChannelPrerequisite()],
        ),
    ]
