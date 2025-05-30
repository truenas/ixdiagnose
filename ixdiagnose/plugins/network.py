import subprocess
from typing import Any

from ixdiagnose.utils.command import Command
from ixdiagnose.utils.formatter import dumps
from ixdiagnose.utils.middleware import MiddlewareClient, MiddlewareCommand

from .base import Plugin
from .metrics import CommandMetric, FileMetric, MiddlewareClientMetric, PythonMetric


def link_choices(client: MiddlewareClient, context: Any) -> str:
    summary = {}
    configured_interfaces = client.call('interface.get_configured_interfaces')
    for link in client.call('rdma.get_link_choices', True):
        summary[link['netdev']] = link | {'configured_interface': link['netdev'] in configured_interfaces}

    return dumps(summary)


def ethtool_callback(client: MiddlewareClient, context: Any) -> str:
    """Run `ethtool -m interface` for every interface, including RDMA."""
    summary = {}
    iface_names = {iface['name'] for iface in client.call('interface.query', [], {'select': ['name']})}
    rdma_names = {rdma['netdev'] for rdma in client.call('rdma.get_link_choices', True)}

    for iname in iface_names | rdma_names:
        ethtool_output = subprocess.run(['ethtool', '-m', iname], capture_output=True, text=True).stdout

        iname_stats = {}
        for line in ethtool_output.splitlines():
            field_name, value = [field.strip() for field in line.split(':', 1)]
            iname_stats[field_name] = value

        summary[iname] = iname_stats

    return dumps(summary)


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
        MiddlewareClientMetric(
            'rdma_config', [
                MiddlewareCommand('rdma.capable_protocols', result_key='capable_protocols'),
                MiddlewareCommand('rdma.get_card_choices', result_key='card_choices'),
                MiddlewareCommand('rdma.interface.query', result_key='interfaces'),
            ]
        ),
        PythonMetric('rdma_link_choices', link_choices),
        PythonMetric('ethtool', ethtool_callback),
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
        CommandMetric('interface_statistics', [Command(['ip', '-j', '-s', '-s', 'addr'], 'Interface Statistics')]),
        CommandMetric('nft_rules', [Command(['nft', '-j', '-a', 'list', 'ruleset'], 'NFTables rulesets')]),
    ]
