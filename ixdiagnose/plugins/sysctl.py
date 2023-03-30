from ixdiagnose.utils.command import Command

from .base import Plugin
from .metrics import CommandMetric, FileMetric


class Sysctl(Plugin):
    name = 'sysctl'
    metrics = [
        CommandMetric('kernel_params', [Command(['sysctl', '-a'], 'All kernel parameters', serializable=False)]),
        FileMetric('sysctl', '/etc/sysctl.conf', extension='.conf'),
    ]
