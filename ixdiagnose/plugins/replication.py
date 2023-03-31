from ixdiagnose.utils.formatter import remove_keys
from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import MiddlewareClientMetric


class Replication(Plugin):
    name = 'replication'
    metrics = [
        MiddlewareClientMetric(
            'replication', [
                MiddlewareCommand('replication.query', format_output=remove_keys(['ssh_credentials'])),
            ]
        ),
        MiddlewareClientMetric(
            'snapshot_tasks', [
                MiddlewareCommand('pool.snapshottask.query', result_key='snapshot_tasks'),
            ]
        ),
    ]
