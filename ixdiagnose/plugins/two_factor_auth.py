from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import MiddlewareClientMetric


class TwoFactorAuth(Plugin):
    name = '2fa'
    metrics = [
        MiddlewareClientMetric('config', [MiddlewareCommand('auth.twofactor.config')]),
        MiddlewareClientMetric('users', [MiddlewareCommand('user.query', api_payload=[
            [['twofactor_auth_configured', '=', True]],
            {'select': ['username', 'local']}
        ])])
    ]
