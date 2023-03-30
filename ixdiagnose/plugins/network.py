from ixdiagnose.utils.command import Command
from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import CommandMetric, FileMetric, MiddlewareClientMetric


class Network(Plugin):
    name = 'network'
    metrics = [
        CommandMetric(
            'protocol_stats', [Command(['netstat', '-p', '-s'], 'Statistics of All protocols', serializable=False)],
        ),
        CommandMetric(
            'ipset_ipvs_rules', [
                Command(['ipvsadm', '-L'], 'IPVS Rules', serializable=False),
                Command(['ipset', '--list'], 'IPSET Rules', serializable=False),
                Command(['netstat', '-nrW'], 'Routing table (netstat)', serializable=False),
            ]
        ),
        CommandMetric('arp', [Command(['arp', '-an'], 'ARP Entries', serializable=False)]),
        CommandMetric('socket_stats', [Command(['ss', '-nipea'], 'Socket Statistics', serializable=False)]),
        FileMetric('hosts', '/etc/hosts'),
        FileMetric('resolv', '/etc/resolv.conf', extension='.conf'),
        MiddlewareClientMetric(
            'middleware_config', [
                MiddlewareCommand('network.configuration.config'),
                MiddlewareCommand('interface.query'),
                MiddlewareCommand('route.system_routes'),
            ]
        ),
    ]
    raw_metrics = [
        CommandMetric(
            'routing', [
                Command(['ip', 'route', 'show', 'default'], 'default_route', serializable=False),
                Command(['ip', 'route', 'show', 'table', 'all'], 'routing_tables', serializable=False),
                Command(['ip', 'rule', 'list'], 'ip_rules', serializable=False),
            ]
        ),
        CommandMetric('interface_statistics', [
            Command(['ip', '-s', 'addr'], 'Interface Statistics', serializable=False)
        ]),
        CommandMetric('nft_rules', [
            Command(['nft', '-a', 'list', 'ruleset'], 'NFTables rulesets', serializable=False)
        ]),
    ]
    serializable_metrics = [
        CommandMetric(
            'routing', [
                Command(['ip', '-j', 'route', 'show', 'default'], 'default_route'),
                Command(['ip', '-j', 'route', 'show', 'table', 'all'], 'routing_tables'),
                Command(['ip', '-j', 'rule', 'list'], 'ip_rules'),
            ]
        ),
        CommandMetric('interface_statistics', [Command(['ip', '-j', '-s', 'addr'], 'Interface Statistics')]),
        CommandMetric('nft_rules', [Command(['nft', '-j', '-a', 'list', 'ruleset'], 'NFTables rulesets')]),
    ]
