from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import MiddlewareClientMetric


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
    ]
