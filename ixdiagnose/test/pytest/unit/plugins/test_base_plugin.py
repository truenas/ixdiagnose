import pytest

from ixdiagnose.plugins.metrics.middleware import MiddlewareClientMetric
from ixdiagnose.plugins.base import Plugin
from ixdiagnose.utils.middleware import MiddlewareCommand


@pytest.mark.parametrize('metrics_to_execute,metric_output,metric_report', [
    (
        [
            MiddlewareClientMetric('services', [MiddlewareCommand('service.query', result_key='services_status')]),
        ],
        {
            'key': 'services_status',
            'output': [
                {
                    'id': 1,
                    'service': 'nfs',
                    'enable': True,
                    'state': 'STOPPED',
                    'pids': []
                },
                {
                    'id': 2,
                    'service': 'snmp',
                    'enable': False,
                    'state': 'STOPPED',
                    'pids': []
                },
                {
                    'id': 3,
                    'service': 'ssh',
                    'enable': True,
                    'state': 'RUNNING',
                    'pids': [
                        2602
                    ]
                },
            ]
        },
        [
            {
                'endpoint': 'service.query',
                'error': None,
                'execution_time': 0.6482527256011963,
                'description': 'Query all system services with `query-filters` and `query-options`.\n\n'
                               'Supports the following extra options:\n'
                               '`include_state` - performance optimization to avoid getting service state.\n'
                               'defaults to True.'
            }
        ]
    )
])
def test_ecexute_impl(mocker, metrics_to_execute, metric_output, metric_report):
    mock_client = mocker.MagicMock()
    context = {'middleware_client': mock_client, 'output_dir': '/root/debug_reports/ixdiagnose/plugins/services'}
    mocker.patch('ixdiagnose.plugins.base.Plugin.metrics_to_execute', return_value=metrics_to_execute)
    mocker.patch('os.path.join', return_value='/root/debug_reports/ixdiagnose/plugins/services')
    mock_obj = mocker.mock_open()
    mock_file = mocker.patch('builtins.open', mock_obj)
    mock_file.write = metric_output
    with pytest.raises(AssertionError):
        Plugin()
    Plugin.name = 'services'
    plugin = Plugin()
    assert plugin.execute_impl(context) is None
