from ixdiagnose.utils.command import Command
from ixdiagnose.utils.formatter import Json
from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import CommandMetric, MiddlewareClientMetric


class System(Plugin):
    name = 'system'
    metrics = [
        CommandMetric('time_info', [
            Command(['date'], 'System Date', serializeable=False),
            Command(['uptime'], 'System Uptime', serializeable=False),
            Command(['ntpq', '-c', 'rv'], 'NTP System Variables', serializeable=False),
            Command(['ntpq', '-pwn'], 'List of NTP peers known to the system', serializeable=False),
        ]),
        CommandMetric('dmesg', [Command(['dmesg'], 'Dmesg', serializeable=False)]),
        CommandMetric('processes', [Command(['ps', '-auxwwf'], 'All running processes', serializeable=False)]),
        CommandMetric('mount_info', [
            Command(['swapon', '-s'], 'Swap Usage Summary', serializeable=False),
            Command(['mount'], 'System Mount Paths', serializeable=False),
            Command(['df', '-T', '-h'], 'Filesystem Resource Usage', serializeable=False),
        ]),
        CommandMetric('memory', [
            Command(['top', '-SHbi', '-d1', '-n2'], 'System Processes/Threads Top', serializeable=False),
            Command(['vmstat'], 'Virtual Memory Statistics', serializeable=False),
        ]),
        CommandMetric('kernel_modules', [Command(['lsmod'], 'List of Kernel Modules', serializeable=False)]),
        MiddlewareClientMetric('coredump', [MiddlewareCommand('system.coredumps')]),
        MiddlewareClientMetric('general_settings', [
            MiddlewareCommand(
                'system.general.config', format_output=Json([
                    'birthday', 'ui_certificate.privatekey', 'ui_certificate.issuer.privatekey',
                    'ui_certificate.signedby.privatekey',
                ]).remove
            )
        ]),
        MiddlewareClientMetric('advanced_settings', [
            MiddlewareCommand('system.advanced.config', format_output=Json(['sed_user', 'sed_passwd']).remove),
        ]),
        MiddlewareClientMetric('alerts', [MiddlewareCommand('alert.list')]),
        MiddlewareClientMetric('middleware_tasks', [MiddlewareCommand('core.get_tasks')]),
        MiddlewareClientMetric('middleware_thread_stacks', [MiddlewareCommand('core.threads_stacks')]),
        MiddlewareClientMetric('jobs', [MiddlewareCommand('core.get_jobs', [[], {'extra': {'raw_result': False}}])]),
        MiddlewareClientMetric('system_info', [
            MiddlewareCommand('system.is_enterprise', result_key='Enterprise System'),
            MiddlewareCommand(
                'truecommand.connected', result_key='Truecommand Status',
                format_output=Json(['truecommand_ip', 'truecommand_url']).remove
            ),
            MiddlewareCommand('system.license', result_key='System License'),
            MiddlewareCommand('system.gather_update_failed', result_key='Failed Updates'),
        ]),
        MiddlewareClientMetric('websocket_messages', [MiddlewareCommand('core.get_websocket_messages')]),
    ]