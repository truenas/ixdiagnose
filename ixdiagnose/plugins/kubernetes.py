from ixdiagnose.utils.command import Command
from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import CommandMetric, MiddlewareClientMetric
from .prerequisites import ServiceRunningPrerequisite


KUBERNETES_RESOURCES = [
    'pods', 'services', 'deployments', 'job', 'daemonsets', 'statefulsets', 'storageclasses',
    'persistentvolumeclaims', 'persistentvolumes', 'namespaces', 'nodes',
]


class Kubernetes(Plugin):
    name = 'kubernetes'
    metrics = [
        CommandMetric('k3s_logs', [
            Command('journalctl -u k3s | tail -n 1000', 'K3s logs', shell=True, serializeable=False),
        ]),
        MiddlewareClientMetric('config', [MiddlewareCommand('kubernetes.config')]),
    ] + [
        CommandMetric(resource, [
            Command(['k3s', 'kubectl', 'get', resource, '-o', 'json'], f'Describe {resource.capitalize()!r} resources')
        ], prerequisites=[ServiceRunningPrerequisite('k3s')])
        for resource in KUBERNETES_RESOURCES
    ]
