import pytest

from ixdiagnose.utils.middleware import MiddlewareCommand, MiddlewareResponse


@pytest.mark.parametrize('endpoint,api_payload,output,response,should_work', [
    (
        'vm.device.usb_passthrough_choices',
        None,
        {
            'usb_1_1': {
                'capability': {
                    'bus': '1',
                    'device': '2',
                    'product': 'QEMU USB Tablet',
                    'product_id': '0x0001',
                    'vendor': 'Adomax Technology Co., Ltd',
                    'vendor_id': '0x0627',
                },
                'available': True,
                'error': None,
                },
        },
        MiddlewareResponse(result_key='usb_passthrough_choices', error=None, output={
            'usb_1_1': {
                'capability': {
                    'bus': '1',
                    'device': '2',
                    'product': 'QEMU USB Tablet',
                    'product_id': '0x0001',
                    'vendor': 'Adomax Technology Co., Ltd',
                    'vendor_id': '0x0627'
                }, 'available': True,
                'error': None
            }
        }),
        True
    ),
    (
        'vm.device.usb_passthrough_choices',
        None,
        {
            'usb_1_1': {
                'capability': {
                    'bus': '1',
                    'device': '2',
                    'product': 'QEMU USB Tablet',
                    'product_id': '0x0001',
                    'vendor': 'Adomax Technology Co., Ltd',
                    'vendor_id': '0x0627'
                },
                'available': False,
                'error': 'Error Occurred'
            }
        },
        MiddlewareResponse(result_key='usb_passthrough_choices', error='Error Occurred', output={
            'usb_1_1': {
                'capability': {
                    'bus': '1',
                    'device': '2',
                    'product': 'QEMU USB Tablet',
                    'product_id': '0x0001',
                    'vendor': 'Adomax Technology Co., Ltd', 'vendor_id': '0x0627'
                },
                'available': True,
                'error': 'error occurred'
            }
        }),
        False
    ),
])
def test_middleware_command(mocker, endpoint, api_payload, output, response, should_work):
    mock_response = mocker.Mock(return_value=MiddlewareResponse(output=output, result_key='usb_passthrough'))
    mocker.patch('ixdiagnose.utils.middleware.MiddlewareCommand.format_output', return_value=output)
    mock_call = mocker.MagicMock()
    mock_call.call.return_value = output
    mock_client = mocker.MagicMock()
    mock_client.return_value = mock_call
    mocker.patch('ixdiagnose.utils.middleware.get_middleware_client', return_value=mock_client)
    cmd_response = MiddlewareCommand(endpoint).execute(middleware_client=mock_response)
    if should_work:
        assert cmd_response.output == response.output
        assert cmd_response.error == response.error
    else:
        assert cmd_response.output != response.output
        assert cmd_response.error != response.error
