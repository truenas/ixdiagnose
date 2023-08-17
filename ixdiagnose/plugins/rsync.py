from ixdiagnose.utils.formatter import remove_keys
from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import MiddlewareClientMetric


class Rsync(Plugin):
    name = 'rsync'
    metrics = [
        MiddlewareClientMetric(
            'rsync', [
                MiddlewareCommand('rsynctask.query', format_output=remove_keys(['ssh_credentials'])),
            ]
        ),
    ]
