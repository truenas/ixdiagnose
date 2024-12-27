from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import MiddlewareClientMetric


class SystemVendor(Plugin):
    name = 'system_vendor'
    metrics = [
        MiddlewareClientMetric('is_vendored', [MiddlewareCommand('system.vendor.is_vendored')]),
        MiddlewareClientMetric('vendor_name', [MiddlewareCommand('system.vendor.name')]),
    ]
