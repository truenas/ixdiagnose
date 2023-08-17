from ixdiagnose.utils.formatter import remove_keys
from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import MiddlewareClientMetric


class CloudSync(Plugin):
    name = 'cloud_sync'
    metrics = [
        MiddlewareClientMetric(
            'cloud_sync', [
                MiddlewareCommand('cloudsync.query', format_output=remove_keys([
                    'credentials.attributes', 'encryption_password', 'encryption_salt',
                ])),
            ]
        ),
    ]
