import os
import pathlib
import shutil

from ixdiagnose.utils.io import truncate_file
from typing import Optional, Tuple

from .base import Item


def get_file_size(file_path: str) -> int:
    return pathlib.Path(file_path).lstat().st_size


class File(Item):
    # TODO: Allow regex matching

    def __init__(self, name: str, max_size: Optional[int] = None, truncate: Optional[bool] = True):
        super().__init__(name, max_size)
        self.truncate: bool = truncate

    def size(self, item_path: str) -> int:
        return get_file_size(item_path)

    def copy_impl(self, item_path: str, destination_path: str) -> list:
        shutil.copy2(item_path, destination_path)
        return [item_path]

    def to_be_copied_checks(self, item_path: str) -> Tuple[bool, Optional[str]]:
        to_copy, error = (True, None) if os.path.isfile(item_path) else (False, f'{item_path!r} is not a file')
        if to_copy and not self.truncate:
            return self.size_check(item_path)
        return to_copy, error

    def post_copy_hook(self, destination_path: str):
        if self.max_size is None:
            return

        truncate_file(destination_path, self.max_size)
