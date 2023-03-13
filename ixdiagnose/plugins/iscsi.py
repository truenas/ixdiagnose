from ixdiagnose.utils.command import Command
from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import CommandMetric, FileMetric, MiddlewareClientMetric
from .prerequisites import ServiceRunningPrerequisite


class ISCSI(Plugin):
    name = 'iscsi'
    metrics = [
        MiddlewareClientMetric('iscsi_config', [
            MiddlewareCommand('iscsi.global.config', result_key='global_config'),
            MiddlewareCommand('iscsi.target.query', result_key='targets'),
            MiddlewareCommand('iscsi.extent.query', result_key='extents'),
        ]),
        CommandMetric(
            'iscsi_state', [
                Command(['scstadmin', '--list_device'], 'Lists SCST devices', serializeable=False),
                Command(['scstadmin', '-list_handler'], 'Lists SCST device handlers', serializeable=False),
                Command(['scstadmin', '-list_driver'], 'Lists SCST drivers', serializeable=False),
                Command(['scstadmin', '-list_target', '-driver', 'iscsi'], 'Lists SCST targets', serializeable=False),
                Command(['scstadmin', '-list_sessions'], 'Lists SCST active sessions', serializeable=False),
                Command(['scstadmin', '-list_scst_attr'], 'Lists SCST core attributes', serializeable=False),
            ], prerequisites=[ServiceRunningPrerequisite('scst')],
        ),
        FileMetric('scst', '/etc/scst.conf', extension='.conf'),
    ]
    raw_metrics = [
        CommandMetric(
            'service_status', [
                Command(
                    ['systemctl', 'status', 'scst'], 'SCST Service Status', serializeable=False, safe_returncodes=[0, 3]
                ),
            ],
        ),
    ]
    serializable_metrics = [
        MiddlewareClientMetric(
            'service_status', [
                MiddlewareCommand(
                    'service.query', [[['service', '=', 'iscsitarget']], {'get': True}], result_key='service'
                ),
            ]
        )
    ]
