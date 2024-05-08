import os
import re

from typing import List, Optional, Tuple

from .base import Item
from .directory import Directory
from .file import File


class Pattern(Item):

    def __init__(
        self, name: str, max_size: Optional[int] = None, truncate_files: Optional[bool] = True,
        add_to_base_item_path: Optional[str] = None,
    ):
        super().__init__(name, max_size)
        self.pattern: str = self.name
        self.truncate_files: bool = truncate_files
        self.add_to_base_item_path: Optional[str] = add_to_base_item_path
        self.init_vars()

    @property
    def report_name_key(self):
        return os.path.join(self.add_to_base_item_path, self.pattern) if self.add_to_base_item_path else self.name

    def init_vars(self) -> None:
        self.items: List[Item] = []
        self.to_skip_items: List[Item] = []

    def initialize_context(self, item_path: str) -> None:
        self.init_vars()
        for entry in self.to_copy_items(item_path):
            if entry.is_dir():
                item = Directory(entry.name, max_size=self.max_size)
            else:
                item = File(entry.name, max_size=self.max_size, truncate=self.truncate_files)

            self.items.append(item)

    def exists(self, item_path: str) -> Tuple[bool, str]:
        exists = bool(self.items)
        return exists, '' if exists else f'No items found matching {self.pattern!r} pattern'

    def source_item_path(self, item_dir: str) -> str:
        return os.path.join(item_dir, self.add_to_base_item_path) if self.add_to_base_item_path else item_dir

    def destination_item_path(self, destination_dir: str) -> str:
        destination_dir = os.path.join(
            destination_dir, self.add_to_base_item_path
        ) if self.add_to_base_item_path else destination_dir
        os.makedirs(destination_dir, exist_ok=True)
        return destination_dir

    def to_copy_items(self, items_path: str) -> list:
        return [
            entry for entry in filter(
                lambda e: re.findall(self.pattern, e.name), os.scandir(items_path)
            )
        ]

    def size(self, item_path: str) -> int:
        return sum(item.size(item_path) for item in self.items)

    def to_be_copied_checks(self, item_path: str) -> Tuple[bool, Optional[dict]]:
        item_check_report = {}
        for item in self.items:
            to_copy, error = item.to_be_copied_checks(os.path.join(item_path, item.name))
            if not to_copy:
                item_check_report[item.name] = error
                self.to_skip_items.append(item)

        return len(self.items) != len(self.to_skip_items), item_check_report

    def copy_impl(self, item_path: str, destination_path: str) -> list:
        copied_items = []
        for item in filter(lambda i: i not in self.to_skip_items, self.items):
            copied_items.extend(item.copy_impl(
                item.source_item_path(item_path), item.destination_item_path(destination_path)
            ))
            item.post_copy_hook(item.destination_item_path(destination_path))
        return copied_items


class DirectoryPattern(Pattern):

    def __init__(
        self, name: str, max_size: Optional[int] = None, truncate_files: Optional[bool] = True, pattern: str = '.*',
    ):
        super().__init__(name=pattern, max_size=max_size, truncate_files=truncate_files, add_to_base_item_path=name)

    @property
    def report_name_key(self):
        if self.add_to_base_item_path:
            return self.add_to_base_item_path if self.name == '.*' else f'{self.add_to_base_item_path}/{self.name}'
        else:
            return self.name
