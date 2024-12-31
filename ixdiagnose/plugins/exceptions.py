import json

from .base import Plugin
from .metrics import PythonMetric

from middlewared.logger import ALL_LOG_FILES


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
    for log in ALL_LOG_FILES:
        try:
            results[log.logfile] = parse_log_file(log.logfile)
        except FileNotFoundError:
            pass

    return results


class LoggedExceptions(Plugin):
    name = 'logged_exceptions'
    metrics = [PythonMetric('log_file_exceptions', gather_exceptions, serializable=True)]
