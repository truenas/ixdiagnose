import pytest

from ixdiagnose.plugins.metrics.directory_tree import DirectoryTreeMetric, get_results
from ixdiagnose.utils.middleware import MiddlewareCommand, MiddlewareResponse


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


@pytest.mark.parametrize('name,isdir,path,result,report,should_work', [
    (
        'certs', '/etc/certificates',
        True,
        (directory_tree_output, []),
        [],
        True,
    ),
    (
        'certs', '/etc/certificates',
        False,
        (directory_tree_output, []),
        [{'error': None, 'path': '/etc/certificates'}],
        False,
    ),
    (
        'certs', '/etc/certificates',
        False,
        (directory_tree_output, [{'error': '/etc/certificates either does not exist or is not a directory',
                                  'path': '/etc/certificates'}]),
        [{'error': '/etc/certificates either does not exist or is not a directory', 'path': '/etc/certificates'}],
        True,
    ),
    (
        'certs', '/etc/certificates',
        True,
        (directory_tree_output, [{'error': None, 'path': '/etc/certificates'}]),
        [],
        False,
    ),
])
def test_directory_tree_metric(mocker, name, isdir, path, result, report, should_work):
    mocker.patch('os.path.isdir', return_value=isdir)
    mocker.patch('ixdiagnose.plugins.metrics.directory_tree.get_results', return_value=result)
    directory_tree = DirectoryTreeMetric(name, path)
    if should_work:
        reports, results = directory_tree.execute_impl()
        assert reports == report
    else:
        reports, results = directory_tree.execute_impl()
        assert reports != report


@pytest.mark.parametrize('middleware_response,results,reports', [
    (
        MiddlewareResponse(
            result_key='filesystem_listdir',
            error=None,
            output=[
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
                },
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
                }
            ]
        ),
        [
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
           },
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
           }
        ],
        [],
    ),
    (
        MiddlewareResponse(
            result_key='filesystem_listdir',
            error='File does not exists',
            output=[]
        ),
        [],
        [
            {'error': "Failed to list contents of '/etc/certificates': File does not exists"}
        ],
    ),
])
def test_get_results(mocker, middleware_response, results, reports):
    mocker.patch.object(MiddlewareCommand, 'execute', return_value=middleware_response)
    output, report = get_results('/etc/certificates')
    assert output == results
    assert report == reports
