import os
import time
import traceback

from ixdiagnose.utils.formatter import dumps
from ixdiagnose.utils.paths import get_artifacts_base_dir
from typing import List, Optional

from .items import Item


class Artifact:

    base_dir: str = NotImplementedError
    name: str = NotImplementedError
    individual_item_max_size_limit: Optional[int] = None
    items: List[Item] = []

    def __init__(self):
        self.debug_report: dict = {}

        assert type(self.base_dir) is str and bool(self.base_dir) is True
        assert type(self.name) is str and bool(self.name) is True
        assert all(isinstance(item, Item) for item in self.items) is True

        if self.individual_item_max_size_limit is not None:
            for item in self.items:
                item.max_size = self.individual_item_max_size_limit

    @property
    def output_dir(self) -> str:
        return os.path.join(get_artifacts_base_dir(), self.name)

    def write_debug_report(self) -> None:
        with open(os.path.join(self.output_dir, 'report.json'), 'w') as f:
            f.write(dumps(self.debug_report))

    def gather(self) -> dict:
        start_time = time.time()
        os.makedirs(self.output_dir, exist_ok=True)
        error = tb = None
        try:
            self.gather_impl()
            self.write_debug_report()
        except Exception as exception:
            error = str(exception)
            tb = traceback.format_exc()

        return {
            'execution_time': time.time() - start_time,
            'execution_error': error,
            'execution_traceback': tb,
        }

    def gather_impl(self) -> None:
        for item in self.items:
            item_report = item_execution_error = item_execution_traceback = None
            start_time = time.time()
            try:
                item_report = item.copy(self.base_dir, self.output_dir)
            except Exception as exc:
                item_execution_error = str(exc)
                item_execution_traceback = traceback.format_exc()

            self.debug_report[item.name] = {
                'execution_time': time.time() - start_time,
                'item_execution_error': item_execution_error,
                'item_execution_traceback': item_execution_traceback,
                'item_report': item_report,
            }
