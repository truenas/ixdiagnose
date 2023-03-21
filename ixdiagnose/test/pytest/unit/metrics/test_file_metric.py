import contextlib
import filecmp
import os
import pytest

from ixdiagnose.plugins.metrics.file import FileMetric


TEST_FILE_DIR = '/tmp'


@pytest.mark.parametrize('name,file_path,should_work,extension', [
    ('hosts', '/etc/hosts', True, ''),
    ('hosts', '/etc/some_test_file', False, ''),
])
def test_file_metric(mocker, monkeypatch, name, file_path, should_work, extension):
    output_file_path = os.path.join(TEST_FILE_DIR, name)
    file_metric = FileMetric(name, file_path, extension=extension)
    file_metric.execution_context = {'output_dir': TEST_FILE_DIR}
    assert file_metric.output_file_path(TEST_FILE_DIR) == output_file_path

    try:
        report = file_metric.execute_impl()[0]
        if should_work:
            assert os.path.exists(output_file_path) is True
            assert report['error'] is None
            assert filecmp.cmp(file_path, output_file_path, False) is True
        else:
            assert os.path.exists(output_file_path) is False
            assert report['error'] is not None
    finally:
        with contextlib.suppress(FileNotFoundError):
            os.unlink(output_file_path)
