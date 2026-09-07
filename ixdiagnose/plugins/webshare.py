from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import MiddlewareClientMetric


class Webshare(Plugin):
    name = "webshare"
    metrics = [
        MiddlewareClientMetric(
            "webshare_config",
            [
                MiddlewareCommand("webshare.config"),
                MiddlewareCommand("sharing.webshare.query"),
            ],
        ),
    ]
