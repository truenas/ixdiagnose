from ixdiagnose.utils.command import Command
from ixdiagnose.utils.formatter import remove_keys
from ixdiagnose.utils.middleware import AdminMiddlewareCommand, MiddlewareCommand

from .base import Plugin
from .metrics import CommandMetric, MiddlewareClientMetric


class System(Plugin):
    name = 'system'
    metrics = [
        CommandMetric('time_info', [
            Command(['date'], 'System Date', serializable=False),
            Command(['uptime'], 'System Uptime', serializable=False),
            Command(['chronyc', '-n', 'sources'], 'Current time sources', serializable=False),
            Command(['chronyc', '-n', 'sourcestats'], 'Drift rate and offset estimation for each source',
                    serializable=False),
            Command(['chronyc', '-n', 'tracking'], 'System clock performance', serializable=False),
            Command(['chronyc', 'ntpdata'], 'Last valid measurement for each source', serializable=False),
        ]),
        CommandMetric('dmesg', [Command(['dmesg'], 'Dmesg', serializable=False)]),
        CommandMetric('processes', [Command(['ps', '-auxwwf'], 'All running processes', serializable=False)]),
        CommandMetric('mount_info', [
            Command(['swapon', '-s'], 'Swap Usage Summary', serializable=False),
            Command(['mount'], 'System Mount Paths', serializable=False),
            Command(['df', '-T', '-h'], 'Filesystem Resource Usage', serializable=False),
            Command(['findmnt', '-o', 'TARGET,SOURCE,FSTYPE,OPTIONS'], 'Mount tree', serializable=False),
        ]),
        CommandMetric('memory', [
            Command(['vmstat'], 'Virtual Memory Statistics', serializable=False),
        ]),
        CommandMetric('top', [
            Command(['top', '-SHbi', '-d1', '-n2'], 'System Processes/Threads Top', serializable=False),
        ]),
        CommandMetric('kernel_modules', [Command(['lsmod'], 'List of Kernel Modules', serializable=False)]),
        MiddlewareClientMetric('coredump', [AdminMiddlewareCommand('system.coredumps')]),
        MiddlewareClientMetric('general_settings', [
            MiddlewareCommand(
                'system.general.config', format_output=remove_keys([
                    'birthday', 'ui_certificate.privatekey', 'ui_certificate.issuer.privatekey',
                    'ui_certificate.signedby.privatekey',
                ])
            )
        ]),
        MiddlewareClientMetric('advanced_settings', [
            MiddlewareCommand('system.advanced.config', format_output=remove_keys(['sed_user', 'sed_passwd'])),
        ]),
        MiddlewareClientMetric('alerts', [MiddlewareCommand('alert.list')]),
        MiddlewareClientMetric('alerts_sources_stats', [AdminMiddlewareCommand('alert.sources_stats')]),
        MiddlewareClientMetric('middleware_thread_stacks', [AdminMiddlewareCommand('core.threads_stacks')]),
        MiddlewareClientMetric(
            'system_global_id', [MiddlewareCommand('system.global.id', result_key='System Global ID')],
        ),
        MiddlewareClientMetric('system_info', [
            AdminMiddlewareCommand('system.is_enterprise', result_key='Enterprise System'),
            AdminMiddlewareCommand('system.license', result_key='System License'),
            MiddlewareCommand('system.info', result_key='system_info'),
        ]),
        MiddlewareClientMetric('system_dataset', [MiddlewareCommand('systemdataset.config')]),
        MiddlewareClientMetric('system_security', [MiddlewareCommand('system.security.config')]),
    ]
