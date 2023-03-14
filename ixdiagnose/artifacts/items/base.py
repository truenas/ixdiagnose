import os
import traceback

from typing import Optional, Tuple


class Item:

    def __init__(self, name: str, max_size: Optional[int] = None):
        self.name: str = name
        self.max_size: Optional[int] = max_size

    def exists(self, item_path: str) -> bool:
        return os.path.exists(item_path)

    def size(self, item_path: str) -> int:
        raise NotImplementedError()

    def is_to_be_copied(self, item_path) -> Tuple[bool, Optional[str]]:
        if not self.exists(item_path):
            return False, f'{item_path!r} does not exist'

        if self.max_size is not None:
            size = self.size(item_path)
            if size > self.max_size:
                return False, f'{item_path!r} exceeds specified {self.max_size!r} size with size being {size!r}'

        return True, None

    def copy(self, item_dir: str, destination_dir: str) -> dict:
        report = {
            'error': None,
            'traceback': None,
            'copied_items': [],
        }
        item_path = os.path.join(item_dir, self.name)
        to_be_copied, report['error'] = self.is_to_be_copied(item_path)
        if to_be_copied:
            try:
                report['copied_items'] = self.copy_impl(item_path, os.path.join(destination_dir, self.name))
            except Exception as e:
                report.update({
                    'error': str(e),
                    'traceback': traceback.format_exc(),
                })

        return report

    def copy_impl(self, item_path: str, destination_path: str) -> list:
        raise NotImplementedError()
