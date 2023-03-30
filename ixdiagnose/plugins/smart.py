from typing import Any

from ixdiagnose.utils.middleware import MiddlewareClient, MiddlewareCommand
from ixdiagnose.utils.run import run

from .base import Plugin
from .metrics import MiddlewareClientMetric, PythonMetric


def smart_output(client: MiddlewareClient, context: Any) -> str:
    include = '8,65,66,67,68,69,70,71,128,129,130,131,132,133,134,135,254,259'
    cp = run(['lsblk', '-ndo', 'name', '-I', include], check=False)
    if cp.returncode:
        return cp.stderr

    output = ''
    for disk in filter(bool, cp.stdout.splitlines()):
        command = ''
        msg = '(NVME device detected)' if 'nvme' in disk else ''
        msg = f'Block Device: /dev/{disk} {msg}'
        command += f'echo "{"=" * (len(msg) + 5)}"\n'
        command += f'echo "  {msg}"\n'
        command += f'echo "{"=" * (len(msg) + 5)}"\n'
        next_line = '\n' * 5
        command += f'smartctl -a /dev/{disk}{next_line}'
        cp = run(command, check=False, timeout=3)
        output += cp.stderr if cp.returncode else cp.stdout

    # TODO: Check the awk script and see what it normalizes
    return output


class SMART(Plugin):
    name = 'smart'
    metrics = [
        MiddlewareClientMetric(
            'smartd_config', [
                MiddlewareCommand(
                    'service.query', [[['service', '=', 'smartd']], {'get': True}], result_key='SMARTD Status'
                ),
                MiddlewareCommand('smart.test.query', result_key='SMART Tests'),
            ]
        ),
        PythonMetric(
            'smart_out', smart_output, description='SMART output', serializable=False,
        ),
    ]
