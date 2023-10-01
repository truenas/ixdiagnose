from ixdiagnose.utils.command import Command
from ixdiagnose.utils.middleware import MiddlewareClient, MiddlewareCommand
from typing import Any

from .base import Plugin
from .metrics import CommandMetric, FileMetric, MiddlewareClientMetric, PythonMetric
from .prerequisites import ServiceRunningPrerequisite


def nfs_client_count_by_type(client: MiddlewareClient, context: Any) -> str:
    num_nfs3 = client.call('nfs.get_nfs3_clients')
    nfs4_clnt_info = client.call('nfs.get_nfs4_clients')
    nfs4_ver_info = [x["info"]["minor version"] for x in nfs4_clnt_info]

    title = 'Number of NFS clients'
    sep = '-----------------------------'
    output = f'{sep}\n{title:^29}\n{sep}\n\n'
    output += f'{"NFSv3":^10}{"NFSv4.0":^10}{"NFSv4.1":^10}{"NFSv4.2":^10}\n'
    output += f'{"-----":^10}{"-------":^10}{"-------":^10}{"-------":^10}\n'
    output += f'{len(num_nfs3):^10}'
    output += f'{nfs4_ver_info.count(0):^10}{nfs4_ver_info.count(1):^10}{nfs4_ver_info.count(2):^10}\n'

    return output


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
        PythonMetric('nfs-client-counts', nfs_client_count_by_type, serializable=False),
    ]
