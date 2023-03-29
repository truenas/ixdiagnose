import functools
import os
import shutil

from pathlib import Path
from typing import Optional, Tuple

from .base import Item


def get_directory_size(directory: str) -> int:
    return sum(i.lstat().st_size for i in Path(directory).rglob('*')) + Path(directory).stat().st_size


def copy2(copied_files: list, src: str, dst: str) -> str:
    copied_files.append(src)
    return shutil.copy2(src, dst)


class Directory(Item):

    def to_be_copied_checks(self, item_path: str) -> Tuple[bool, Optional[str]]:
        to_copy, error = (True, None) if os.path.isdir(item_path) else (False, f'{item_path!r} is not a directory')
        if to_copy:
            return self.size_check(item_path)
        return to_copy, error

    def size(self, item_path: str) -> int:
        return get_directory_size(item_path)

    def copy_impl(self, item_path: str, destination_path: str) -> list:
        copied_items = []
        shutil.copytree(item_path, destination_path, copy_function=functools.partial(copy2, copied_items))
        return copied_items
