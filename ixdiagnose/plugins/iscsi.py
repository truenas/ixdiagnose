import re

from ixdiagnose.utils.command import Command
from ixdiagnose.utils.formatter import remove_keys
from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import CommandMetric, MiddlewareClientMetric, RedactedFileMetric
from .prerequisites import ServiceRunningPrerequisite

SENSITIVE_LINE = re.compile(r'^(\s*)(IncomingUser "|OutgoingUser ")(\S*) (\S*)"$')


def redact_chap_passwords(line):
    return SENSITIVE_LINE.sub(r'\1\2\3 **REDACTED**"', line)


class ISCSI(Plugin):
    name = 'iscsi'
    metrics = [
        MiddlewareClientMetric('iscsi_config', [
            MiddlewareCommand('iscsi.global.config', result_key='global_config'),
            MiddlewareCommand('iscsi.target.query', result_key='targets'),
            MiddlewareCommand('iscsi.extent.query', result_key='extents'),
            MiddlewareCommand('iscsi.targetextent.query', result_key='targetextents'),
            MiddlewareCommand('iscsi.portal.query', result_key='portals'),
            MiddlewareCommand('iscsi.initiator.query', result_key='initiators'),
            MiddlewareCommand('iscsi.auth.query', result_key='auths',
                              format_output=remove_keys(['secret', 'peersecret'])),
        ]),
        CommandMetric(
            'iscsi_state', [
                Command(['scstadmin', '--list_device'], 'Lists SCST devices', serializable=False),
                Command(['scstadmin', '-list_handler'], 'Lists SCST device handlers', serializable=False),
                Command(['scstadmin', '-list_driver'], 'Lists SCST drivers', serializable=False),
                Command(['scstadmin', '-list_target', '-driver', 'iscsi'], 'Lists SCST targets', serializable=False),
                Command(['scstadmin', '-list_sessions'], 'Lists SCST active sessions', serializable=False),
                Command(['scstadmin', '-list_scst_attr'], 'Lists SCST core attributes', serializable=False),
            ], prerequisites=[ServiceRunningPrerequisite('scst')],
        ),
        RedactedFileMetric('scst', '/etc/scst.conf', extension='.conf', redact_callback=redact_chap_passwords),
    ]
    raw_metrics = [
        CommandMetric(
            'service_status', [
                Command(
                    ['systemctl', 'status', 'scst'], 'SCST Service Status', serializable=False, safe_returncodes=[0, 3]
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
