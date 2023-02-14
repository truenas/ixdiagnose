from ixdiagnose.utils.command import Cmd

from .base import CmdMetric, Plugin


class Hardware(Plugin):
    name = 'hardware'
    metrics = [
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
    ]
