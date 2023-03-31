import json

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

    serializable = context['serializable']
    output = {} if serializable else ''
    for disk in filter(bool, cp.stdout.splitlines()):
        cp = run(['smartctl', '-a', f'/dev/{disk}'] + (['-j'] if serializable else []), check=False, timeout=3)

        if serializable:
            try:
                disk_output = cp.stderr if cp.returncode else json.loads(cp.stdout)
            except json.JSONDecodeError as e:
                disk_output = str(e)

            output[disk] = disk_output
        else:
            msg = '(NVME device detected)' if 'nvme' in disk else ''
            msg = f'Block Device: /dev/{disk} {msg}'
            output += f'{"=" * (len(msg) + 5)}\n'
            output += f'  {msg}\n'
            output += f'{"=" * (len(msg) + 5)}\n\n{cp.stderr if cp.returncode else cp.stdout}\n\n'

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
    ]
    raw_metrics = [
        PythonMetric(
            'smart_out', smart_output, description='SMART output', serializable=False, context={'serializable': False},
        ),
    ]
    serializable_metrics = [
        PythonMetric(
            'smart_out', smart_output, description='SMART output', context={'serializable': True},
        ),
    ]
