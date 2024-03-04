import contextlib
import os
import tempfile

from ixdiagnose.artifacts.base import Artifact
from ixdiagnose.artifacts.items import DirectoryPattern


class TestDirectoryPattern(Artifact):
    name = 'test_dir_pattern'
    individual_item_max_size_limit = 1024

    def __init__(self, temp_debug_dir):
        super().__init__()
        self.debug_dir = temp_debug_dir

    @property
    def output_dir(self) -> str:
        return self.debug_dir


def create_file_having_size(file_path: str, file_size: int):
    with open(file_path, 'wb') as f:
        f.write(os.urandom(file_size))


@contextlib.contextmanager
def create_items():
    with tempfile.TemporaryDirectory() as tmp_dir:
        source_dir = os.path.join(tmp_dir, 'source')
        dest_dir = os.path.join(tmp_dir, 'dest')
        os.makedirs(source_dir)
        all_items = []

        for test_dir in ['dir1', 'dir2']:
            dir_path = os.path.join(source_dir, test_dir)
            os.mkdir(dir_path)
            all_items.append(dir_path)

            file_path = os.path.join(dir_path, 'file')
            with open(file_path, 'w'):
                pass
            all_items.append(file_path)

        yield source_dir, dest_dir, all_items


def test_directory_pattern_size_check():
    with create_items() as (source_dir, dest_dir, all_items):
        create_file_having_size(os.path.join(source_dir, 'dir2/file'), 2048)
        dest_items = [item.replace(source_dir, dest_dir) for item in all_items]

        TestDirectoryPattern.base_dir = source_dir
        TestDirectoryPattern.items = [DirectoryPattern('dir1'), DirectoryPattern('dir2')]
        artifact = TestDirectoryPattern(dest_dir)
        artifact.gather_impl()

        for item in [i for i in dest_items]:
            assert os.path.exists(item) is True
