from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import MiddlewareClientMetric
from .prerequisites import VMPrerequisite


class VM(Plugin):
    name = 'vm'
    metrics = [
        MiddlewareClientMetric(
            'gpu', [MiddlewareCommand('device.get_gpus', result_key='gpus')],
            prerequisites=[VMPrerequisite()]
        ),
        MiddlewareClientMetric(
            'passthrough_choices', [
                MiddlewareCommand('vm.device.usb_passthrough_choices', result_key='usb_passthrough_choices'),
                MiddlewareCommand('vm.device.passthrough_device_choices', result_key='passthrough_device_choices'),
            ],
            prerequisites=[VMPrerequisite()]
        ),
        MiddlewareClientMetric(
            'vms', [MiddlewareCommand('vm.query', result_key='vms')],
            prerequisites=[VMPrerequisite()]
        ),
        MiddlewareClientMetric(
            'vm_devices', [MiddlewareCommand('vm.device.query', result_key='devices')],
            prerequisites=[VMPrerequisite()]
        ),
    ]
