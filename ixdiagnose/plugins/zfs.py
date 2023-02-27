from ixdiagnose.utils.command import Command
from ixdiagnose.utils.middleware import MiddlewareClient, MiddlewareCommand

from .base import Plugin
from .metrics import CommandMetric, MiddlewareClientMetric, PythonMetric


class ZFS(Plugin):
    name = 'zfs'
    metrics = [
        CommandMetric(
            'pool_status', [
                Command(['zpool', 'list', '-v'], 'ZFS Pool(s)', serializeable=False),
                Command(['zpool', 'status', '-v'], 'ZFS Pool(s) Status', serializeable=False),
            ]
        ),
        CommandMetric('pool_history', [Command(['zpool', 'history'], 'ZFS Pool(s) History', serializeable=False)]),
        MiddlewareClientMetric(
            'pool_config', [
                MiddlewareCommand('pool.scrub.query', result_key='scrub_tasks'),
                MiddlewareCommand('zfs.pool.query', result_key='pool_config'),
            ]
        ),
        MiddlewareClientMetric(
            'replication', [
                MiddlewareCommand('replication.query'),
            ]
        ),
        MiddlewareClientMetric(
            'snapshots', [
                MiddlewareCommand('pool.snapshottask.query', result_key='snapshot_tasks'),
                MiddlewareCommand('zfs.snapshot.query', [[], {'extra': {
                    'props': ['name', 'used', 'available', 'referenced', 'mountpoint', 'freenas:state'],
                    # TODO: Add changes to zfs snapshot service to allow props filtering
                }}]),
            ]
        ),
    ]
