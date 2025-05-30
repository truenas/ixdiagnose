from ixdiagnose.utils.command import Command
from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import MiddlewareClientMetric, CommandMetric


class IPMI(Plugin):
    name = 'ipmi'
    metrics = [
        MiddlewareClientMetric('info', [
            MiddlewareCommand('ipmi.sel.elist', result_key='extended_log_info', job=True),
            MiddlewareCommand('ipmi.sel.info', result_key='general_log', job=True),
            MiddlewareCommand('ipmi.mc.info', result_key='mgmt_controller_info'),
            MiddlewareCommand('ipmi.lan.query', result_key='lan_info'),
            MiddlewareCommand('ipmi.sensors.query', result_key='sensors_info'),
            MiddlewareCommand('ipmi.chassis.info', result_key='chassis_info'),
        ]),
        CommandMetric(
            'ipmitool',
            [Command(['ipmitool', 'fru', 'print'], 'FRU Manufacturing Details', serializable=False)],
        ),
    ]
