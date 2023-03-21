import json
import pytest

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
    mock_call = mocker.MagicMock()
    mock_call.call.return_value = output
    mock_client = mocker.MagicMock()
    mock_client.return_value = mock_call
    mocker.patch('ixdiagnose.plugins.metrics.python.get_middleware_client', return_value=mock_client)
    mocker.patch('json.dumps', return_value=json.dumps(output))
    mock_callback = mocker.Mock()
    python_metric = PythonMetric(name, mock_callback)
    error_report, result = python_metric.execute_impl()
    if should_work:
        assert error_report == report
    else:
        assert error_report != report
