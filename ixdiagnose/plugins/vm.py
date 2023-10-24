from collections import defaultdict
from ixdiagnose.utils.formatter import remove_keys
from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import FileMetric, MiddlewareClientMetric, PythonMetric
from .prerequisites import VMPrerequisite


def get_iommu_groups(client, context):
    pci_devices = client.call('vm.device.passthrough_device_choices')
    iommu_groups = defaultdict(list)
    for pci_id, data in pci_devices.items():
        group_no = data['iommu_group']['number'] if data['iommu_group'] else None
        iommu_groups[group_no if group_no is not None else 'UNDEFINED'].append(pci_id)
    return iommu_groups


class VM(Plugin):
    name = 'vm'
    metrics = [
        FileMetric('haproxy', '/etc/haproxy/haproxy.cfg', extension='.cfg', prerequisites=[VMPrerequisite()]),
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
