import json
import os
import subprocess
import time

from typing import List, Dict, Union


class Cmd:
    safe_returncodes = [0]

    def __init__(self, command, shell=False, serializeable_output=True, safe_returncodes=None):
        self.command = command
        self.shell = shell
        self.serializeable_output = serializeable_output
        self.safe_returncodes = safe_returncodes or self.safe_returncodes

    def execute(self) -> subprocess.CompletedProcess:
        cmd = self.command
        if self.shell and isinstance(self.command, list):
           cmd = " ".join(self.command)
        elif not self.shell and isinstance(self.command, 'str'):
            cmd = self.command.split(" ")

        return subprocess.run(cmd, shell=self.shell)


class Metric:
    name: str = NotImplementedError
    plugin = None

    def __init__(self, plugin) -> None:
        self.plugin = plugin
    
    @property
    def output_file_extension(self):
        return ".json"
    
    @property
    def output_file_path(self):
        return os.path.join(self.plugin.output_dir, f"{self.name}{self.output_file_extension}")

    def format_data(self, context):
        return json.dumps(context, indent=4)

    def execute(self):
       raise NotImplementedError

    def write_output(self, context):
        with open(self.output_file_path, 'w') as file:
            file.write(self.format_data(context))


class CmdMetric(Metric):

    cmds: List[Cmd] = []

    @property
    def serializable(self):
        return all(cmd.serializable for cmd in self.cmds)

    @property
    def output_file_extension(self):
        return ".json" if self.serializable else ".txt"

    def format_data(self, context: list):
        result = [] if self.serializable else ""
        for cmd, proc in context:
            if self.serializable:
                result.append({
                    'key': 3,
                    'output': json.load(proc.stdout.decode())
                })
            else:
                result += f"""
                {proc.stdout.decode()}
                """

    def execute(self):
        cmd_context = []
        for cmd in self.cmds:
            cmd_context.append((cmd, cmd.execute()))

        self.write_output(cmd_context)


class MiddlewareClientMetric(Metric):
    api_endpoint: str = NotImplementedError
    api_payload: List = []

    def format_output(self):
        pass

    def execute(self):
        # {"api_endpoint": "", "api_payload": "", "result": None}
        pass


class Plugin:
    name: str = NotImplementedError
    metrics: Union[CmdMetric, MiddlewareClientMetric] = []
    output_base_dir: str = None
    debug_report = {}

    def __init__(self, output_base_dir: str):
        self.output_base_dir =  output_base_dir

    def on_success(self):
        pass

    def on_failure(self):
        pass

    @property
    def output_dir(self):
        return os.path.join(self.output_base_dir, self.name)

    def execute_metrics(self):
        for metric in self.metrics:
            start_time = time.time()
            metric_report = {}
            metric_error = None
            try:
                metric_report = metric.execute() # execution mechanish TBD
            except Exception as exc:
                metric_error = str(exc)
            
            self.debug_report[metric] += {
                'execution_time': time.time() - start_time,
                'metric_report': metric_report,
                'metric_execution_error': metric_error,
            }

    def write_debug_report(self):
        pass
