from ixdiagnose.utils.command import Command
from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import CommandMetric, MiddlewareClientMetric


def redact_instances(instances: list) -> list:
    for instance in instances:
        instance.pop('vnc_password', None)
        raw = instance['raw']

        if 'config' in raw:
            raw['config'].pop('user.ix_vnc_config', None)

        if 'expanded_config' in raw:
            raw['expanded_config'].pop('user.ix_vnc_config', None)

    return instances


class Virt(Plugin):
    name = 'virt'
    metrics = [
        CommandMetric('incus_logs', [
            Command('journalctl -u incus | tail -n 1000', 'Incus logs', serializable=False),
        ]),
        MiddlewareClientMetric('virt_global_config', [MiddlewareCommand('virt.global.config')]),
        MiddlewareClientMetric(
            'virt_instances', [
                MiddlewareCommand(
                    'virt.instance.query',
                    api_payload=[[], {'extra': {'raw': True}}],
                    format_output=redact_instances
                )
            ]
        ),
        MiddlewareClientMetric('virt_volumes', [MiddlewareCommand('virt.volume.query')]),
        CommandMetric('incus_commands', [
            Command('incus profile list', 'Incus profiles', serializable=False),
            Command('incus project list', 'Incus projects', serializable=False),
            Command('incus network list', 'Incus networks', serializable=False),
            Command('incus storage list', 'Incus storage', serializable=False),
        ]),
    ]
