import json
import pytest

from ixdiagnose.exceptions import CallError
from ixdiagnose.plugins.metrics.python import PythonMetric


@pytest.mark.parametrize('name, output, report, should_work', [
    (
        'smb_shares',
        {
            'crave': [],
            'rootd': [
                {
                    'name': 'rootd',
                    'key_format': 'HEX',
                    'key_present_in_database': True,
                    'valid_key': True,
                    'locked': True,
                    'unlock_error': None,
                    'unlock_successful': True
                },
            ]
        },
        {'error': None},
        True
    ),
    (
        'smb_shares',
        {
            'crave': [],
            'rootd': [
                {
                    'name': 'rootd',
                    'key_format': 'HEX',
                    'key_present_in_database': True,
                    'valid_key': True,
                    'locked': True,
                    'unlock_error': None,
                    'unlock_successful': False
                }
            ]
        },
        {'error': 'some error occurred'},
        False
    )
])
def test_python_metric(mocker, monkeypatch, name, output, report, should_work):
    mock_client = mocker.MagicMock()
    mocker.patch('json.dumps', return_value=json.dumps(output))
    mock_callback = mocker.Mock()
    python_metric = PythonMetric(name, mock_callback)
    python_metric.middleware_client = mock_client
    error_report, result = python_metric.execute_impl()
    if should_work:
        assert error_report == report
    else:
        assert error_report != report


@pytest.mark.parametrize('name,callback,should_work', [
    (
        'smb_shares',
        lambda client, context: None,
        True,
    ),
    (
        'smb_shares',
        lambda client: None,
        False,
    ),
    (
        'smb_shares',
        'not a callable',
        False,
    )
])
def test_python_metric_callback(name, callback, should_work):
    if should_work:
        assert isinstance(PythonMetric(name, callback), PythonMetric) is True
    else:
        with pytest.raises(CallError):
            PythonMetric(name, callback)
