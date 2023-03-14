import errno
import os
import re

from distutils.dir_util import mkpath
from distutils.file_util import copy_file
from ixdiagnose.exceptions import CallError
from typing import Optional, Tuple

from .base import Item


def get_directory_size(directory: str) -> int:
    total = 0
    try:
        for entry in os.scandir(directory):
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


def copy_tree(src: str, dst: str, regex_pattern: Optional[str] = None) -> list:
    if not os.path.isdir(src):
        raise CallError(f'{src!r} is not a directory', errno=errno.EINVAL)

    mkpath(dst)

    outputs = []
    for n in filter(lambda name: not regex_pattern or re.findall(regex_pattern, name), os.listdir(src)):
        src_name = os.path.join(src, n)
        dst_name = os.path.join(dst, n)

        if os.path.isdir(src_name):
            outputs.extend(copy_tree(src_name, dst_name, regex_pattern))
        else:
            copy_file(src_name, dst_name)
            outputs.append(src_name)

    return outputs


class Directory(Item):

    def __init__(self, name: str, max_size: Optional[int] = None, regex: Optional[str] = None):
        super().__init__(name, max_size)
        self.regex: Optional[str] = regex

    def to_be_copied_checks(self, item_path: str) -> Tuple[bool, Optional[str]]:
        return (True, None) if os.path.isdir(item_path) else (False, f'{item_path!r} is not a directory')

    def size(self, item_path: str) -> int:
        return get_directory_size(item_path)

    def copy_impl(self, item_path: str, destination_path: str) -> list:
        return copy_tree(item_path, destination_path, self.regex)
