from ixdiagnose.utils.command import Command

from .base import Plugin
from .metrics import CommandMetric, FileMetric


class Sysctl(Plugin):
    name = 'sysctl'
    metrics = [
        CommandMetric('kernel_params', [Command(['sysctl', '-a'], 'All kernel parameters', serializeable=False)]),
        FileMetric('sysctl_config', '/etc/sysctl.conf'),
    ]