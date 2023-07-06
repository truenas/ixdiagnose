from ixdiagnose.utils.command import Command
from ixdiagnose.utils.formatter import remove_keys
from ixdiagnose.utils.middleware import MiddlewareCommand

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
        ]),
        CommandMetric('memory', [
            Command(['top', '-SHbi', '-d1', '-n2'], 'System Processes/Threads Top', serializable=False),
            Command(['vmstat'], 'Virtual Memory Statistics', serializable=False),
        ]),
        CommandMetric('kernel_modules', [Command(['lsmod'], 'List of Kernel Modules', serializable=False)]),
        MiddlewareClientMetric('coredump', [MiddlewareCommand('system.coredumps')]),
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
        MiddlewareClientMetric('alerts_sources_stats', [MiddlewareCommand('alert.sources_stats')]),
        MiddlewareClientMetric('middleware_tasks', [MiddlewareCommand('core.get_tasks')]),
        MiddlewareClientMetric('middleware_thread_stacks', [MiddlewareCommand('core.threads_stacks')]),
        MiddlewareClientMetric('jobs', [MiddlewareCommand('core.get_jobs', [[], {'extra': {'raw_result': False}}])]),
        MiddlewareClientMetric('system_info', [
            MiddlewareCommand('system.is_enterprise', result_key='Enterprise System'),
            MiddlewareCommand(
                'truecommand.connected', result_key='Truecommand Status',
                format_output=remove_keys(['truecommand_ip', 'truecommand_url'])
            ),
            MiddlewareCommand('system.license', result_key='System License'),
            MiddlewareCommand('system.gather_update_failed', result_key='Failed Updates'),
        ]),
        MiddlewareClientMetric('websocket_messages', [MiddlewareCommand('core.get_websocket_messages')]),
    ]
