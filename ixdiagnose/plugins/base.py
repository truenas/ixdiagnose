import json
import os
import time

from typing import List, Union

from ixdiagnose.utils.paths import get_plugin_base_dir

from .metrics_base import CmdMetric, MiddlewareClientMetric


class Plugin:

    metrics: List[Union[CmdMetric, MiddlewareClientMetric]] = []
    name: str = NotImplementedError

    def __init__(self):
        self.debug_report: dict = {}

    @property
    def output_dir(self) -> str:
        return os.path.join(get_plugin_base_dir(), self.name)

    def execute_metrics(self) -> None:
        os.makedirs(self.output_dir, exist_ok=True)
        for metric in self.metrics:
            metric_report = {}
            metric_error = None
            start_time = time.time()
            try:
                metric_report = metric.execute()  # execution mechanism TBD
            except Exception as exc:
                metric_error = str(exc)

            # Before doing anything else, let's get execution time of the metric
            execution_time = time.time() - start_time
            if metric_output := metric_report.pop('output', None):
                with open(metric.output_file_path(self.output_dir), 'w') as f:
                    f.write(metric_output)

            # Expected metric report structure
            # [
            #   "stats": [
            #       {"description": "System Sensors", "error": None},
            #       {"description": "System PCI devices", "error": "X command returned with non safe exit code"},
            #   ]
            # ]

            self.debug_report[metric.name] += {
                'execution_time': execution_time,
                'metric_report': metric_report,
                'metric_execution_error': metric_error,
            }

    def write_debug_report(self):
        with open(self.output_dir, 'report.json') as f:
            f.write(json.dumps(self.debug_report, indent=4))
