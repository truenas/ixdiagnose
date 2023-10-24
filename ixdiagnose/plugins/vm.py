from collections import defaultdict
from ixdiagnose.utils.formatter import remove_keys
from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import MiddlewareClientMetric, PythonMetric
from .prerequisites import VMPrerequisite


def get_iommu_groups(client, context):
    pci_devices = client.call('vm.device.passthrough_device_choices')
    iommu_groups = defaultdict(list)
    for pci_id, data in pci_devices.items():
        iommu_groups[data['iommu_group']['number']].append(pci_id)
    return iommu_groups


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
            'vms', [
                MiddlewareCommand(
                    'vm.query', result_key='vms', format_output=remove_keys(['devices.attributes.password'])
                )
            ],
            prerequisites=[VMPrerequisite()]
        ),
        MiddlewareClientMetric(
            'vm_devices', [
                MiddlewareCommand(
                    'vm.device.query', result_key='devices', format_output=remove_keys(['attributes.password'])
                )
            ],
            prerequisites=[VMPrerequisite()]
        ),
        PythonMetric('iommu_group',  get_iommu_groups),
    ]
