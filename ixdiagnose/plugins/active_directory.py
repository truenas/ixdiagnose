from ixdiagnose.utils.command import Command
from ixdiagnose.utils.formatter import remove_keys
from ixdiagnose.utils.middleware import MiddlewareCommand
from typing import Optional

from .base import Plugin
from .metrics import CommandMetric, MiddlewareClientMetric
from .prerequisites import ActiveDirectoryStatePrerequisite


def ad_domain_name() -> Optional[str]:
    return (MiddlewareCommand('activedirectory.config').execute().output or {}).get('domainname')


class ActiveDirectory(Plugin):
    name = 'active_directory'
    metrics = [
        CommandMetric(
            'ad_info', [
                Command(['wbinfo', '-t'], 'Active directory trust secret', serializable=False),
                Command(['wbinfo', '-P'], 'Active directory NETLOGON connection.', serializable=False),
                Command(['wbinfo', '-m ', '--verbose'], 'Active directory trusted domains.', serializable=False),
                Command(['wbinfo', '--all-domains'], 'Active directory of all domains.', serializable=False),
                Command(['wbinfo', '--own-domain'], 'Active directory own domains', serializable=False),
                Command(['wbinfo', '--online-status'], 'Active directory online status.', serializable=False),
                Command(['wbinfo -u'], 'Active directory Users', serializable=False, max_lines=50),
                Command(['wbinfo -g'], 'Active directory Groups.', serializable=False, max_lines=50),
                Command(
                    'wbinfo --domain-info="$(wbinfo --own-domain)"', 'Active directory domain information.',
                    serializable=False,
                ),
                Command(
                    'wbinfo --dc-info="$(wbinfo --own-domain)"', 'Active Directory DC info.',
                    serializable=False,
                ),
                Command(
                    ['wbinfo', f'--dsgetdcname={ad_domain_name()}'], 'Active Directory DC name.', serializable=False
                ),
            ], prerequisites=[ActiveDirectoryStatePrerequisite()],
        ),
        CommandMetric(
            'ad_join_status', [
                Command(
                    ['net', '-d', 5, '-k', 'ads', 'testjoin'], 'Active Directory Join Status.', serializable=False
                ),
            ], prerequisites=[ActiveDirectoryStatePrerequisite()],
        ),
        MiddlewareClientMetric(
            'ad_config', [MiddlewareCommand('activedirectory.config', format_output=remove_keys(['bindpw']))],
        ),
        MiddlewareClientMetric(
            'domain_info', [MiddlewareCommand('activedirectory.domain_info')],
            prerequisites=[ActiveDirectoryStatePrerequisite()],
        ),
        MiddlewareClientMetric(
            'kerberos_principal_choices', [MiddlewareCommand('kerberos.keytab.kerberos_principal_choices')],
        ),
        MiddlewareClientMetric(
            'machine_account_status', [
                MiddlewareCommand('activedirectory.machine_account_status'),
            ], prerequisites=[ActiveDirectoryStatePrerequisite()]
        ),
        MiddlewareClientMetric(
            'lookup_dc', [
                MiddlewareCommand('activedirectory.lookup_dc'),
            ], prerequisites=[ActiveDirectoryStatePrerequisite()]
        ),
        MiddlewareClientMetric(
            'spn_list', [
                MiddlewareCommand('activedirectory.lookup_dc'),
            ], prerequisites=[ActiveDirectoryStatePrerequisite()]
        ),
        MiddlewareClientMetric('idmap', [MiddlewareCommand('idmap.query')]),
    ]
