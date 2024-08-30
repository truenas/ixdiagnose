import json
import time

from typing import List, Tuple

from ixdiagnose.plugins.prerequisites.base import Prerequisite
from ixdiagnose.utils.formatter import dumps, loads
from ixdiagnose.utils.command import Command

from .base import Metric


class CommandMetric(Metric):

    def __init__(self, name: str, cmds: List[Command], prerequisites: List[Prerequisite] = None):
        super().__init__(name, prerequisites)
        self.cmds: List[Command] = cmds

        assert type(self.cmds) is list
        assert all(isinstance(cmd, Command) for cmd in self.cmds) is True

    @property
    def serializable(self) -> bool:
        return all(cmd.serializable for cmd in self.cmds)

    @property
    def output_file_extension(self) -> str:
        return '.json' if self.serializable else '.txt'

    def format_data(self, cmd_context: list) -> str:
        if self.serializable:
            result = dumps(cmd_context)
        else:
            result = ''
            for index, entry in enumerate(cmd_context):
                padding = f'\n{"-" * (len(entry["description"]) + 5)}\n'
                result += f'{padding}{index + 1}) {entry["description"]}{padding}\n{entry["result"]}'

        return result

    def execute_impl(self) -> Tuple[List, str]:
        cmd_context = []
        metric_report = []
        for cmd in self.cmds:
            cmd.execution_context = self.execution_context
            start_time = time.time()
            cp = cmd.execute()
            report = {
                'command': cmd.command,
                'error': None,
                'execution_time': time.time() - start_time,
                'description': cmd.description,
                'returncode': cp.returncode,
            }
            metric_report.append(report)

            if cp.returncode not in cmd.safe_returncodes:
                report['error'] = cp.stderr or f'Command returncode {cp.returncode!r} is not marked safe'
                continue

            output = cp.stdout
            if self.serializable:
                try:
                    output = loads(output)
                except json.JSONDecodeError:
                    report['error'] = f'Failed to serialize command output: {output!r}'
                    continue

            cmd_context.append({'description': cmd.description, 'result': output})

        return metric_report, self.format_data(cmd_context) if cmd_context else ''
