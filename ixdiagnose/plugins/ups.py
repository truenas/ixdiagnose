from typing import Any

from ixdiagnose.utils.formatter import remove_keys
from ixdiagnose.utils.middleware import MiddlewareClient, MiddlewareCommand
from ixdiagnose.utils.run import run

from .base import Plugin
from .metrics import MiddlewareClientMetric, PythonMetric
from .prerequisites import ServiceRunningPrerequisite


def upsc_output(client: MiddlewareClient, context: Any) -> str:
    ups_identifier = client.call('ups.config')['complete_identifier']
    upsc = run(['upsc', ups_identifier], check=False)
    if upsc.returncode:
        return f'Failed to retrieve upsc output: {upsc.stderr}'
    else:
        return upsc.stdout


class UPS(Plugin):
    name = 'ups'
    metrics = [
        MiddlewareClientMetric(
            'ups_config',
            [
                MiddlewareCommand('ups.config', format_output=remove_keys(['monpwd'])),
            ]
        ),
        PythonMetric(
            'upsc_output',
            upsc_output,
            prerequisites=[ServiceRunningPrerequisite('nut-monitor')],
            serializable=False
        ),
    ]
