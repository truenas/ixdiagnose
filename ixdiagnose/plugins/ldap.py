from ixdiagnose.utils.command import Command
from ixdiagnose.utils.formatter import remove_keys
from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import CommandMetric, FileMetric, MiddlewareClientMetric


class LDAP(Plugin):
    name = 'ldap'
    metrics = [
        CommandMetric(
            'kerberos', [
                Command(['klist'], 'Kerberos Tickets', serializeable=False),
                Command(['klist', '-ket'], 'Kerberos keytab system', serializeable=False),
            ]
        ),
        FileMetric('nsswitch', '/etc/nsswitch.conf', extension='.conf'),
        FileMetric('krb5', '/etc/krb5.conf', extension='.conf'),
        FileMetric('ldap', '/etc/openldap/ldap.conf', extension='.conf'),
        FileMetric('nslcd', '/etc/nslcd.conf', extension='.conf'),
        MiddlewareClientMetric(
            'ldap_config', [
                MiddlewareCommand('ldap.config', format_output=remove_keys(['bindpw'])),
                MiddlewareCommand('ldap.get_samba_domains', result_key='samba_domains'),
                MiddlewareCommand('ldap.get_root_DSE', result_key='root_dse'),
            ]
        ),
    ]
