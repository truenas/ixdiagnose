from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import MiddlewareClientMetric


class TruenasConnect(Plugin):
    name = 'truenas_connect'
    metrics = [
        MiddlewareClientMetric('config', [MiddlewareCommand('tn_connect.config')]),
    ]
