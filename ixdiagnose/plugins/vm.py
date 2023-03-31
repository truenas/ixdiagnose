from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import FileMetric, MiddlewareClientMetric


class VM(Plugin):
    name = 'vm'
    metrics = [
        FileMetric('haproxy', '/etc/haproxy/haproxy.cfg', extension='.cfg'),
        MiddlewareClientMetric(
            'gpu', [MiddlewareCommand('device.get_gpus', result_key='gpus')],
        ),
        MiddlewareClientMetric(
            'passthrough_choices', [
                MiddlewareCommand('vm.device.usb_passthrough_choices', result_key='usb_passthrough_choices'),
                MiddlewareCommand('vm.device.passthrough_device_choices', result_key='passthrough_device_choices'),
            ],
        ),
        MiddlewareClientMetric('vms', [MiddlewareCommand('vm.query', result_key='vms')]),
        MiddlewareClientMetric('vm_devices', [MiddlewareCommand('vm.device.query', result_key='devices')]),
    ]
