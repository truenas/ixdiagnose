from typing import Any

from ixdiagnose.utils.command import Command
from ixdiagnose.utils.formatter import dumps
from ixdiagnose.utils.middleware import MiddlewareClient, MiddlewareCommand
from ixdiagnose.utils.run import run

from .base import Plugin
from .metrics import CommandMetric, MiddlewareClientMetric, PythonMetric


def zfs_getacl(dataset_name: str, props_dict: dict) -> str:
    return f'\n\n{zfs_getacl_impl(dataset_name, props_dict)}\n'


def zfs_getacl_impl(dataset_name: str, props_dict: dict) -> str:
    err_str = f'Failed to retrieve ACL info for {dataset_name!r}: '
    if not all(props_dict.get(k) for k in ('acltype', 'mounted', 'mountpoint')):
        return f'{err_str}unable to retrieve mounted/mountpoint information for {dataset_name!r}'

    if props_dict['mounted'] != 'yes':
        return f'{err_str}dataset is not mounted'

    acl_binary = 'nfs4xdr_getfacl' if props_dict['acltype'] == 'nfsv4' else 'getfacl'
    cp = run([acl_binary, props_dict['mountpoint']], check=False)
    if cp.returncode:
        return f'{err_str}unable to retrieve acl details ({cp.stderr})'

    return f'Mountpoint ACL: {dataset_name}\n{cp.stdout}'


def resource_output(client: MiddlewareClient, resource_type: str) -> str:
    if resource_type == 'zfs':
        cp = run(['zfs', 'get', 'all', '-t', 'filesystem'], check=False)
    else:
        cp = run([resource_type, 'get', 'all'], check=False)
    if cp.returncode:
        return f'Failed to retrieve {resource_type!r} resources: {cp.stderr}'

    prop_list = {'acltype', 'mounted', 'mountpoint'}
    resource_context = resource_name = None
    output = ''
    prop_dict = {}
    output_lines = cp.stdout.splitlines()
    props_header = output_lines[0]
    for index, resource_line in enumerate(filter(bool, map(str.strip, output_lines[1:]))):
        resource_name = resource_line.split()[0].strip()
        if resource_context != resource_name:
            if resource_context is not None and resource_type == 'zfs':
                output += zfs_getacl(resource_context, prop_dict)

            prop_dict = {}
            header_str = f'{resource_type} get all {resource_name}'
            next_line = '\n\n' if index != 0 else ''
            output += f'{next_line}{"=" * (len(header_str) + 5)}\n  {header_str}\n{"=" * (len(header_str) + 5)}\n\n'
            output += f'{props_header}\n'
            resource_context = resource_name

        if resource_type == 'zfs':
            prop = resource_line.split()[1]
            if prop in prop_list:
                prop_dict[prop] = resource_line.split()[2]

        output += f'{resource_line}\n'

    if resource_name is not None and resource_type == 'zfs':
        output += zfs_getacl(resource_name, prop_dict)

    return output


def encryption_summary(client: MiddlewareClient, context: Any) -> str:
    summary = {}
    for pool in client.call('pool.query'):
        summary[pool['name']] = client.call('pool.dataset.encryption_summary', pool['name'], job=True)

    return dumps(summary)


class ZFS(Plugin):
    name = 'zfs'
    metrics = [
        CommandMetric(
            'dataset_list', [
                Command(['zfs', 'list', '-ro', 'space,refer,mountpoint'], 'ZFS Dataset(s)', serializable=False),
            ]
        ),
        CommandMetric(
            'pool_list', [Command(['zpool', 'list', '-v'], 'ZFS Pool(s)', serializable=False)]
        ),
        CommandMetric(
            'pool_status', [Command(['zpool', 'status', '-v'], 'ZFS Pool(s) Status', serializable=False)]
        ),
        CommandMetric(
            'pool_status_guid', [Command(['zpool', 'status', '-g'], 'ZFS Pool(s) Status (with vdev GUIDs)',
                                         serializable=False)]
        ),
        CommandMetric('pool_history', [Command(['zpool', 'history'], 'ZFS Pool(s) History', serializable=False)]),
        CommandMetric('arc_summary', [Command(['arc_summary'], 'ARC Summary', serializable=False)]),
        MiddlewareClientMetric(
            'pool_scrub_tasks', [
                MiddlewareCommand('pool.scrub.query', result_key='scrub_tasks'),
            ]
        ),
        PythonMetric('encryption_summary', encryption_summary),
    ]
    raw_metrics = [
        CommandMetric('snapshot_config', [
            Command(
                ['zfs', 'list', '-t', 'snapshot', '-o', 'name,used,available,referenced,mountpoint,freenas:state'],
                'ZFS Snapshots', serializable=False,
            )
        ]),
        CommandMetric(
            'lsblk', [
                Command(
                    ['lsblk', '-o', 'NAME,FSTYPE,LABEL,UUID,PARTUUID', '-l', '-e', '230'],
                    'lsblk -o NAME,FSTYPE,LABEL,UUID,PARTUUID -l -e 230', serializable=False
                ),
            ]
        ),
        PythonMetric('dataset_config', resource_output, 'zfs', 'ZFS Datasets Configuration', serializable=False),
        PythonMetric('pool_config', resource_output, 'zpool', 'ZFS Pools Configuration', serializable=False),
    ]
    serializable_metrics = [
        CommandMetric(
            'lsblk', [
                Command(
                    ['lsblk', '-o', 'NAME,FSTYPE,LABEL,UUID,PARTUUID', '-l', '-e', '230', '-J'],
                    'lsblk -o NAME,FSTYPE,LABEL,UUID,PARTUUID -l -e 230 -J'
                ),
            ]
        ),
        MiddlewareClientMetric('dataset_config', [MiddlewareCommand('zfs.dataset.query')]),
        MiddlewareClientMetric('pool_config', [MiddlewareCommand('zfs.pool.query')]),
        MiddlewareClientMetric('snapshot_config', [
            MiddlewareCommand('zfs.snapshot.query', [[], {'extra': {
                'props': ['name', 'used', 'available', 'referenced', 'mountpoint', 'freenas:state'],
                # TODO: Add changes to zfs snapshot service to allow props filtering
            }}]),
        ]),
    ]
