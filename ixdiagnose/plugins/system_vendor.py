from ixdiagnose.utils.middleware import AdminMiddlewareCommand

from .base import Plugin
from .metrics import MiddlewareClientMetric


class SystemVendor(Plugin):
    name = 'system_vendor'
    metrics = [
        MiddlewareClientMetric('is_vendored', [AdminMiddlewareCommand('system.vendor.is_vendored')]),
        MiddlewareClientMetric('vendor_name', [AdminMiddlewareCommand('system.vendor.name')]),
    ]
