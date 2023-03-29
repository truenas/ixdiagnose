import os

from distutils.dir_util import copy_tree
from pathlib import Path
from typing import Optional, Tuple

from .base import Item


def get_directory_size(directory: str) -> int:
    total = 0
    try:
        with os.scandir(directory) as it:
            for entry in it:
                if entry.is_symlink():
                    continue
                if entry.is_file():
                    total += entry.stat().st_size
                elif entry.is_dir():
                    try:
                        total += get_directory_size(entry.path)
                    except FileNotFoundError:
                        pass
    except NotADirectoryError:
        return os.path.getsize(directory)
    except PermissionError:
        # if for whatever reason we can't open the folder, return 0
        return 0
    return total


class Directory(Item):

    def to_be_copied_checks(self, item_path: str) -> Tuple[bool, Optional[str]]:
        to_copy, error = (True, None) if os.path.isdir(item_path) else (False, f'{item_path!r} is not a directory')
        if to_copy:
            return self.size_check(item_path)
        return to_copy, error

    def size(self, item_path: str) -> int:
        return get_directory_size(item_path)

    def copy_impl(self, item_path: str, destination_path: str) -> list:
        return copy_tree(item_path, destination_path)
