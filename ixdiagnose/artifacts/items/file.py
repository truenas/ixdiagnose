import os
import pathlib
import shutil

from typing import Optional, Tuple

from .base import Item


class File(Item):
    # TODO: Allow regex matching

    def size(self, item_path: str) -> int:
        return pathlib.Path(item_path).stat().st_size

    def copy_impl(self, item_path: str, destination_path: str) -> list:
        shutil.copy(item_path, destination_path)
        return [item_path]

    def to_be_copied_checks(self, item_path: str) -> Tuple[bool, Optional[str]]:
        return (True, None) if os.path.isfile(item_path) else (False, f'{item_path!r} is not a file')
