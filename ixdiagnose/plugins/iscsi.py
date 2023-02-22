from ixdiagnose.utils.command import Command
from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import CommandMetric, FileMetric, MiddlewareClientMetric


class ISCSI(Plugin):
    name = 'iscsi'
    metrics = [
        CommandMetric(
            'service_status', [
                Command(
                    ['systemctl', 'status', 'scst'], 'SCST Service Status', serializeable=False, safe_returncodes=[0, 3]
                ),
            ],
        ),
        MiddlewareClientMetric('iscsi_config', [
            MiddlewareCommand(
                'service.query', [[['service', '=', 'iscsitarget']], {'get': True}], result_key='service_config',
            ),
            MiddlewareCommand('iscsi.global.config', result_key='ISCSI global configuration'),
        ]),
        CommandMetric(
            'iscsi_state', [
                Command(['scstadmin', '--list_device'], 'Lists SCST devices', serializeable=False),
                Command(['scstadmin', '-list_handler'], 'Lists SCST device handlers', serializeable=False),
                Command(['scstadmin', '-list_driver'], 'Lists SCST drivers', serializeable=False),
                Command(['scstadmin', '-list_target', '-driver', 'iscsi'], 'Lists SCST targets', serializeable=False),
                Command(['scstadmin', '-list_sessions'], 'Lists SCST active sessions', serializeable=False),
                Command(['scstadmin', '-list_scst_attr'], 'Lists SCST core attributes', serializeable=False),
            ],
        ),
        FileMetric('shadow.conf', '/etc/ctl.conf.shadow'),
        FileMetric('scst_conf', '/etc/scst.conf'),
    ]
