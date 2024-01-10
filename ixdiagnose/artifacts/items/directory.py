import functools
import os
import shutil

from pathlib import Path
from typing import List, Optional, Tuple

from .base import Item


def get_directory_size(directory: str) -> int:
    return sum(i.lstat().st_size for i in Path(directory).rglob('*')) + Path(directory).stat().st_size


def copy2(copied_files: list, src: str, dst: str) -> str:
    copied_files.append(src)
    return shutil.copy2(src, dst)


def ignore_func(to_ignore: list, src: str, names: list) -> list:
    if ignore_items := [os.path.basename(i) for i in to_ignore if os.path.dirname(i) == src]:
        return ignore_items
    return []


class Directory(Item):

    def __init__(self, name: str, max_size: Optional[int] = None, ignore_items: Optional[List] = None):
        super().__init__(name, max_size)
        self.ignore_items: Optional[List[str]] = ignore_items

    def to_be_copied_checks(self, item_path: str) -> Tuple[bool, Optional[str]]:
        to_copy, error = (True, None) if os.path.isdir(item_path) else (False, f'{item_path!r} is not a directory')
        if to_copy:
            return self.size_check(item_path)
        return to_copy, error

    def size(self, item_path: str) -> int:
        return get_directory_size(item_path)

    def copy_impl(self, item_path: str, destination_path: str) -> list:
        copied_items = []
        shutil.copytree(
            item_path, destination_path, copy_function=functools.partial(copy2, copied_items),
            ignore=functools.partial(ignore_func, self.ignore_items)
        )
        return copied_items
