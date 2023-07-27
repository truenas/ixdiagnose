from collections import defaultdict
from pathlib import Path

from .base import Plugin
from .metrics import PythonMetric


def cpu_ppin(client, context):
    final = defaultdict(list)
    for i in Path('/sys/devices/system/cpu/').glob('cpu*/topology/ppin'):
        try:
            final[i.read_text().strip()].append(i.parent.parent.name.strip())
        except Exception:
            continue

    return dict(final)


class Cpu(Plugin):
    name = 'cpu'
    metrics = [
        PythonMetric('cpu_ppin_info', cpu_ppin, serializable=True),
    ]
