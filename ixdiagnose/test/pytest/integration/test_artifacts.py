import contextlib
import os
import shutil

from ixdiagnose.artifact import artifact_factory, gather_artifacts as gather_artifacts_impl
from ixdiagnose.config import conf


@contextlib.contextmanager
def gather_artifacts():
    conf.debug_path = '/tmp/ixdiagnose'
    os.makedirs(conf.debug_path, exist_ok=True)

    try:
        gather_artifacts_impl()
        yield os.path.join(conf.debug_path, 'debug/artifacts')
    finally:
        shutil.rmtree(conf.debug_path, ignore_errors=True)


def get_artifacts_dirs(base_artifact_dir) -> list:
    return [
        os.path.join(base_artifact_dir, i) for i in os.listdir(base_artifact_dir)
        if os.path.isdir(os.path.join(base_artifact_dir, i))
    ]


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
