import os

from typing import Any, Tuple


class Metric:

    def __init__(self, name: str):
        self.name: str = name

    @property
    def output_file_extension(self) -> str:
        return '.json'

    def output_file_path(self, base_dir: str) -> str:
        return os.path.join(base_dir, f'{self.name}{self.output_file_extension}')

    def execute(self) -> Tuple[Any, str]:
        data = self.execute_impl()
        assert isinstance(data, (list, tuple)) and len(data) == 2
        return data

    def execute_impl(self) -> Tuple[Any, str]:
        raise NotImplementedError
