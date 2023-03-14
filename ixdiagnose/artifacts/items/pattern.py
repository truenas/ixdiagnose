import os
import re

from typing import List, Optional, Tuple

from .base import Item
from .directory import Directory
from .file import File


class Pattern(Item):

    def __init__(self, name: str, max_size: Optional[int] = None):
        super().__init__(name, max_size)
        self.pattern: str = self.name
        self.items: List[Item] = []

    def initialize_context(self, item_path: str) -> None:
        for entry in self.to_copy_items(item_path):
            self.items.append(
                Directory(entry) if os.path.isdir(os.path.join(item_path, entry)) else File(entry)
            )

    def exists(self, item_path: str) -> Tuple[bool, str]:
        exists = bool(self.items)
        return exists, '' if exists else f'No items found matching {self.pattern!r} pattern'

    def source_item_path(self, item_dir: str) -> str:
        return item_dir

    def destination_item_path(self, destination_dir: str) -> str:
        return destination_dir

    def to_copy_items(self, items_path: str) -> list:
        return [entry for entry in filter(lambda e: re.findall(self.pattern, e), os.listdir(items_path))]

    def size(self, item_path: str) -> int:
        return sum(item.size(item_path) for item in self.items)

    def to_be_copied_checks(self, item_path: str) -> Tuple[bool, Optional[str]]:
        items_checks = list(zip(*[i.to_be_copied_checks(os.path.join(item_path, i.name)) for i in self.items]))
        return all(items_checks[0] or [False]), '\n'.join(filter(bool, items_checks[1])) or None

    def copy_impl(self, item_path: str, destination_path: str) -> list:
        copied_items = []
        for item in self.items:
            copied_items.extend(item.copy_impl(
                item.source_item_path(item_path), item.destination_item_path(destination_path)
            ))
        return copied_items
