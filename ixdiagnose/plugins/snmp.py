
from ixdiagnose.utils.formatter import remove_keys
from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import MiddlewareClientMetric, DirectoryTreeMetric, FileMetric


class SNMP(Plugin):
    name = 'snmp'
    metrics = [
        MiddlewareClientMetric(
            'snmp_config',
            [
                MiddlewareCommand('snmp.config', format_output=remove_keys(['v3_password', 'v3_privpassphrase'])),
            ]
        ),
        FileMetric('snmp', '/etc/snmp/snmp.conf', extension='.conf'),
        FileMetric('snmpd', '/etc/snmp/snmpd.conf', extension='.conf'),
        DirectoryTreeMetric('custom_snmpd', '/etc/snmp/snmpd.conf.d'),
        DirectoryTreeMetric('mibs', '/etc/snmp-mibs-downloader'),
    ]
