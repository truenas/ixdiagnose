import os
import traceback

from .artifacts.factory import artifact_factory
from .config import conf
from .event import send_event
from .utils.formatter import dumps
from .utils.paths import get_artifacts_base_dir


def gather_artifacts(percentage: int = 0, total_percentage: int = 100) -> None:
    os.makedirs(get_artifacts_base_dir(), exist_ok=True)
    to_execute_artifacts = {
        artifact_name: artifact for artifact_name, artifact in artifact_factory.get_items().items()
        if artifact_name not in conf.exclude_artifacts
    }
    artifacts_report = {}
    artifact_percentage = total_percentage / (len(to_execute_artifacts) or 1)  # We want to handle this quietly
    for artifact_name, artifact in to_execute_artifacts.items():

        try:
            report = artifact.gather()
        except Exception as exc:
            report = {
                'execution_time': None,
                'execution_error': str(exc),
                'execution_traceback': traceback.format_exc(),
            }

        artifacts_report[artifact_name] = report
        percentage += artifact_percentage
        send_event(int(percentage + 0.5), f'Gathered artifact {artifact_name!r}')

    with open(os.path.join(get_artifacts_base_dir(), 'report.json'), 'w') as f:
        f.write(dumps(artifacts_report))
