from ixdiagnose.utils.formatter import remove_keys
from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import MiddlewareClientMetric


class CloudBackup(Plugin):
    name = 'cloud_backup'
    metrics = [
        MiddlewareClientMetric(
            'cloud_backup', [
                MiddlewareCommand('cloud_backup.query', format_output=remove_keys([
                    'credentials.attributes', 'password',
                ])),
            ]
        ),
    ]
