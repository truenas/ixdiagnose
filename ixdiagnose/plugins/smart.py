import json

from typing import Any

from ixdiagnose.utils.middleware import MiddlewareClient
from ixdiagnose.utils.run import run

from .base import Plugin
from .metrics import PythonMetric


def smart_output(client: MiddlewareClient, context: Any) -> str:
    include = '8,65,66,67,68,69,70,71,128,129,130,131,132,133,134,135,254,259'
    cp = run(['lsblk', '-ndo', 'name,vendor', '-I', include, '-J'], check=False)
    if cp.returncode:
        return cp.stderr

    serializable = context['serializable']
    output = {} if serializable else ''
    for i in json.loads(cp.stdout)['blockdevices']:
        disk, vendor = i['name'], i['vendor']
        cmd = ['smartctl', '-x', f'/dev/{disk}']
        nvme_msg = ''
        if vendor is not None and vendor.lower().strip() == 'nvme':
            # is an nvme device sitting behind tri-mode HBA
            nvme_msg = ' (NVMe device detected)'
            cmd.extend(['-d', 'nvme'])

        if serializable:
            # -j for json
            # -c "compressed" json (removes unnecessary newlines, etc)
            cmd.extend(['-jc'])

        cp = run(cmd, check=False, timeout=3)
        if serializable:
            if cp.returncode:
                output[disk] = cp.stderr
            else:
                try:
                    output[disk] = json.loads(cp.stdout)
                except Exception as e:
                    output[disk] = str(e)
        else:
            msg = f'Block Device: /dev/{disk}{nvme_msg}'
            output += f'{"=" * (len(msg) + 5)}\n'
            output += f'  {msg}\n'
            output += f'{"=" * (len(msg) + 5)}\n\n{cp.stderr if cp.returncode else cp.stdout}\n\n'

    return output


class SMART(Plugin):
    name = 'smart'
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
