import os
import time
import traceback

from typing import List

from ixdiagnose.utils.formatter import dumps
from ixdiagnose.utils.middleware import get_middleware_client
from ixdiagnose.utils.paths import get_plugin_base_dir

from .metrics import Metric


class Plugin:

    metrics: List[Metric] = []
    raw_metrics: List[Metric] = []
    serializable_metrics: List[Metric] = []
    name: str = NotImplementedError

    def __init__(self):
        self.debug_report: dict = {}

    @property
    def output_dir(self) -> str:
        return os.path.join(get_plugin_base_dir(), self.name)

    def metrics_to_execute(self):
        return self.metrics + self.raw_metrics

    def execute_metrics(self) -> None:
        os.makedirs(self.output_dir, exist_ok=True)
        context = {
            'middleware_client': None,
            'output_dir': self.output_dir,
        }
        try:
            with get_middleware_client() as client:
                context['middleware_client'] = client
                return self.execute_impl(context)
        except ConnectionError:
            return self.execute_impl(context)

    def execute_impl(self, context: dict) -> None:
        for metric in self.metrics_to_execute():
            metric_report = metric_output = metric_error = metric_execution_traceback = None
            start_time = time.time()
            try:
                metric_report, metric_output = metric.execute(context)  # execution mechanism TBD
            except Exception as exc:
                metric_error = str(exc)
                metric_execution_traceback = traceback.format_exc()

            # Before doing anything else, let's get execution time of the metric
            execution_time = time.time() - start_time
            if metric_output:
                with open(metric.output_file_path(self.output_dir), 'w') as f:
                    f.write(metric_output)

            self.debug_report[metric.name] = {
                'execution_time': execution_time,
                'metric_report': metric_report,
                'metric_execution_error': metric_error,
                'metric_execution_traceback': metric_execution_traceback,
            }

    def write_debug_report(self) -> None:
        with open(os.path.join(self.output_dir, 'report.json'), 'w') as f:
            f.write(dumps(self.debug_report))

    def execute(self) -> dict:
        start_time = time.time()
        plugin_error = plugin_traceback = None
        try:
            self.execute_metrics()
            self.write_debug_report()
        except Exception as exception:
            plugin_error = str(exception)
            plugin_traceback = traceback.format_exc()

        return {
            'execution_time': time.time() - start_time,
            'execution_error': plugin_error,
            'execution_traceback': plugin_traceback,
        }
