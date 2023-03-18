import os
import traceback

from typing import Optional, Tuple


class Item:

    def __init__(self, name: str, max_size: Optional[int] = None):
        self.name: str = name
        self.max_size: Optional[int] = max_size

        assert type(self.name) is str and bool(self.name) is True

    def exists(self, item_path: str) -> Tuple[bool, str]:
        exists = os.path.exists(item_path)
        return exists, '' if exists else f'{item_path!r} does not exist'

    def size(self, item_path: str) -> int:
        raise NotImplementedError()

    def to_be_copied_checks(self, item_path: str) -> Tuple[bool, Optional[str]]:
        return True, None

    def is_to_be_copied(self, item_path) -> Tuple[bool, Optional[str]]:
        exists, exists_error = self.exists(item_path)
        if not exists:
            return False, exists_error

        if self.max_size is not None:
            size = self.size(item_path)
            if size > self.max_size:
                return False, f'{item_path!r} exceeds specified {self.max_size!r} size with size being {size!r}'

        return self.to_be_copied_checks(item_path)

    def source_item_path(self, item_dir: str) -> str:
        return os.path.join(item_dir, self.name)

    def destination_item_path(self, destination_dir: str) -> str:
        return os.path.join(destination_dir, self.name)

    def initialize_context(self, item_path: str) -> None:
        pass

    def copy(self, item_dir: str, destination_dir: str) -> dict:
        report = {
            'error': None,
            'traceback': None,
            'copied_items': [],
        }
        item_path = self.source_item_path(item_dir)
        self.initialize_context(item_path)
        to_be_copied, report['error'] = self.is_to_be_copied(item_path)
        if to_be_copied:
            try:
                report['copied_items'] = self.copy_impl(item_path, self.destination_item_path(destination_dir))
            except Exception as e:
                report.update({
                    'error': str(e),
                    'traceback': traceback.format_exc(),
                })

        return report

    def copy_impl(self, item_path: str, destination_path: str) -> list:
        raise NotImplementedError()
