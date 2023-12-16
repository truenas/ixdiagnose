from json import loads

from ixdiagnose.utils.run import run

from .base import Plugin
from .metrics import PythonMetric


def nspawn_containers(client, context):
    try:
        return [
            i for i in loads(run(['machinectl', 'list', '-o', 'json']).stdout)
            if i['service'] == 'systemd-nspawn'
        ]
    except Exception:
        return []


class Containers(Plugin):
    name = 'containers'
    metrics = [
        PythonMetric('nspawn_containers', nspawn_containers, serializable=True),
    ]
