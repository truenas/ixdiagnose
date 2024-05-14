import os
import pathlib
import shutil

from ixdiagnose.utils.io import truncate_file
from typing import Optional, Tuple

from .base import Item


class File(Item):

    def __init__(self, name: str, max_size: Optional[int] = None, truncate: Optional[bool] = True):
        super().__init__(name, max_size)
        self.truncate: bool = truncate

    def size(self, item_path: str) -> int:
        try:
            return pathlib.Path(item_path).lstat().st_size
        except Exception:
            return 0

    def copy_impl(self, item_path: str, destination_path: str) -> list:
        try:
            shutil.copy2(item_path, destination_path)
            return [item_path]
        except Exception:
            return []

    def to_be_copied_checks(self, item_path: str) -> Tuple[bool, Optional[str]]:
        to_copy, error = (True, None) if os.path.isfile(item_path) else (False, f'{item_path!r} is not a file')
        if to_copy and not self.truncate:
            return self.size_check(item_path)
        return to_copy, error

    def post_copy_hook(self, destination_path: str):
        if self.max_size is None:
            return

        if self.truncate:
            truncate_file(destination_path, self.max_size)
