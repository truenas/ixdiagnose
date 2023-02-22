import json
import os

from ixdiagnose.utils.middleware import MiddlewareCommand
from typing import Any, Dict, List, Optional, Tuple

from .base import Metric


def get_results(path: str) -> Tuple[List[Dict[str, Any]], List[Dict[str, Optional[str]]]]:
    report = []
    results = []
    response = MiddlewareCommand('filesystem.listdir', [path]).execute()
    if response.error:
        report.append({'error': f'Failed to list contents of {path!r}: {response.error}'})
        return [], report

    for entry in response.output:
        if entry['type'] == 'DIRECTORY':
            entry_results, entry_reports = get_results(entry['path'])
            report.extend(entry_reports)
            entry['children'] = entry_results

        results.append(entry)

    return results, report


class DirectoryTreeMetric(Metric):

    def __init__(self, name: str, path: str):
        super().__init__(name)
        self.path: str = path

    def execute_impl(self) -> Tuple[Any, str]:
        report = {'error': None}
        if not os.path.isdir(self.path):
            report['error'] = f'{self.path!r} either does not exist or is not a directory'
            return report, ''

        results, report = get_results(self.path)
        return report, json.dumps(results, indent=4)
