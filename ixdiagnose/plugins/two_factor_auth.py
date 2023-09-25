from typing import Any

from ixdiagnose.utils.formatter import dumps
from ixdiagnose.utils.middleware import MiddlewareClient, MiddlewareCommand

from .base import Plugin
from .metrics import MiddlewareClientMetric, PythonMetric


def twofactor_details_of_users(client: MiddlewareClient, context: Any) -> str:
    summary = client.call('auth.twofactor.get_users_config')
    for user in summary:
        user['secret_configured'] = bool(user.pop('secret_hex'))

    return dumps(summary)


class TwoFactorAuth(Plugin):
    name = '2fa'
    metrics = [
        MiddlewareClientMetric('config', [MiddlewareCommand('auth.twofactor.config')]),
        PythonMetric('users', twofactor_details_of_users),
    ]
