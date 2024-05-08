import contextlib
import os
import shutil

from ixdiagnose.utils.io import truncate_file
from typing import Optional, Tuple

from .base import Item


class File(Item):

    def __init__(self, name: str, max_size: Optional[int] = None, truncate: Optional[bool] = True):
        super().__init__(name, max_size)
        self.truncate: bool = truncate
        self.file_descriptor: Optional[int] = None

    def initialize_context(self, item_path: str):
        self.file_descriptor = os.open(item_path, os.O_RDONLY | os.O_NOFOLLOW)

    def size(self, item_path: str) -> int:
        if not self.file_descriptor:
            return os.lstat(item_path).st_size

        return os.fstat(self.file_descriptor).st_size

    def copy_impl(self, item_path: str, destination_path: str) -> list:
        if must_close := self.file_descriptor is None:
            self.initialize_context(item_path)

        try:
            shutil.copy2(self.get_fd_path(), destination_path)
        finally:
            if must_close:
                self.close_descriptor()

        return [item_path]

    def get_fd_path(self) -> str:
        return os.path.join('/proc/self/fd', str(self.file_descriptor))

    def to_be_copied_checks(self, item_path: str) -> Tuple[bool, Optional[str]]:
        to_copy, error = (True, None) if os.path.isfile(item_path) else (False, f'{item_path!r} is not a file')
        if to_copy and not self.truncate:
            return self.size_check(item_path)
        return to_copy, error

    def close_descriptor(self):
        if self.file_descriptor:
            with contextlib.suppress(OSError):
                os.close(self.file_descriptor)
                self.file_descriptor = None

    def __del__(self):
        self.close_descriptor()

    def post_copy_hook(self, destination_path: str):
        self.close_descriptor()
        if self.max_size is None:
            return

        if self.truncate:
            truncate_file(destination_path, self.max_size)
