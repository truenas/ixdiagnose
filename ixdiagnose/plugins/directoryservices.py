from ixdiagnose.utils.command import Command
from ixdiagnose.utils.formatter import remove_keys
from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import CommandMetric, FileMetric, MiddlewareClientMetric
from .prerequisites import ActiveDirectoryStatePrerequisite, DomainJoinedPrerequisite


class DirectoryServices(Plugin):
    name = 'directory_services'
    metrics = [
        MiddlewareClientMetric(
            'base_information', [
                MiddlewareCommand('directoryservices.status'),
                MiddlewareCommand('directoryservices.config', format_output=remove_keys(['credential']))
            ]
        ),
        MiddlewareClientMetric(
            'domain_info', [MiddlewareCommand('directoryservices.domain_info')],
            prerequisites=[DomainJoinedPrerequisite()]
        ),
        CommandMetric(
            'ad_info', [
                Command(['wbinfo', '-t'], 'Active directory trust secret', serializable=False),
                Command(['wbinfo', '-P'], 'Active directory NETLOGON connection.', serializable=False),
                Command(['wbinfo', '-m ', '--verbose'], 'Active directory trusted domains.', serializable=False),
                Command(['wbinfo', '--all-domains'], 'Active directory of all domains.', serializable=False),
                Command(['wbinfo', '--own-domain'], 'Active directory own domains', serializable=False),
                Command(['wbinfo', '--online-status'], 'Active directory online status.', serializable=False),
                Command(['wbinfo', '-u'], 'Active directory Users', serializable=False, max_lines=50),
                Command(['wbinfo', '-g'], 'Active directory Groups.', serializable=False, max_lines=50),
                Command(
                    'wbinfo --domain-info="$(wbinfo --own-domain)"', 'Active directory domain information.',
                    serializable=False,
                ),
                Command(
                    'wbinfo --dc-info="$(wbinfo --own-domain)"', 'Active Directory DC info.',
                    serializable=False,
                ),
            ], prerequisites=[ActiveDirectoryStatePrerequisite()],
        ),
        CommandMetric(
            'ad_join_status', [
                Command(
                    ['net', '-d', '5', '-k', 'ads', 'testjoin'], 'Active Directory Join Status.', serializable=False
                ),
            ], prerequisites=[ActiveDirectoryStatePrerequisite()],
        ),
        MiddlewareClientMetric(
            'kerberos_principal_choices', [MiddlewareCommand('kerberos.keytab.kerberos_principal_choices')],
        ),
        MiddlewareClientMetric(
            'kerberos_configuration', [
                MiddlewareCommand('kerberos.realm.query'),
                MiddlewareCommand('kerberos.config'),
                MiddlewareCommand('kerberos.realm.query', format_output=remove_keys(['file'])),
            ],
        ),
        FileMetric('nsswitch', '/etc/nsswitch.conf', extension='.conf'),
        FileMetric('krb5', '/etc/krb5.conf', extension='.conf'),
        FileMetric('ldap', '/etc/openldap/ldap.conf', extension='.conf'),
        CommandMetric(
            'sssd', [
                Command(
                    ['grep', '-iv', 'ldap_default_authtok', '/etc/sssd/sssd.conf'],
                    'Config file', serializable=False
                )
            ]
        )
    ]
