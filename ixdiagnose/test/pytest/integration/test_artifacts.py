import contextlib
import json
import os
import shutil

from ixdiagnose.artifact import artifact_factory, gather_artifacts as gather_artifacts_impl
from ixdiagnose.config import conf
from jsonschema import validate

from .utils import BASE_REPORT_SCHEMA


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
            assert {item.name for item in artifact.items} == set(artifact_report)

            for item_report in artifact_report.values():
                validate(item_report, ARTIFACT_REPORT_SCHEMA)
