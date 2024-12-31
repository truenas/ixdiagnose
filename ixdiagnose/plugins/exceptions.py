import json

from .base import Plugin
from .metrics import PythonMetric

LOG_FILES = (
    '/var/log/app_lifecycle.log',
    '/var/log/app_migrations.log',
    '/var/log/failover.log',
    '/var/log/middlewared.log',
    '/var/log/netdata_api.log',
    '/var/log/zettarepl.log'
)


def parse_log_file(path: str) -> list[dict]:
    results = []
    with open(path, 'r') as f:
        for line in f:
            if '@cee:{"TNLOG":' not in line:
                continue

            data = json.loads(line.split('@cee:')[1])
            results.append(data['TNLOG'])

    return results


def gather_exceptions(client: None, resource_type: str) -> dict:
    results = {}
    for log in LOG_FILES:
        try:
            results[log] = parse_log_file(log)
        except FileNotFoundError:
            pass

    return results


class LoggedExceptions(Plugin):
    name = 'logged_exceptions'
    metrics = [PythonMetric('log_file_exceptions', gather_exceptions, serializable=True)]
