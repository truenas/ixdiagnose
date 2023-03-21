import pytest

from ixdiagnose.utils.middleware import MiddlewareCommand, MiddlewareResponse
from ixdiagnose.plugins.metrics.middleware import MiddlewareClientMetric


@pytest.mark.parametrize('name,cmds,responses,context,should_work', [
    (
        'mid_cmds',
        [
            MiddlewareCommand('vm.device.usb_passthrough_choices', result_key='usb_passthrough_choices'),
            MiddlewareCommand('vm.device.passthrough_device_choices', result_key='pci_passthrough_device_choices')
        ],
        [
            MiddlewareResponse(result_key='usb_passthrough_choices', error=None, output={
                'usb_1_1': {
                    'capability': {
                        'bus': '1',
                        'device': '2',
                        'product': 'QEMU USB Tablet',
                        'product_id': '0x0001',
                        'vendor': 'Adomax Technology Co., Ltd',
                        'vendor_id': '0x0627'
                    },
                    'available': True,
                    'error': None,
                },
            }),
            MiddlewareResponse(result_key='pci_passthrough_device_choices', error=None, output={}),
        ],
        [
            {
                'key': 'usb_passthrough_choices',
                'output': {
                    'usb_1_1':
                        {
                            'capability':
                                {
                                    'bus': '1',
                                    'device': '2',
                                    'product': 'QEMU USB Tablet',
                                    'product_id': '0x0001',
                                    'vendor': 'Adomax Technology Co., Ltd',
                                    'vendor_id': '0x0627'
                                },
                            'available': True,
                            'error': None
                        }
                }
            },
            {
                'key': 'pci_passthrough_device_choices',
                'output': {}
            }
        ],
        True
    ),
    (
        'mid_cmds',
        [
            MiddlewareCommand('vm.device.usb_passthrough_choices', result_key='usb_passthrough_choices'),
            MiddlewareCommand('vm.device.passthrough_device_choices', result_key='pci_passthrough_device_choices'),
        ],
        [
            MiddlewareResponse(result_key='usb_passthrough_choices', error=None, output={
                'usb_1_1': {
                    'capability': {
                        'bus': '1',
                        'device': '2',
                        'product': 'QEMU USB Tablet',
                        'product_id': '0x0001',
                        'vendor': 'Adomax Technology Co., Ltd',
                        'vendor_id': '0x0627'},
                    'available': True,
                    'error': None
                }
            }),
            MiddlewareResponse(result_key='pci_passthrough_device_choices', error=None, output={})
        ],
        [
            {
                'key': 'usb_passthrough_choices',
                'output': {
                    'usb_1_1': {
                        'capability': {
                            'bus': '1',
                            'device': '2',
                            'product': 'QEMU USB Tablet',
                            'product_id': '0x0001',
                            'vendor': 'Adomax Technology Co., Ltd',
                            'vendor_id': '0x0627'
                        },
                        'available': True,
                        'error': None
                    }
                }
            },
        ],
        False
    ),
])
def test_middleware_metric(mocker, name, cmds, responses, context, should_work):
    mock_client = mocker.Mock()
    mocker.patch('ixdiagnose.utils.middleware.MiddlewareCommand.execute', side_effect=responses)
    mocker.patch('ixdiagnose.plugins.metrics.middleware.MiddlewareClientMetric.get_methods_metadata', return_value={})
    metric = MiddlewareClientMetric(name, cmds)
    metric.middleware_client = mock_client
    if should_work:
        report, output = metric.execute_impl()
        assert output == metric.format_output(context=context)
    else:
        report, output = metric.execute_impl()
        assert output != metric.format_output(context=context)
