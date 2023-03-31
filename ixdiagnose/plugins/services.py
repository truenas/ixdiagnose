from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import MiddlewareClientMetric


class Services(Plugin):
    name = 'services'
    metrics = [
        MiddlewareClientMetric('services', [MiddlewareCommand('service.query', result_key='services_status')]),
    ]
