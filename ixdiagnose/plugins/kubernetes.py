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
        CommandMetric(
            'resources_state', [
                Command([
                    'k3s', 'kubectl', 'get', 'pods,svc,daemonsets,deployments,statefulset,sc,pvc,ns,job', '-A',
                    '-o', 'wide',
                ], 'Kubernetes Resources', serializeable=False)
            ], prerequisites=[ServiceRunningPrerequisite('k3s')],
        ),
        MiddlewareClientMetric('config', [MiddlewareCommand('kubernetes.config')]),
    ]
    raw_metrics = [
        CommandMetric(resource, [
            Command(
                ['k3s', 'kubectl', 'describe', resource, '-A'],
                f'Describe {resource.capitalize()!r} resources', serializeable=False,
            )
        ], prerequisites=[ServiceRunningPrerequisite('k3s')])
        for resource in KUBERNETES_RESOURCES
    ]
    serializable_metrics = [
        CommandMetric(resource, [
            Command(['k3s', 'kubectl', 'get', resource, '-o', 'json'], f'Describe {resource.capitalize()!r} resources')
        ], prerequisites=[ServiceRunningPrerequisite('k3s')])
        for resource in KUBERNETES_RESOURCES
    ]
