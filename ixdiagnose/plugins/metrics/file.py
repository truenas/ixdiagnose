import shutil

from ixdiagnose.plugins.prerequisites.base import Prerequisite
from typing import Callable, Dict, List, Tuple

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


class RedactedFileMetric(FileMetric):
    """
    Copies the specified text file, calling the redact_callback on each line
    to perform any necessary redaction.
    """

    def __init__(self, name: str,
                 file_path: str,
                 prerequisites: List[Prerequisite] = None,
                 extension: str = '.txt',
                 redact_callback: Callable[[str], str] | None = None):
        super().__init__(name, file_path, prerequisites, extension)
        self.redact_callback = redact_callback

    def execute_impl(self) -> Tuple[Dict, str]:
        report = {
            'error': None, 'description': f'Redacted contents of {self.file_path!r}',
        }
        output = ''
        try:
            with open(self.file_path, "r", encoding="utf-8") as input_file:
                output_filepath = self.output_file_path(self.execution_context['output_dir'])
                with open(output_filepath, "w", encoding="utf-8") as output_file:
                    for line in input_file:
                        if self.redact_callback:
                            line = self.redact_callback(line)
                        output_file.write(line)
        except FileNotFoundError:
            report['error'] = f'{self.file_path!r} file path does not exist'

        return report, output
