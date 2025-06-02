from ixdiagnose.utils.formatter import redact_keys
from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import MiddlewareClientMetric


class NVMet(Plugin):
    name = 'nvmet'
    metrics = [MiddlewareClientMetric(
        'nvmet_config',
        [
            MiddlewareCommand('nvmet.global.config', result_key='global_config'),
            MiddlewareCommand(
                'nvmet.host.query',
                result_key='hosts',
                format_output=redact_keys(exclude=['dhchap_key', 'dhchap_ctrl_key'])
            ),
            MiddlewareCommand(
                'nvmet.host_subsys.query',
                result_key='host_subsys',
                format_output=redact_keys(exclude=['host.nvmet_host_dhchap_key', 'host.nvmet_host_dhchap_ctrl_key'])
            ),
            MiddlewareCommand('nvmet.namespace.query', result_key='namespaces'),
            MiddlewareCommand('nvmet.port.query', result_key='ports'),
            MiddlewareCommand('nvmet.port_subsys.query', result_key='port_subsys'),
            MiddlewareCommand('nvmet.subsys.query', result_key='subsys'),
        ]
    )]
