from ixdiagnose.utils.command import Command
from ixdiagnose.utils.formatter import remove_keys
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
            Command('journalctl -u k3s | tail -n 1000', 'K3s logs', serializable=False),
        ]),
        CommandMetric(
            'resources_state', [
                Command([
                    'k3s', 'kubectl', 'get', 'pods,svc,daemonsets,deployments,statefulset,sc,pvc,ns,job', '-A',
                    '-o', 'wide',
                ], 'Kubernetes Resources', serializable=False)
            ], prerequisites=[ServiceRunningPrerequisite('k3s')],
        ),
        MiddlewareClientMetric('backups', [MiddlewareCommand('kubernetes.list_backups')]),
        MiddlewareClientMetric('config', [MiddlewareCommand('kubernetes.config')]),
        MiddlewareClientMetric('catalogs', [MiddlewareCommand('catalog.query')]),
        MiddlewareClientMetric(
            'chart_releases', [
                MiddlewareCommand('chart.release.query', format_output=remove_keys(['config']))
            ], prerequisites=[ServiceRunningPrerequisite('k3s')],
        ),
    ]
    raw_metrics = [
        CommandMetric(resource, [
            Command(
                ['k3s', 'kubectl', 'describe', resource, '-A'],
                f'Describe {resource.capitalize()!r} resources', serializable=False,
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
