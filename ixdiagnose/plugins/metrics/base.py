import os

from ixdiagnose.plugins.prerequisites.base import Prerequisite
from typing import Any, List, Tuple


class Metric:

    def __init__(self, name: str, prerequisites: List[Prerequisite] = None):
        self.name: str = name
        self.prerequisites: List[Prerequisite] = prerequisites or []

    @property
    def output_file_extension(self) -> str:
        return '.json'

    def output_file_path(self, base_dir: str) -> str:
        return os.path.join(base_dir, f'{self.name}{self.output_file_extension}')

    def execute(self) -> Tuple[Any, str]:
        for prerequisite in self.prerequisites:
            if not prerequisite.evaluate():
                return {'error': f'"{prerequisite}" prerequisite failed'}, ''

        data = self.execute_impl()
        assert isinstance(data, (list, tuple)) and len(data) == 2
        return data

    def execute_impl(self) -> Tuple[Any, str]:
        raise NotImplementedError
