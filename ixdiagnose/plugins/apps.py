from ixdiagnose.utils.command import Command
from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import CommandMetric, MiddlewareClientMetric
from .prerequisites import ServiceRunningPrerequisite


class Apps(Plugin):
    name = 'apps'
    metrics = [
        CommandMetric('docker_logs', [
            Command('journalctl -u docker | tail -n 1000', 'Docker logs', serializable=False),
        ]),
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
