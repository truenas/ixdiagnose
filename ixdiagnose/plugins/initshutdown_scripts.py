from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import MiddlewareClientMetric


class InitShutDownScripts(Plugin):
    name = 'initshutdown_scripts'
    metrics = [
        MiddlewareClientMetric('initshutdown', [MiddlewareCommand('initshutdownscript.query')]),
    ]
