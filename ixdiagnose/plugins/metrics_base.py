import json
import os

from typing import Any, Dict, List

from ixdiagnose.utils.command import Cmd


class Metric:

    def __init__(self, name: str):
        self.name: str = name

    @property
    def output_file_extension(self) -> str:
        return '.json'

    def output_file_path(self, base_dir: str) -> str:
        return os.path.join(base_dir, f'{self.name}{self.output_file_extension}')

    def format_data(self, context: Any) -> str:
        return json.dumps(context, indent=4)

    def execute(self) -> Dict:
        raise NotImplementedError


class CmdMetric(Metric):

    def __init__(self, name: str, cmds: List[Cmd]):
        super().__init__(name)
        self.cmds: List[Cmd] = cmds

    @property
    def serializable(self) -> bool:
        return all(cmd.serializeable for cmd in self.cmds)

    @property
    def output_file_extension(self) -> str:
        return '.json' if self.serializable else '.txt'

    def format_data(self, cmd_context: list) -> str:
        if self.serializable:
            result = super().format_data(cmd_context)
        else:
            result = ''
            for index, entry in enumerate(cmd_context):
                padding = f'\n{"-" * (len(entry["description"]) + 5)}\n'
                result += f'{padding}{index + 1}) {entry["description"]}{padding}{entry["result"]}'

        return result

    def execute(self) -> Dict:
        cmd_context = []
        metric_report = []
        for cmd in self.cmds:
            cp = cmd.execute()
            report = {
                'error': None, 'description': cmd.description, 'returncode': cp.returncode,
            }
            metric_report.append(report)

            if cp.returncode not in cmd.safe_returncodes:
                report['error'] = cp.stderr or f'Command returncode {cp.returncode!r} is not marked safe'
                continue

            output = cp.stdout
            if self.serializable:
                try:
                    output = json.loads(output)
                except json.JSONDecodeError:
                    report['error'] = f'Failed to serialize command output: {output!r}'
                    continue

            cmd_context.append({'description': cmd.description, 'result': output})

        return {'stats': metric_report, 'output': self.format_data(cmd_context)}


class MiddlewareClientMetric(Metric):
    api_endpoint: str = NotImplementedError
    api_payload: List = []

    def format_output(self):
        pass

    def execute(self):
        # {"api_endpoint": "", "api_payload": "", "result": None}
        pass
