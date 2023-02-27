from ixdiagnose.utils.command import Command
from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import CommandMetric, FileMetric, MiddlewareClientMetric


class Network(Plugin):
    name = 'network'
    metrics = [
        CommandMetric(
            'routing', [
                Command(['ip', '-j', 'route', 'show', 'default'], 'default_route'),
                Command(['ip', '-j', 'route', 'show', 'table', 'all'], 'routing_tables'),
                Command(['ip', '-j', 'rule', 'list'], 'ip_rules'),
            ]
        ),
        CommandMetric(
            'protocol_stats', [Command(['netstat', '-p', '-s'], 'Statistics of All protocols', serializeable=False)],
        ),
        CommandMetric('interface_statistics', [Command(['ip', '-j', '-s', 'addr'], 'Interface Statistics')]),
        CommandMetric(
            'ipset_ipvs_rules', [
                Command(['ipvsadm', '-L'], 'IPVS Rules', serializeable=False),
                Command(['ipset', '--list'], 'IPSET Rules', serializeable=False),
                Command(['netstat', '-nrW'], 'Routing table (netstat)', serializeable=False),
            ]
        ),
        CommandMetric('nft_rules', [Command(['nft', '-j', '-a', 'list', 'ruleset'], 'NFTables rulesets')]),
        CommandMetric('arp', [Command(['arp', '-an'], 'ARP Entries', serializeable=False)]),
        CommandMetric('socket_stats', [Command(['ss', '-nipea'], 'Socket Statistics', serializeable=False)]),
        FileMetric('hosts', '/etc/hosts'),
        FileMetric('resolvers', '/etc/resolv.conf'),
        MiddlewareClientMetric(
            'middleware_config', [
                MiddlewareCommand('network.configuration.config'),
                MiddlewareCommand('interface.query'),
                MiddlewareCommand('route.system_routes'),
            ]
        ),
    ]
