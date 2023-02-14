import json
import os

from typing import Any, Dict, List, Tuple

from ixdiagnose.utils.command import Cmd


class Metric:

    def __init__(self, name: str):
        self.name: str = name

    @property
    def output_file_extension(self) -> str:
        return '.json'

    def output_file_path(self, base_dir: str) -> str:
        return os.path.join(base_dir, f'{self.name}{self.output_file_extension}')

    def execute(self) -> Tuple[Any, str]:
        data = self.execute_impl()
        assert isinstance(data, (list, tuple)) and len(data) == 2
        return data

    def execute_impl(self) -> Tuple[Any, str]:
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
            result = json.dumps(cmd_context, indent=4)
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

        return metric_report, self.format_data(cmd_context) if cmd_context else ''


class FileMetric(Metric):

    def __init__(self, name: str, file_path: str):
        super().__init__(name)
        self.file_path: str = file_path

    def execute_impl(self) -> Tuple[Dict, str]:
        report = {
            'error': None, 'description': f'Contents of {self.file_path!r}',
        }
        try:
            with open(self.file_path, 'r') as f:
                output = f.read()
        except FileNotFoundError:
            output = None
            report['error'] = f'{self.file_path!r} file path does not exist'

        return report, output


class MiddlewareClientMetric(Metric):
    api_endpoint: str = NotImplementedError
    api_payload: List = []

    def format_output(self):
        pass

    def execute(self) -> Tuple[Any, str]:
        # {"api_endpoint": "", "api_payload": "", "result": None}
        pass
