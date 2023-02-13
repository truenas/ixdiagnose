from ixdiagnose.utils.command import Cmd

from .base import CmdMetric, Plugin


class Hardware(Plugin):
    name = 'hardware'
    metrics = [
        CmdMetric(
            'CPU Information', [
                Cmd(['lscpu', '-J'], 'CPU Information'),
            ]
        ),
        CmdMetric(
            'Dmidecode', [
                Cmd(['dmidecode'], 'Dmidecode'),
            ],
        ),
    ]
