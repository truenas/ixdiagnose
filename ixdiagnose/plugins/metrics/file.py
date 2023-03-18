import shutil

from ixdiagnose.plugins.prerequisites.base import Prerequisite
from typing import Dict, List, Tuple

from .base import Metric


class FileMetric(Metric):

    def __init__(self, name: str, file_path: str, prerequisites: List[Prerequisite] = None, extension: str = '.txt'):
        super().__init__(name, prerequisites)
        self.extension: str = extension
        self.file_path: str = file_path

        assert type(self.file_path) is str and bool(self.file_path) is True

    @property
    def output_file_extension(self) -> str:
        return self.extension

    def execute_impl(self) -> Tuple[Dict, str]:
        report = {
            'error': None, 'description': f'Contents of {self.file_path!r}',
        }
        output = ''
        try:
            shutil.copy(self.file_path, self.output_file_path(self.execution_context['output_dir']))
        except FileNotFoundError:
            report['error'] = f'{self.file_path!r} file path does not exist'

        return report, output
