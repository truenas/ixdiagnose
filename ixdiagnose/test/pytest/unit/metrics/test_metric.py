import pytest

from ixdiagnose.plugins.metrics.base import Metric


@pytest.mark.parametrize('context,data,should_work', [
    (
        {
            'middleware_client': None,
            'output_dir': '/root/debug_reports/ixdiagnose/plugins/iscsi'
        },
        (
            [
                {
                    'endpoint': 'service.query',
                    'error': None,
                    'execution_time': 0.07165694236755371,
                    'description': 'Query all system services with `query-filters` and `query-options`'
                }
            ],
            {
                'key': 'service',
                'output': {
                    'id': 7,
                    'service': 'iscsitarget',
                    'enable': True,
                    'state': 'RUNNING',
                    'pids': []
                }
            }
        ),
        False
    ),
    (
        {
            'middleware_client': None,
            'output_dir': '/root/debug_reports/ixdiagnose/plugins/iscsi'
        },
        (
            [
                {
                    'endpoint': 'service.query',
                    'error': None,
                    'execution_time': 0.07165694236755371,
                    'description': 'Query all system services with `query-filters` and `query-options`'
                }
            ],
            ''
        ),
        True
    )
])
def test_metric_execute(mocker, context, data, should_work):
    mocker.patch('ixdiagnose.plugins.metrics.base.Metric.initialize_context', return_value=None)
    mocker.patch('ixdiagnose.plugins.metrics.base.Metric.execute_impl', return_value=data)
    metric = Metric('iscsi')
    if should_work:
        assert metric.execute(context) == data
    else:
        with pytest.raises(AssertionError):
            metric.execute(context)
