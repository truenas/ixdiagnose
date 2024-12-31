import contextlib
import fnmatch
import json
import os

from ixdiagnose.utils.command import Command
from ixdiagnose.utils.middleware import MiddlewareCommand
from ixdiagnose.utils.run import run

from .base import Plugin
from .metrics import CommandMetric, FileMetric, MiddlewareClientMetric, PythonMetric


def get_ds_list() -> list:
    ds_list = []
    file_path = '/conf/truenas_root_ds.json'

    with contextlib.suppress(FileNotFoundError, json.JSONDecodeError):
        with open(file_path, 'r') as file:
            data = json.load(file)

        for entry in data:
            if entry.get('fhs_entry', {}).get('snap') and entry.get('ds'):
                ds_list.append(entry['ds'])

    return ds_list


def get_root_ds(client: None, resource_type: str) -> dict:
    report = {
        'developer_mode_enabled': None,
        'error': None,
    }
    error_str = 'Failed to retrieve root dataset information: '
    cp = run(['zfs', 'get', '-o', 'name', '-H', 'name', '/'], check=False)
    if cp.returncode:
        report['error'] = f'{error_str}{cp.stderr}'
        return report

    ds = cp.stdout.strip()

    cp = run(['zfs', 'get', '-H', 'truenas:developer', ds], check=False)
    if cp.returncode:
        report['error'] = f'{error_str}{cp.stderr}'
        return report

    output = cp.stdout.split()
    if output[-2] == 'on':
        report['developer_mode_enabled'] = True
    else:
        report['developer_mode_enabled'] = False

    return report


class UsrPostprocess:
    def __init__(self):
        self.is_enterprise = None

    def __call__(self, execution_context, lines: str) -> str:
        if self.is_enterprise is None:
            self.is_enterprise = execution_context['middleware_client'].call('system.is_enterprise')

        if self.is_enterprise:
            return lines

        result = []
        for line in lines.splitlines():
            try:
                filename = line.split(maxsplit=1)[1].strip()
            except IndexError:
                pass
            else:
                if can_be_modified(filename):
                    continue

            result.append(line)

        return "\n".join(result)


def can_be_modified(filename: str) -> bool:
    patterns = (
        # Modified by `middlewared.utils.rootfs.ReadonlyRootfsManager`
        "/usr/bin/apt",
        "/usr/bin/apt-config",
        "/usr/bin/apt-key",
        "/usr/bin/dpkg",
        "/usr/local/bin/apt",
        "/usr/local/bin/apt-config",
        "/usr/local/bin/apt-key",
        "/usr/local/bin/dpkg",
    )
    return any(should_exclude(filename, pattern) for pattern in patterns)


def should_exclude(filename: str, pattern: str) -> bool:
    if fnmatch.fnmatch(filename, pattern):
        return True

    if os.path.commonprefix((f"{filename}/", pattern)) == f"{filename}/":
        return True

    return False


class SystemState(Plugin):
    name = 'system_state'
    metrics = [
        CommandMetric(f'{ds.split("/")[-1]}_dataset_diff', [
            Command(
                ['zfs', 'diff', f'{ds}@pristine'],
                f'changes of {ds} dataset',
                serializable=False,
                postprocess=UsrPostprocess() if ds.split('/')[-1] == 'usr' else None,
            )],
        )
        for ds in get_ds_list()
    ] + [
        FileMetric('root_dataset_configuration', '/conf/truenas_root_ds.json', extension='.json'),
        MiddlewareClientMetric('bootenvs', [MiddlewareCommand('bootenv.query')]),
        PythonMetric('developer_mode', get_root_ds),
    ]
