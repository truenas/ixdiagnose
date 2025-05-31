from ixdiagnose.utils.formatter import redact_keys
from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import MiddlewareClientMetric, FileMetric


class SSH(Plugin):
    name = 'ssh'
    metrics = [
        MiddlewareClientMetric(
            'ssh_config',
            [MiddlewareCommand(
                'ssh.config',
                format_output=redact_keys(include=[
                    'id', 'bindiface', 'tcpport', 'password_login_groups', 'passwordauth', 'kerberosauth', 'tcpfwd',
                    'compression', 'sftp_log_level', 'sftp_log_facility', 'weak_ciphers', 'options',
                ])
            )]
        ),
        FileMetric('sshd', '/etc/pam.d/sshd'),
        FileMetric('sshd_config', '/etc/ssh/sshd_config'),
    ]
