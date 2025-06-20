import os

from ixdiagnose.plugins.prerequisites.base import Prerequisite
from typing import Any, List, Tuple


class Metric:

    def __init__(self, name: str, prerequisites: List[Prerequisite] | None = None):
        self.execution_context: Any = None
        self.name = name
        self.prerequisites = prerequisites or []

        assert type(name) is str and bool(name) is True
        assert type(self.prerequisites) is list
        assert all(isinstance(prerequisite, Prerequisite) for prerequisite in self.prerequisites) is True

    @property
    def output_file_extension(self) -> str:
        return '.json'

    def output_file_path(self, base_dir: str) -> str:
        return os.path.join(base_dir, f'{self.name}{self.output_file_extension}')

    def execute(self, execution_context: Any = None) -> Tuple[Any, str]:
        self.execution_context = execution_context
        for prerequisite in self.prerequisites:
            if not prerequisite.evaluate():
                return {'error': f'"{prerequisite}" prerequisite failed'}, ''

        self.initialize_context()
        data = self.execute_impl()
        assert isinstance(data, (list, tuple)) and len(data) == 2
        assert type(data[1]) is str
        return data

    def initialize_context(self) -> None:
        pass

    def execute_impl(self) -> Tuple[Any, str]:
        raise NotImplementedError
