from ixdiagnose.utils.command import Command
from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import CommandMetric, MiddlewareClientMetric


class Apps(Plugin):
    name = 'apps'
    metrics = [
        CommandMetric('docker_logs', [
            Command('journalctl -u docker | tail -n 1000', 'Docker logs', serializable=False),
        ]),
        MiddlewareClientMetric('app_images', [MiddlewareCommand('app.image.query')]),
        MiddlewareClientMetric('app_dockerhub_limit', [MiddlewareCommand('app.image.dockerhub_rate_limit')]),
        MiddlewareClientMetric('apps', [MiddlewareCommand('app.query')]),
        MiddlewareClientMetric('apps_gpu_choices', [MiddlewareCommand('app.gpu_choices')]),
        MiddlewareClientMetric('apps_used_ports', [MiddlewareCommand('app.used_ports')]),
        MiddlewareClientMetric('catalog', [MiddlewareCommand('catalog.config')]),
        MiddlewareClientMetric('catalog_trains', [MiddlewareCommand('catalog.trains')]),
        MiddlewareClientMetric('docker_config', [MiddlewareCommand('docker.config')]),
        MiddlewareClientMetric('docker_status', [MiddlewareCommand('docker.status')]),
    ]
