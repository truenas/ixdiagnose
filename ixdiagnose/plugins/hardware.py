from ixdiagnose.utils.command import Command
from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import CommandMetric, FileMetric, MiddlewareClientMetric


class Hardware(Plugin):
    name = 'hardware'
    metrics = [
        CommandMetric(
            'dmidecode', [
                Command(['dmidecode'], 'Dmidecode', serializeable=False),
            ],
        ),
        CommandMetric(
            'pci', [
                Command(['lspci', '-vvvD'], 'List of PCI Devices', serializeable=False),
            ],
        ),
        CommandMetric(
            'sensors', [
                Command(['sensors', '-j'], 'List of available sensors'),
            ],
        ),
        FileMetric('usb_devices', '/sys/kernel/debug/usb/devices'),
        MiddlewareClientMetric('disks', [MiddlewareCommand('device.get_disks')]),
        MiddlewareClientMetric('enclosures', [MiddlewareCommand('enclosure.query')]),
    ]
    raw_metrics = [
        CommandMetric(
            'block_devices', [
                Command([
                    'lsblk', '-o',
                    'NAME,ALIGNMENT,MIN-IO,OPT-IO,PHY-SEC,LOG-SEC,ROTA,SCHED,RQ-SIZE,RA,WSAME,HCTL,PATH',
                ], 'List of Block Devices', serializeable=False),
            ],
        ),
        CommandMetric('cpu', [Command(['lscpu'], 'CPU Information', serializeable=False)]),
    ]
    serializable_metrics = [
        CommandMetric(
            'block_devices', [
                Command([
                    'lsblk', '-J', '-o',
                    'NAME,ALIGNMENT,MIN-IO,OPT-IO,PHY-SEC,LOG-SEC,ROTA,SCHED,RQ-SIZE,RA,WSAME,HCTL,PATH',
                ], 'List of Block Devices'),
            ],
        ),
        CommandMetric('cpu', [Command(['lscpu', '-J'], 'CPU Information')]),
    ]
