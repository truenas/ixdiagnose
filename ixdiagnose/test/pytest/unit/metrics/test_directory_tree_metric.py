import pytest

from ixdiagnose.plugins.metrics.directory_tree import DirectoryTreeMetric


directory_tree_output = [
    {
        'name': 'truenas_default.crt',
        'path': '/etc/certificates/truenas_default.crt',
        'realpath': '/etc/certificates/truenas_default.crt',
        'type': 'FILE',
        'size': 1334,
        'mode': 33188,
        'acl': False,
        'uid': 0,
        'gid': 0,
        'is_mountpoint': False,
        'is_ctldir': False
    },
    {
        'name': 'CA',
        'path': '/etc/certificates/CA',
        'realpath': '/etc/certificates/CA',
        'type': 'DIRECTORY',
        'size': 2,
        'mode': 16877,
        'acl': False,
        'uid': 0,
        'gid': 0,
        'is_mountpoint': False,
        'is_ctldir': False,
        'children': []
    },
    {
        'name': 'truenas_default.key',
        'path': '/etc/certificates/truenas_default.key',
        'realpath': '/etc/certificates/truenas_default.key',
        'type': 'FILE',
        'size': 1704,
        'mode': 33024,
        'acl': False,
        'uid': 0,
        'gid': 0,
        'is_mountpoint': False,
        'is_ctldir': False
    }
]


@pytest.mark.parametrize('name,path,result,report,should_work', [
    (
        'certs', '/etc/certificates',
        (directory_tree_output, []),
        [],
        True,
    ),
    (
        'certs', '/etc/certificates',
        (directory_tree_output, []),
        [{'error': None, 'path': '/etc/certificates'}],
        False,
    ),
    (
        'certs', '/etc/certificates',
        (directory_tree_output, [{'error': None, 'path': '/etc/certificates'}]),
        [{'error': None, 'path': '/etc/certificates'}],
        True,
    ),
    (
        'certs', '/etc/certificates',
        (directory_tree_output, [{'error': None, 'path': '/etc/certificates'}]),
        [],
        False,
    ),
])
def test_directory_tree_metric(mocker, name, path, result, report, should_work):
    mocker.patch('ixdiagnose.plugins.metrics.directory_tree.get_results', return_value=result)
    directory_tree = DirectoryTreeMetric(name, path)
    if not should_work:
        reports, results = directory_tree.execute_impl()
        assert reports != report
    else:
        reports, results = directory_tree.execute_impl()
        assert reports == report
