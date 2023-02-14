from ixdiagnose.utils.command import Cmd

from .base import Plugin
from .metrics_base import CmdMetric, FileMetric


class Hardware(Plugin):
    name = 'hardware'
    metrics = [
        CmdMetric(
            'block_devices', [
                Cmd([
                    'lsblk', '-J', '-o',
                    'NAME,ALIGNMENT,MIN-IO,OPT-IO,PHY-SEC,LOG-SEC,ROTA,SCHED,RQ-SIZE,RA,WSAME,HCTL,PATH',
                ], 'List of PCI Devices'),
            ],
        ),
        CmdMetric(
            'cpu', [
                Cmd(['lscpu', '-J'], 'CPU Information'),
            ]
        ),
        CmdMetric(
            'dmidecode', [
                Cmd(['dmidecode'], 'Dmidecode', serializeable=False),
            ],
        ),
        CmdMetric(
            'pci', [
                Cmd(['lspci', '-vvvD'], 'List of PCI Devices', serializeable=False),
            ],
        ),
        FileMetric('usb_devices', '/sys/kernel/debug/usb/devices'),
    ]
