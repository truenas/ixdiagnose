from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import MiddlewareClientMetric
from .prerequisites import ServiceRunningPrerequisite


class Apps(Plugin):
    name = 'apps'
    metrics = [
        MiddlewareClientMetric(
            'apps', [
                MiddlewareCommand('app.query')
            ],
            prerequisites=[ServiceRunningPrerequisite('docker')],
        ),
        MiddlewareClientMetric(
            'docker_config', [
                MiddlewareCommand('docker.config'),
            ],
        ),
        MiddlewareClientMetric(
            'docker_status', [
                MiddlewareCommand('docker.status'),
            ],
        ),
    ]
