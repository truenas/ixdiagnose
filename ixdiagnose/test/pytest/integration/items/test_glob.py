import contextlib
import os
import tempfile

from ixdiagnose.artifacts.items import Glob
from ixdiagnose.artifacts.base import Artifact


DATA = {
    'files': [
        'test_file1',
        'test_file2',
        'test_file3',
    ],
    'dirs': [
        'test_dir1',
        'test_dir2',
        'test_dir3',
    ],
}
DIR_TEST_FILE = 'test_dir_file'


class TestGlob(Artifact):
    base_dir = '/tmp'
    name = 'test_glob'
    items = []

    def __init__(self, temp_debug_dir):
        super().__init__()
        self.debug_dir = temp_debug_dir

    @property
    def output_dir(self) -> str:
        return os.path.join(self.debug_dir, self.name)


def sort_list(list_: list):
    list_.sort()
    return list_


def validate_report_data(source_path, data, report, errors=None):
    errors = errors or {}
    base_dict = {
        'execution_time': 0,
        'item_execution_error': None,
        'item_execution_traceback': None,
        'item_report': {
            'traceback': None,
            'copied_items': []
        }
    }
    assert report[source_path]['execution_time'] != 0
    base_dict['execution_time'] = report[source_path]['execution_time']
    report[source_path]['item_report']['copied_items'].sort()
    report_errors = report[source_path]['item_report'].pop('error')
    base_dict['item_report']['copied_items'] = sort_list(data)
    assert report == {source_path: base_dict}
    if errors:
        assert all((errors.get(k) == v for k, v in report_errors.items())) is True

    return True


@contextlib.contextmanager
def glob_data():
    with tempfile.TemporaryDirectory() as destination_dir:
        with tempfile.TemporaryDirectory() as source_dir:
            data = {'source_dir': source_dir, 'destination_dir': destination_dir, 'dirs': [], 'files': [], 'all': []}
            for test_dir in DATA['dirs']:
                dir_path = os.path.join(source_dir, test_dir)
                os.mkdir(dir_path)
                with open(os.path.join(dir_path, DIR_TEST_FILE), 'w') as f:
                    f.write('testing  max size ' * 30)
                data['dirs'].append(dir_path)
                data['all'].append(os.path.join(dir_path, DIR_TEST_FILE))
            for test_file in DATA['files']:
                file_path = os.path.join(source_dir, test_file)
                with open(file_path, 'w') as f:
                    f.write('testing  max size ' * 30)
                data['files'].append(file_path)
                data['all'].append(file_path)
            yield data


def test_glob_item_artifact():
    with glob_data() as data:
        destination_dir = data.pop('destination_dir')
        source_dir = f'{data.pop("source_dir")}/*'
        TestGlob.items = [Glob(source_dir)]
        glob_artifact = TestGlob(destination_dir)
        glob_artifact.gather_impl()

        assert sort_list(glob_artifact.debug_report[source_dir]['item_report']['copied_items']) == sort_list(
            data['all']
        )
        assert all([
            os.path.isfile(os.path.join(os.path.join(destination_dir, TestGlob.name), test_file[1:]))
            for test_file in data['all']
        ]) is True
        assert validate_report_data(source_dir, data['all'], glob_artifact.debug_report) is True


def test_glob_to_skip_items():
    with glob_data() as data:
        destination_dir = data.pop('destination_dir')
        source_dir = f'{data.pop("source_dir")}/*'
        TestGlob.items = [Glob(source_dir, to_skip_items=[data['dirs'][0], data['files'][0]])]
        glob_artifact = TestGlob(destination_dir)
        glob_artifact.gather_impl()

        data['all'].remove(data['files'][0]), data['all'].remove(os.path.join(data['dirs'][0], DIR_TEST_FILE))
        assert sort_list(glob_artifact.debug_report[source_dir]['item_report']['copied_items']) == sort_list(
            data['all']
        )
        assert all([
            os.path.isfile(os.path.join(os.path.join(destination_dir, TestGlob.name), test_file[1:]))
            for test_file in data['all']
        ]) is True
        assert validate_report_data(source_dir, data['all'], glob_artifact.debug_report) is True


def test_glob_item_readonly_validation():
    with glob_data() as data:
        destination_dir = data.pop('destination_dir')
        source_dir = f'{data.pop("source_dir")}/*'
        skip_dir, skip_file = data['dirs'][0], data['files'][0]
        for skip_item in (skip_file, skip_dir):
            os.chmod(skip_item, 0o333)

        TestGlob.items = [Glob(source_dir)]
        glob_artifact = TestGlob(destination_dir)
        glob_artifact.gather_impl()

        data['all'].remove(data['files'][0]), data['all'].remove(os.path.join(skip_dir, DIR_TEST_FILE))
        assert sort_list(glob_artifact.debug_report[source_dir]['item_report']['copied_items']) == sort_list(
            data['all']
        )
        assert all([
            os.path.isfile(os.path.join(os.path.join(destination_dir, TestGlob.name), test_file[1:]))
            for test_file in data['all']
        ])
        assert all([
            os.path.isfile(os.path.isfile(os.path.join(os.path.join(destination_dir, TestGlob.name), skip_dir[1:]))),
            os.path.isfile(os.path.join(os.path.join(destination_dir, TestGlob.name), skip_file[1:]))
        ]) is False
        assert validate_report_data(
            source_dir, data['all'], glob_artifact.debug_report,
            errors={file_name: f"'{file_name}' is not readable" for file_name in (skip_dir, skip_file)}
        ) is True


def test_glob_item_maxsize_validation():
    with glob_data() as data:
        destination_dir = data.pop('destination_dir')
        source_dir = f'{data.pop("source_dir")}/*'
        TestGlob.items = [Glob(source_dir, max_size=10)]
        glob_artifact = TestGlob(destination_dir)
        glob_artifact.gather_impl()

        assert sort_list(glob_artifact.debug_report[source_dir]['item_report']['copied_items']) == []
        assert not all([
            os.path.isfile(os.path.join(os.path.join(destination_dir, TestGlob.name), test_file[1:]))
            for test_file in data['all']
        ])
        assert validate_report_data(
            source_dir, [], glob_artifact.debug_report,
            errors={
                file_name: f"'{file_name}' exceeds specified 10 size" for file_name in [*data['dirs'], *data['files']]
            }
        ) is True
