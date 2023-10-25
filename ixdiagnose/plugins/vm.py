from collections import defaultdict
from ixdiagnose.utils.formatter import remove_keys
from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import MiddlewareClientMetric, PythonMetric
from .prerequisites import VMPrerequisite


def passthrough_choices(client, context):
    data = {
        'usb_passthrough_choices': client.call('vm.device.usb_passthrough_choices'),
        'passthrough_device_choices': client.call('vm.device.passthrough_device_choices'),
        'iommu_groups': defaultdict(list),
    }
    for pci_id, data in data['passthrough_device_choices'].items():
        group_no = data['iommu_group']['number'] if data['iommu_group'] else None
        data['iommu_groups'][group_no if group_no is not None else 'UNDEFINED'].append(pci_id)

    return data


class VM(Plugin):
    name = 'vm'
    metrics = [
        MiddlewareClientMetric(
            'gpu', [MiddlewareCommand('device.get_gpus', result_key='gpus')],
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
        PythonMetric('passthrough_choices',  passthrough_choices, prerequisites=[VMPrerequisite()]),
    ]
