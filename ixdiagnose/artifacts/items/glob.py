import functools
import os
import glob
import shutil
import stat

from typing import List, Optional, Tuple

from .base import Item
from .directory import copy2, get_directory_size


class Glob(Item):

    def __init__(self, name: str, max_size: Optional[int] = None, to_skip_items: Optional[list] = None):
        super().__init__(name, max_size)
        self.init_vars()
        self.to_skip_items: List[str] = to_skip_items or []

    def init_vars(self) -> None:
        self.items: List[dict] = []

    def initialize_context(self, item_path: str) -> None:
        self.init_vars()
        for entry in self.to_copy_items(item_path):
            if os.path.isfile(entry):
                item = {
                    'name': os.path.basename(entry),
                    'type': 'file',
                    'size': os.path.getsize(entry),
                    'path': entry,
                }
            else:
                item = {
                    'name': os.path.basename(entry),
                    'type': 'dir',
                    'size': get_directory_size(entry),
                    'path': entry,
                }

            self.items.append(item)

    def to_copy_items(self, items_path: str) -> list:
        return glob.glob(items_path)

    def exists(self, item_path: str) -> Tuple[bool, str]:
        exists = bool(self.items)
        return exists, '' if exists else f'No items found matching {self.name!r} glob pattern'

    def destination_item_path(self, destination_dir: str) -> str:
        return destination_dir

    def size(self, item_path: str) -> int:
        return sum(item['size'] for item in self.items)

    def copy_validation(self, item: dict) -> Tuple[bool, str]:

        if self.max_size and item['size'] > self.max_size:
            return False, f'{item["path"]!r} exceeds specified {self.max_size!r} size'
        elif stat.S_IRUSR & os.stat(item['path']).st_mode == 0:
            return False, f'{item["path"]!r} is not readable'
        return True, ''

    def to_be_copied_checks(self, item_path: str) -> Tuple[bool, Optional[dict]]:
        item_check_report = {}
        for item in self.items:
            to_copy, error = self.copy_validation(item)

            if not to_copy:
                item_check_report[item['path']] = error
                self.to_skip_items.append(item['path'])

        return len(self.items) != len(self.to_skip_items), item_check_report

    def copy_impl(self, item_path: str, destination_path: str) -> list:
        copied_items = []
        for item in filter(lambda i: i['path'] not in self.to_skip_items, self.items):

            destination_parent_path = os.path.join(destination_path, os.path.dirname(item['path'])[1:])
            os.makedirs(destination_parent_path, exist_ok=True)
            if item['type'] == 'file':
                shutil.copy2(item['path'], destination_parent_path)
                copied_items.append(item['path'])
            else:
                shutil.copytree(
                    item['path'], os.path.join(destination_parent_path, os.path.basename(item['path'])),
                    copy_function=functools.partial(copy2, copied_items), dirs_exist_ok=True,
                )

        return copied_items
