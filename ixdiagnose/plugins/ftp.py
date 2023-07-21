from ixdiagnose.utils.command import Command
from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import CommandMetric, FileMetric, MiddlewareClientMetric


class FTP(Plugin):
    name = 'ftp'
    metrics = [
        CommandMetric('services_status', [
            Command(
                ['systemctl', 'status', 'proftpd'], 'FTP Service Status', serializable=False,
                safe_returncodes=[0, 3],
            ),
        ]),
        FileMetric('ftpusers', '/etc/ftpusers'),
        FileMetric('proftpd.conf', '/etc/proftpd/proftpd.conf'),
        MiddlewareClientMetric('ftp_config', [
            MiddlewareCommand('ftp.config'),
        ])
    ]
