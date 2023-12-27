from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import MiddlewareClientMetric


class RBAC(Plugin):
    name = 'rbac'
    metrics = [
        MiddlewareClientMetric(
            'privilege_information', [
                MiddlewareCommand('privilege.query'),
                MiddlewareCommand('privilege.always_has_root_password_enabled'),
            ],
        ),
        MiddlewareClientMetric(
            'authenticated_sessions', [
                MiddlewareCommand('auth.sessions'),
            ],
        ),
        MiddlewareClientMetric(
            'privileged_local_users', [
                MiddlewareCommand('user.query', [[['roles', '!=', []]], {'select': ['username', 'uid', 'roles']}]),
            ],
        ),
    ]
