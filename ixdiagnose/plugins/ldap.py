from ixdiagnose.utils.command import Command
from ixdiagnose.utils.formatter import Json
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
        FileMetric('nsswitch_conf', '/etc/nsswitch.conf'),
        FileMetric('krb5_conf', '/etc/krb5.conf'),
        FileMetric('openldap_ldap_conf', '/etc/openldap/ldap.conf'),
        FileMetric('nslcd.conf', '/etc/nslcd.conf'),
        MiddlewareClientMetric(
            'ldap_config', [
                MiddlewareCommand('ldap.config', format_output=Json(['bindpw']).remove),
                MiddlewareCommand('ldap.get_samba_domains', result_key='samba_domains'),
                MiddlewareCommand('ldap.get_root_DSE', result_key='root_dse'),
            ]
        ),
    ]
