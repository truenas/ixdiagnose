import os
import traceback

from .artifacts.factory import artifact_factory
from .utils.formatter import dumps
from .utils.paths import get_artifacts_base_dir


def gather_artifacts() -> None:
    os.makedirs(get_artifacts_base_dir(), exist_ok=True)
    artifacts_report = {}
    for artifact_name, artifact in artifact_factory.get_artifacts().items():
        try:
            report = artifact.gather()
        except Exception as exc:
            report = {
                'execution_time': None,
                'execution_error': str(exc),
                'execution_traceback': traceback.format_exc(),
            }
        artifacts_report[artifact_name] = report

    with open(os.path.join(get_artifacts_base_dir(), 'report.json'), 'w') as f:
        f.write(dumps(artifacts_report))
