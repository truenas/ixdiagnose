import os
import re

from typing import Optional

from .base import Artifact
from .items import Pattern


RE_CORE_NAME = re.compile(r'^core\.(.+?)\..+')


class CorePattern(Pattern):

    def __init__(self, max_size: Optional[int] = None):
        super().__init__(r'^core\..+', max_size, truncate_files=False)

    def to_copy_items(self, items_path: str) -> list:
        items = {}
        for entry in filter(
            lambda e: re.findall(self.pattern, e) and RE_CORE_NAME.findall(e),
            sorted(os.listdir(items_path))
        ):
            core_name = RE_CORE_NAME.findall(entry)[0]
            items[core_name] = entry

        return list(items.values())


class CoreDumps(Artifact):
    base_dir = '/var/db/system/cores'
    name = 'cores'
    items = [
        CorePattern(max_size=10 * 1024 * 1024),  # limiting it to 10 mb per core for now
    ]
