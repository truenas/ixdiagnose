from ixdiagnose.utils.formatter import remove_keys
from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import MiddlewareClientMetric


class Certificates(Plugin):
    name = 'certificates'
    metrics = [
        MiddlewareClientMetric('certificates', [
            MiddlewareCommand(
                'certificate.query', [['cert_type_CSR', '=', False]],
                result_key='certificates', format_output=remove_keys([
                    'privatekey', 'issuer', 'signedby',
                ])
            ),
            MiddlewareCommand(
                'certificate.query', [['cert_type_CSR', '=', True]],
                result_key='csr', format_output=remove_keys([
                    'privatekey', 'issuer', 'signedby',
                ])
            )
        ]),
        MiddlewareClientMetric('certificate_authorities', [
            MiddlewareCommand(
                'certificateauthority.query', format_output=remove_keys([
                    'privatekey', 'issuer', 'signedby',
                ])
            )
        ]),
    ]
