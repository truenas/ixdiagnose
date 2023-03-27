import contextlib
import pytest
import os

from subprocess import CompletedProcess
from ixdiagnose.plugins.zfs import zfs_getacl_impl, resource_output, kstat_output


def get_assets_dir_path() -> str:
    current_file_path = os.path.abspath(__file__)
    assets_parent_dir = os.path.dirname(current_file_path)
    return os.path.join(assets_parent_dir, 'assets')


@contextlib.contextmanager
def get_assets_file(filename):
    with open(os.path.join(get_assets_dir_path(), filename), 'r') as file:
        yield file


@pytest.mark.parametrize('dataset_name,props_dict,args,return_code,stdout,stderr,should_work', [
    (
        'crave/ix-applications',
        {'mounted': 'yes', 'mountpoint': '/mnt/crave/ix-applications', 'acltype': 'posix'},
        ('getfacl', '/mnt/crave/ix-applications'),
        0,
        '# file: mnt/crave/ix-applications\n# owner: root\n# group: root\nuser::rwx\ngroup::r-x\nother::r-x',
        '',
        True
    ),
    (
        'boot-pool/ROOT/23.10-MASTER-20230308-062905',
        {'mounted': 'yes', 'mountpoint': 'legacy', 'acltype': 'off'},
        ('getfacl', 'legacy'),
        1,
        '',
        'getfacl: legacy: No such file or directory\n',
        False
    ),
    (
        'boot-pool/ROOT/23.10-MASTER-20230308-062905',
        {'mounted': 'yes', 'mountpoint': 'legacy', 'acltype': 'off'},
        ('getfacl', 'legacy'),
        1,
        '',
        '',
        False
    )
])
def test_zfs_getacl_impl(mocker, dataset_name, props_dict, args, return_code, stdout, stderr, should_work):
    with get_assets_file('acl_output.txt') as f:
        mocker.patch('ixdiagnose.plugins.zfs.run', return_value=CompletedProcess(args, return_code, stdout, stderr))
        if should_work:
            assert zfs_getacl_impl(dataset_name, props_dict) == f.read()
        else:
            assert zfs_getacl_impl(dataset_name, props_dict) != f.read()


@pytest.mark.parametrize('resource_type,args,returncode,file_name,stderr,return_zfs_getacl,should_work', [
    (
        'zpool',
        ('zpool', 'get', 'all'),
        0,
        'input_resource_output1.txt',
        '',
        None,
        False
    ),
    (
        'zfs',
        ('zfs', 'get', 'all'),
        0,
        'input_resource_output2.txt',
        '',
        [
            '\nMountpoint ACL: crave\n'
            '# file: mnt/crave\n'
            '# owner: root\n'
            '# group: root\n'
            'user::rwx\n'
            'group::r-x\n'
            'other::r-x\n\n',
            '\nMountpoint ACL: rootd\n'
            '# file: mnt/rootd\n'
            '# owner: root\n'
            '# group: root\n'
            'user::rwx\n'
            'group::r-x\n'
            'other::r-x\n\n',
        ],
        True
    ),
    (
        'zfs',
        ('zfs', 'get', 'all'),
        0,
        'input_resource_output3.txt',
        '',
        [
            '\nMountpoint ACL: crave\n'
            '# file: mnt/crave\n'
            '# owner: root\n'
            '# group: root\n'
            'user::rwx\n'
            'group::r-x\n'
            'other::r-x\n\n',
            '\nMountpoint ACL: rootd\n'
            '# file: mnt/rootd\n'
            '# owner: root\n'
            '# group: root\n'
            'user::rwx\n'
            'group::r-x\n'
            'other::r-x\n\n',
        ],
        False
    )
])
def test_resource_output(mocker, resource_type, args, returncode, file_name, stderr, return_zfs_getacl, should_work):
    with get_assets_file('get_zpool_output.txt') as f:
        with get_assets_file(file_name) as input_file:
            mock_client = mocker.Mock()
            mocker.patch('ixdiagnose.plugins.zfs.run',
                         return_value=CompletedProcess(args, returncode, input_file.read(), stderr))
            mocker.patch('ixdiagnose.plugins.zfs.zfs_getacl', side_effect=return_zfs_getacl)
            if should_work:
                assert resource_output(mock_client, resource_type) == f.read()
            else:
                assert resource_output(mock_client, resource_type) != f.read()


@pytest.mark.parametrize('pools,file_name,should_work', [
    (
        [
            {
                'name': 'rootd',
                'id': 'rootd',
                'guid': '6009907550966676357',
                'hostname': 'truenas',
                'status': 'ONLINE',
                'healthy': True,
                'warning': False,
            },
        ],
        'input_kstat_output1.txt',
        True
    ),
    (
        [
            {
                'name': 'rootd',
                'id': 'rootd',
                'guid': '6009907550966676357',
                'hostname': 'truenas',
                'status': 'ONLINE',
                'healthy': True,
                'warning': False,
            },
        ],
        'input_kstat_output2.txt',
        False
    ),
    (
        [
            {
                'name': 'rootd',
                'id': 'rootd',
                'guid': '6009907550966676357',
                'hostname': 'truenas',
                'status': 'ONLINE',
                'healthy': True,
                'warning': False,
            },
        ],
        'input_kstat_output3.txt',
        False
    )
])
def test_kstat_output(mocker, pools, file_name, should_work):
    with get_assets_file('kstat_output.txt') as f:
        with get_assets_file(file_name) as input_file:
            mock_client = mocker.Mock()
            mocker.patch('builtins.map', return_value=['rootd'])
            mocker.patch(
                'os.path.join', side_effect=[
                    '/proc/spl/kstat/zfs/fletcher_4_bench',
                    '/proc/spl/kstat/zfs/vdev_raidz_bench',
                    '/proc/spl/kstat/zfs/dbgmsg',
                    '/proc/spl/kstat/zfs/root/multihost',
                    '/proc/spl/kstat/zfs/rootd/state',
                    '/proc/spl/kstat/zfs/rootd/txgs'
                ],
            )
            mocker.patch('os.path.exists', side_effect=[False, False, False, False, True, True])
            mock_open = mocker.patch('builtins.open')
            mock_open.return_value.__enter__.side_effect = [
                mocker.mock_open(read_data='ONLINE').return_value,
                mocker.mock_open(read_data=input_file.read()).return_value
            ]
            output = f.read()
            if should_work:
                assert kstat_output(mock_client, None) == output
            else:
                assert kstat_output(mock_client, None) != output
