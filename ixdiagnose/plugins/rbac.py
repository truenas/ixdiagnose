from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import MiddlewareClientMetric


class RBAC(Plugin):
    name = 'rbac'
    metrics = [
        MiddlewareClientMetric(
            'privilege_information', [
                MiddlewareCommand('privilege.query'),
            ],
        ),
    ]
