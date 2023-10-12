import pytest
import tempfile

from ixdiagnose.config import conf
from ixdiagnose.exceptions import CallError
from ixdiagnose.run import generate_debug


@pytest.mark.parametrize(
    'debug_path,path_is_abs,compress,path_exists,expected_output,should_work', [
        (
            '/tmp/ixdiagnose',
            True,
            True,
            False,
            '/tmp/ixdiagnose.tgz',
            True,
        ),
        (
            '/tmp/ixdiagnose',
            False,
            True,
            False,
            '/tmp/ixdiagnose.tgz',
            False,
        ),
        (
            '/tmp/ixdiagnose',
            False,
            True,
            False,
            '/tmp/ixdiagnose.tgz',
            False,
        ),
        (
            '/tmp/ixdiagnose',
            True,
            True,
            True,
            '/tmp/ixdiagnose.tgz',
            False,
        ),
        (
            None,
            True,
            False,
            False,
            '/tmp/tempdir6746',
            True,
        ),
        (
            '/tmp/ixdiagnose',
            True,
            False,
            False,
            '/tmp/ixdiagnose',
            True,
        ),
    ]
)
def test_compression_validation(mocker, path_is_abs, debug_path, path_exists, compress, expected_output, should_work):
    conf.debug_path = debug_path
    mocker.patch('os.path.isabs', return_value=path_is_abs)
    conf.compress = compress
    conf.compressed_path = '/tmp/ixdiagnose.tgz'
    if compress:
        mocker.patch('os.path.exists', return_value=path_exists)

    if not conf.debug_path:
        mocked_temp_dir = mocker.MagicMock()
        mocked_temp_dir.name = '/tmp/tempdir6746'
        mocker.patch.object(tempfile, 'TemporaryDirectory', return_value=mocked_temp_dir)

    for method in (
        'os.makedirs',
        'os.chmod',
        'ixdiagnose.run.generate_plugins_debug',
        'ixdiagnose.run.gather_artifacts',
        'ixdiagnose.run.compress_debug',
        'ixdiagnose.run.event_callbacks.clear',
    ):
        mocker.patch(method, return_value=None)

    if should_work:
        assert generate_debug() == expected_output
    else:
        with pytest.raises(CallError):
            generate_debug()
