import os
import time
import traceback

from ixdiagnose.utils.formatter import dumps
from ixdiagnose.utils.paths import get_artifacts_base_dir


class Artifact:

    name: str = NotImplementedError

    def __init__(self):
        self.debug_report: dict = {}

    @property
    def output_dir(self) -> str:
        return os.path.join(get_artifacts_base_dir(), self.name)

    def write_debug_report(self) -> None:
        with open(os.path.join(self.output_dir, 'report.json'), 'w') as f:
            f.write(dumps(self.debug_report))

    def gather(self) -> dict:
        start_time = time.time()
        os.makedirs(self.output_dir, exist_ok=True)
        error = tb = None
        try:
            self.gather_impl()
            self.write_debug_report()
        except Exception as exception:
            error = str(exception)
            tb = traceback.format_exc()

        return {
            'execution_time': time.time() - start_time,
            'execution_error': error,
            'execution_traceback': tb,
        }

    def gather_impl(self) -> None:
        raise NotImplementedError()
