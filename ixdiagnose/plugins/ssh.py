
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
                format_output=redact_keys([
                    'privatekey', 'host_dsa_key', 'host_ecdsa_key', 'host_ed25519_key', 'host_key', 'host_rsa_key'
                ])
            )]
        ),
        FileMetric('sshd', '/etc/pam.d/sshd'),
        FileMetric('sshd_config', '/etc/ssh/sshd_config'),
    ]
