import os
import re

from collections import defaultdict
from systemd import journal
from typing import Optional, Tuple

from .base import Artifact
from .items import Pattern


RE_CORE_NAME = re.compile(r'^core\.(.+?)\..+')


class CorePattern(Pattern):

    MAX_ARTIFACT_SIZE: int = 30 * 1024 * 1024

    def __init__(self, max_size: Optional[int] = None):
        super().__init__(r'^core\..+', max_size, truncate_files=False)

    def to_copy_items(self, items_path: str) -> list:
        dumps = defaultdict(dict)
        with journal.Reader() as reader:
            reader.add_match(CODE_FUNC='submit_coredump')
            for core in filter(
                lambda c: all(k in c for k in ('COREDUMP_TIMESTAMP', 'COREDUMP_EXE', 'COREDUMP_FILENAME')),
                reader
            ):
                if not isinstance(core['COREDUMP_FILENAME'], str) or not os.path.exists(core['COREDUMP_FILENAME']):
                    continue
                dumps[core['COREDUMP_EXE']][core['COREDUMP_TIMESTAMP']] = core

        return [
            os.path.basename(dumps[exe][max(dumps[exe])]['COREDUMP_FILENAME'])
            for exe in dumps
        ]

    def to_be_copied_checks(self, item_path: str) -> Tuple[bool, Optional[dict]]:
        to_copy, report = super().to_be_copied_checks(item_path)
        if not to_copy:
            return to_copy, report

        total_size = 0
        for item in filter(lambda i: i not in self.to_skip_items, self.items):
            item_size = item.size(item_path)
            if total_size + item_size > self.MAX_ARTIFACT_SIZE:
                self.to_skip_items.append(item)
                report[item.name] = f'Skipped due to {item_size / 1024 / 1024!r} MB exceeding ' \
                                    f'coredump artifact {self.MAX_ARTIFACT_SIZE / 1024 / 1024!r} MB max size'
            else:
                total_size += item_size

        return len(self.items) != len(self.to_skip_items), report


class CoreDumps(Artifact):
    base_dir = '/var/db/system/cores'
    name = 'cores'
    items = [
        CorePattern(max_size=10 * 1024 * 1024),  # limiting it to 10 mb per core for now
    ]
