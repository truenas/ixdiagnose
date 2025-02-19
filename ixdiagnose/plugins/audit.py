from ixdiagnose.utils.command import Command
from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import CommandMetric, FileMetric, MiddlewareClientMetric


class Audit(Plugin):
    name = 'audit'
    metrics = [
        MiddlewareClientMetric(
            'audit_configuration', [
                MiddlewareCommand('audit.config'),
            ],
        ),
        MiddlewareClientMetric(
            'recent_audited_method_calls', [
                MiddlewareCommand('audit.query', [{
                    'services': ['MIDDLEWARE'],
                    'query-filters': [['event', '=', 'METHOD_CALL']],
                    'query-options': {
                        'select': [
                            'audit_id',
                            'message_timestamp',
                            'service_data.origin',
                            'service_data.credentials',
                            'event_data',
                            'success'
                        ],
                        'order_by': ['-message_timestamp']
                    }
                }]),
            ],
        ),
        CommandMetric(
            # This generates a file that is collected in the associated FileMetric.
            'truenas_verify_data', [
                Command(
                    ['shasum', '-a', '256', '/conf/rootfs.mtree'], 'sha256 rootfs.mtree', serializable=False
                ),
                Command(
                    ['truenas_verify'], 'Result from truenas_verify', serializable=False,
                    safe_returncodes=[],  # With no safe_returncodes we can silently run the command
                ),
            ],
        ),
        # The log depends on the truenas_verify command.
        FileMetric('truenas_verify', '/var/log/audit/truenas_verify.log', extension='.log'),
    ]
