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
                    'privatekey', 'host_dsa_key', 'host_dsa_key_pub', 'host_dsa_key_cert_pub', 'host_ecdsa_key',
                    'host_ecdsa_key_pub', 'host_ecdsa_key_cert_pub', 'host_ed25519_key', 'host_ed25519_key_pub',
                    'host_ed25519_key_cert_pub', 'host_key', 'host_key_pub', 'host_rsa_key', 'host_rsa_key_pub',
                    'host_rsa_key_cert_pub',
                ])
            )]
        ),
        FileMetric('sshd', '/etc/pam.d/sshd'),
        FileMetric('sshd_config', '/etc/ssh/sshd_config'),
    ]
