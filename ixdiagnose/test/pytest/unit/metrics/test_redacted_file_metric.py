import contextlib
import filecmp
import os
import pytest

from ixdiagnose.plugins.metrics.file import RedactedFileMetric
from ixdiagnose.plugins.iscsi import redact_chap_passwords

from ixdiagnose.test.pytest.unit.utils import get_asset_path


TEST_FILE_DIR = '/tmp'


@pytest.mark.parametrize('name,raw_asset_filename,cooked_asset_filename,extension,callback', [
    (
        'scst.conf',
        'redacted_file_metric_scst_input.txt',
        'redacted_file_metric_scst_output.txt',
        '.conf',
        redact_chap_passwords
    ),
])
def test_redacted_file_metric(mocker,
                              monkeypatch,
                              name,
                              raw_asset_filename,
                              cooked_asset_filename,
                              extension,
                              callback):
    raw_file_path = get_asset_path(raw_asset_filename)
    cooked_file_path = get_asset_path(cooked_asset_filename)
    output_file_path = os.path.join(TEST_FILE_DIR, name)

    file_metric = RedactedFileMetric('scst', raw_file_path, extension=extension, redact_callback=callback)
    file_metric.execution_context = {'output_dir': TEST_FILE_DIR}
    assert file_metric.output_file_path(TEST_FILE_DIR) == output_file_path

    try:
        report = file_metric.execute_impl()[0]
        assert os.path.exists(output_file_path) is True
        assert report['error'] is None
        assert filecmp.cmp(cooked_file_path, output_file_path, False) is True
    finally:
        with contextlib.suppress(FileNotFoundError):
            os.unlink(output_file_path)
