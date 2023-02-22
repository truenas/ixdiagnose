from ixdiagnose.plugins.prerequisites.base import Prerequisite
from typing import Dict, List, Tuple

from .base import Metric


class FileMetric(Metric):

    def __init__(self, name: str, file_path: str, prerequisites: List[Prerequisite] = None):
        super().__init__(name, prerequisites)
        self.file_path: str = file_path

    @property
    def output_file_extension(self) -> str:
        return '.txt'

    def execute_impl(self) -> Tuple[Dict, str]:
        report = {
            'error': None, 'description': f'Contents of {self.file_path!r}',
        }
        try:
            with open(self.file_path, 'r') as f:
                output = f.read()
        except FileNotFoundError:
            output = None
            report['error'] = f'{self.file_path!r} file path does not exist'

        return report, output
