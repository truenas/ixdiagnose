import contextlib
import json
import os
import pytest
import shutil
import tempfile

from ixdiagnose.artifacts.items import Directory
from ixdiagnose.artifact import artifact_factory, gather_artifacts as gather_artifacts_impl
from ixdiagnose.event import event_callbacks
from ixdiagnose.config import conf
from ixdiagnose.utils.paths import get_artifacts_base_dir
from jsonschema import validate

from .utils import BASE_REPORT_SCHEMA

PROGRESS_DESCRIPTIONS = []
PROGRESS_TRACK = []

ARTIFACT_REPORT_SCHEMA = {
    'type': 'object',
    'properties': {
        'execution_time': {'type': 'number'},
        'item_report': {
            'anyOf': [
                {
                    'type': 'object',
                    'properties': {
                        'error': {'type': ['string', 'null', 'object']},
                        'traceback': {'type': ['string', 'null']},
                        'copied_items': {'type': 'array'},
                    },
                },
                {'type': 'null'}
            ]
        },
        'item_execution_error': {'type': ['string', 'null']},
        'item_execution_traceback': {'type': ['string', 'null']},
    },
}


@contextlib.contextmanager
def create_items():
    with tempfile.TemporaryDirectory() as tmp_dir:
        source_dir = os.path.join(tmp_dir, 'source')
        dest_dir = os.path.join(tmp_dir, 'dest')
        os.makedirs(source_dir)
        all_items = []

        for test_dir in ['dir1', 'dir2', 'dir1/dir3']:
            dir_path = os.path.join(source_dir, test_dir)
            os.mkdir(dir_path)
            all_items.append(dir_path)

            file_path = os.path.join(dir_path, 'file')
            with open(file_path, 'w'):
                pass
            all_items.append(file_path)

        to_ignore = ['dir2', 'dir1/file', 'dir1/dir3/file']

        yield source_dir, dest_dir, all_items, to_ignore


@contextlib.contextmanager
def create_test_file_having_size(file_path: str, file_size: int):
    try:
        with open(file_path, 'wb') as f:
            f.write(os.urandom(file_size))

        yield os.path.basename(file_path)
    finally:
        os.remove(file_path)


@contextlib.contextmanager
def gather_artifacts(base_percentage=0, total_percentage=100):
    conf.debug_path = '/tmp/ixdiagnose'
    os.makedirs(conf.debug_path, exist_ok=True)

    try:
        gather_artifacts_impl(percentage=base_percentage, total_percentage=total_percentage)
        yield get_artifacts_base_dir()
    finally:
        event_callbacks.clear()
        shutil.rmtree(conf.debug_path, ignore_errors=True)


def get_artifacts_dirs(base_artifact_dir) -> list:
    return [
        i.path for i in os.scandir(base_artifact_dir) if i.is_dir()
    ]


def event_callback(progresss, text):
    PROGRESS_TRACK.append(progresss)
    PROGRESS_DESCRIPTIONS.append(text)


def test_base_report_generation():
    with gather_artifacts() as artifacts_dir:
        assert os.path.exists(os.path.join(artifacts_dir, 'report.json')) is True


def test_artifacts_directories_report_generation():
    with gather_artifacts() as artifacts_dir:
        artifacts_dirs = get_artifacts_dirs(artifacts_dir)
        assert len(artifacts_dirs) > 0
        for artifact_dir in artifacts_dirs:
            assert os.path.exists(os.path.join(artifact_dir, 'report.json')) is True


def test_artifacts_count():
    with gather_artifacts() as artifacts_dir:
        artifacts_dirs = get_artifacts_dirs(artifacts_dir)
        assert len(artifacts_dirs) == len(artifact_factory.get_items())


def test_report_schema():
    artifacts = artifact_factory.get_items()
    with gather_artifacts() as artifacts_dir:
        with open(os.path.join(artifacts_dir, 'report.json')) as f:
            base_report = json.loads(f.read())

        assert set(artifacts) == set(base_report)

        for artifact_name, artifact_report in base_report.items():
            validate(base_report[artifact_name], BASE_REPORT_SCHEMA)

        for artifact_dir in get_artifacts_dirs(artifacts_dir):
            with open(os.path.join(artifact_dir, 'report.json')) as f:
                artifact_report = json.loads(f.read())

            artifact = artifacts[os.path.basename(artifact_dir)]
            assert {item.report_name_key for item in artifact.items} == set(artifact_report)

            for item_report in artifact_report.values():
                validate(item_report, ARTIFACT_REPORT_SCHEMA)


@pytest.mark.parametrize('file_size,file_truncated', [
    (5 * 1024 * 1024, False),
    (2 * 1024 * 1024, False),
    (12 * 1024 * 1024, True),
    (15 * 1024 * 1024, True),
])
def test_truncation_of_file(file_size, file_truncated):
    with create_test_file_having_size('/var/log/failover.log', file_size) as file_name:
        with gather_artifacts() as artifacts_dir:
            if file_truncated:
                assert os.path.getsize(os.path.join(artifacts_dir, 'logs', file_name)) < file_size
            else:
                assert os.path.getsize(os.path.join(artifacts_dir, 'logs', file_name)) == file_size


def test_artifact_event_progress_count():
    event_callbacks.register(callback=event_callback)
    with gather_artifacts():
        assert len(artifact_factory.get_items()) + 1 == len(PROGRESS_DESCRIPTIONS) == len(PROGRESS_TRACK)


def test_directory_copy():
    with create_items() as (source_dir, dest_dir, all_items, to_ignore):
        directory_obj = Directory('test')
        directory_obj.copy_impl(source_dir, dest_dir)

        for item in all_items:
            dest_item = os.path.join(dest_dir, os.path.relpath(item, source_dir))
            assert os.path.exists(dest_item) is True


def test_ignore_items():
    with create_items() as (source_dir, dest_dir, all_items, to_ignore):
        ignore_items = [os.path.join(source_dir, item) for item in to_ignore]

        directory_obj = Directory(name='test', ignore_items=ignore_items)
        directory_obj.copy_impl(source_dir, dest_dir)

        # Assert ignored items not in destination
        for dest_item in to_ignore:
            assert os.path.exists(os.path.join(dest_dir, dest_item)) is False

        # Assert not ignored items in destination
        for dest_item in [i for i in all_items if i not in ignore_items]:
            assert os.path.exists(os.path.join(dest_dir, dest_item)) is True

        # Assert all items in source
        for source_item in all_items:
            assert os.path.exists(source_item) is True
