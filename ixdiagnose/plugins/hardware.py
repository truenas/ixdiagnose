import os
import re
import typing

from ixdiagnose.utils.command import Command
from ixdiagnose.utils.formatter import remove_keys
from ixdiagnose.utils.middleware import MiddlewareClient, MiddlewareCommand
from ixdiagnose.utils.run import run

from .base import Plugin
from .metrics import CommandMetric, FileMetric, MiddlewareClientMetric, PythonMetric
from .prerequisites import JBOFPrerequisite


def nvdimm_info(client: MiddlewareClient, context: typing.Any) -> str:
    nmem = re.compile(r'^nmem\d+$')
    output = ''
    with os.scandir('/dev/') as sdir:
        for i in filter(lambda x: nmem.match(x.name), sdir):
            output += f"{'=' * 20} {i.path} {'=' * 20}\n"
            cp = run(f'/usr/local/sbin/ixnvdimm {i.path}', check=False)
            if cp.returncode:
                output += f'Failed to retrieve nvdimm info: {cp.stderr}\n\n'
            else:
                output += f'{cp.stdout}\n\n'
    return output


class Hardware(Plugin):
    name = 'hardware'
    metrics = [
        CommandMetric(
            'dmidecode', [
                Command(['dmidecode'], 'Dmidecode', serializable=False),
            ],
        ),
        CommandMetric(
            "jbof_view", [
                Command(["jbof_view.py", "--both"], "jbof_view.py --both", serializable=False),
            ],
            prerequisites=[JBOFPrerequisite()],
        ),
        CommandMetric(
            'pci', [
                Command(['lspci', '-vvvD'], 'List of PCI Devices', serializable=False),
            ],
        ),
        CommandMetric(
            'sensors', [
                Command(['sensors', '-j'], 'List of available sensors'),
            ],
        ),
        FileMetric('usb_devices', '/sys/kernel/debug/usb/devices'),
        MiddlewareClientMetric('disks', [MiddlewareCommand('device.get_disks')]),
        MiddlewareClientMetric('disks_config', [MiddlewareCommand('disk.query')]),
        MiddlewareClientMetric('enclosures', [MiddlewareCommand('enclosure2.query')]),
        MiddlewareClientMetric('virtualization_variant', [MiddlewareCommand('hardware.virtualization.variant')]),
        MiddlewareClientMetric('is_virtualized', [MiddlewareCommand('hardware.virtualization.is_virtualized')]),
        MiddlewareClientMetric('jbof_config', [MiddlewareCommand('jbof.query',
                                                                 format_output=remove_keys(['mgmt_password']))]),
        PythonMetric('nvdimm_info', nvdimm_info, serializable=False),
    ]
    raw_metrics = [
        CommandMetric(
            'block_devices', [
                Command([
                    'lsblk', '-o',
                    'NAME,ALIGNMENT,MIN-IO,OPT-IO,PHY-SEC,LOG-SEC,ROTA,SCHED,RQ-SIZE,RA,WSAME,HCTL,SIZE,PARTTYPENAME,'
                    'PATH',
                ], 'List of Block Devices', serializable=False),
            ],
        ),
        CommandMetric('cpu', [Command(['lscpu'], 'CPU Information', serializable=False)]),
    ]
    serializable_metrics = [
        CommandMetric(
            'block_devices', [
                Command([
                    'lsblk', '-J', '-o',
                    'NAME,ALIGNMENT,MIN-IO,OPT-IO,PHY-SEC,LOG-SEC,ROTA,SCHED,RQ-SIZE,RA,WSAME,HCTL,SIZE,PARTTYPENAME,'
                    'PATH',
                ], 'List of Block Devices'),
            ],
        ),
        CommandMetric('cpu', [Command(['lscpu', '-J'], 'CPU Information')]),
    ]
