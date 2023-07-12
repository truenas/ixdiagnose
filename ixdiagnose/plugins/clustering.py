from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import FileMetric, MiddlewareClientMetric
from .prerequisites import ServiceRunningPrerequisite


class Clustering(Plugin):
    name = 'clustering'
    metrics = [
        FileMetric('nodes', '/etc/ctdb/nodes'),
        FileMetric('gluster_workdir_dataset', '/data/.glusterd_workdir_dataset'),
        FileMetric('glusterd', '/var/db/system/glusterd/glusterd.info', extension='.info'),
        FileMetric('glusterd', '/etc/glusterfs/glusterd.vol', extension='.vol'),
        MiddlewareClientMetric(
            'ctdb_info', [
                MiddlewareCommand('ctdb.general.pnn'),
                MiddlewareCommand('ctdb.general.recovery_master'),
                MiddlewareCommand('ctdb.general.status'),
                MiddlewareCommand('ctdb.private.ips.query'),
                MiddlewareCommand('ctdb.public.ips.query'),
                MiddlewareCommand('ctdb.general.listnodes'),
                MiddlewareCommand('ctdb.root_dir.config'),
            ], prerequisites=[ServiceRunningPrerequisite('glusterd')],
        ),
        MiddlewareClientMetric(
            'glusterd_info', [
                MiddlewareCommand('gluster.peer.query'),
                MiddlewareCommand('gluster.volume.query'),
            ], prerequisites=[ServiceRunningPrerequisite('glusterd')],
        ),
        MiddlewareClientMetric(
            'clustered_services', [
                MiddlewareCommand('ctdb.services.get'),
            ], prerequisites=[ServiceRunningPrerequisite('glusterd')],
        ),
    ]
