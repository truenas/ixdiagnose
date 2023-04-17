import pytest
from subprocess import CompletedProcess

from ixdiagnose.plugins.smb import get_smb_shares
from ixdiagnose.test.pytest.unit.utils import get_asset


@pytest.mark.parametrize('middleware_return_values', [
    [
        [
            {
                'id': 3,
                'purpose': 'DEFAULT_SHARE',
                'path': '/mnt/crave/data',
                'path_suffix': '',
                'home': False,
                'name': 'data',
                'comment': '',
                'ro': False,
                'browsable': True,
                'recyclebin': False,
                'guestok': False,
                'hostsallow': [],
                'hostsdeny': [],
                'auxsmbconf': '',
                'aapl_name_mangling': False,
                'abe': False,
                'acl': True,
                'durablehandle': True,
                'streams': True,
                'timemachine': False,
                'timemachine_quota': 0,
                'vuid': '',
                'shadowcopy': True,
                'fsrvp': False,
                'enabled': True,
                'cluster_volname': '',
                'afp': False,
                'path_local': '/mnt/crave/data',
                'locked': False
            },
        ],
        {
            'properties': {
                'mountpoint': {
                    'parsed': '/mnt/crave/data',
                    'rawvalue': '/mnt/crave/data',
                    'value': '/mnt/crave/data',
                    'source': 'DEFAULT',
                    'source_info': None
                },
                'acltype': {
                    'parsed': 'posix',
                    'rawvalue': 'posix',
                    'value': 'posix',
                    'source': 'LOCAL',
                    'source_info': None
                }
            },
            'id': 'crave/data',
            'type': 'FILESYSTEM',
            'name': 'crave/data',
            'pool': 'crave',
            'encrypted': False,
            'encryption_root': None,
            'key_loaded': False,
            'children': []
        }
    ]
])
def test_get_smb_shares(mocker, middleware_return_values):
    output = get_asset('smb_shares_output.txt')
    mock_client = mocker.MagicMock(side_effect=middleware_return_values)
    mocker.patch('ixdiagnose.plugins.smb.run', return_value=CompletedProcess(
        args=(
            'net conf showshare data\nls -ld /mnt/crave/data\ndf -T /mnt/crave/data\n',
        ),
        returncode=0,
        stdout=output,
        stderr=''
    ))
    result = get_smb_shares(mock_client, None)
    assert isinstance(result, str)
    assert result == output
