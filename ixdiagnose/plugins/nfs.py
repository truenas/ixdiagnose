from ixdiagnose.utils.command import Command
from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import CommandMetric, FileMetric, MiddlewareClientMetric
from .prerequisites import ServiceRunningPrerequisite


class NFS(Plugin):
    name = 'nfs'
    metrics = [
        CommandMetric('services_status', [
            Command(
                ['systemctl', 'status', 'nfs-server'], 'NFS Service Status', serializable=False,
                safe_returncodes=[0, 3],
            ),
            Command(
                ['systemctl', 'status', 'rpc-statd'], 'RPC Statd Service Status', serializable=False,
                safe_returncodes=[0, 3],
            ),
            Command(
                ['systemctl', 'status', 'rpc-gssd'], 'RPC Gssd Service Status', serializable=False,
                safe_returncodes=[0, 3],
            ),
            Command(
                ['systemctl', 'status', 'gssproxy'], 'Gssproxy Service Status', serializable=False,
                safe_returncodes=[0, 3],
            ),
        ]),
        CommandMetric(
            'rpcinfo', [
                Command(['rpcinfo', '-p'], 'Status of the RPC Server', serializable=False),
            ], prerequisites=[ServiceRunningPrerequisite('rpc-statd')],
        ),
        FileMetric('nfs-common', '/etc/default/nfs-common'),
        FileMetric('nfs-kernel-server', '/etc/default/nfs-kernel-server'),
        FileMetric('nfs-exports', '/etc/exports'),
        MiddlewareClientMetric('nfs_config', [
            MiddlewareCommand('nfs.config'),
            MiddlewareCommand('sharing.nfs.query'),
        ]),
    ]
