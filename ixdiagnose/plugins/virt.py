from ixdiagnose.utils.command import Command
from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import CommandMetric, MiddlewareClientMetric


class Virt(Plugin):
    name = 'virt'
    metrics = [
        CommandMetric('incus_logs', [
            Command('journalctl -u incus | tail -n 1000', 'Incus logs', serializable=False),
        ]),
        MiddlewareClientMetric('virt_global_config', [MiddlewareCommand('virt.global.config')]),
        MiddlewareClientMetric(
            'virt_instances', [MiddlewareCommand('virt.instance.query', [[], {'extra': {'raw': True}}])]
        ),
        MiddlewareClientMetric('virt_volumes', [MiddlewareCommand('virt.volume.query')]),
        CommandMetric('incus_commands', [
            Command('incus profile list', 'Incus profiles', serializable=False),
            Command('incus project list', 'Incus projects', serializable=False),
            Command('incus network list', 'Incus networks', serializable=False),
            Command('incus storage list', 'Incus storage', serializable=False),
        ]),
    ]
