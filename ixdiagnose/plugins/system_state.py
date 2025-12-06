import contextlib
import json

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


class SystemState(Plugin):
    name = 'system_state'
    metrics = [
        CommandMetric(f'{ds.split("/")[-1]}_dataset_diff', [
            Command(
                ['zfs', 'diff', f'{ds}@pristine'],
                f'changes of {ds} dataset', serializable=False,
            )],
        )
        for ds in get_ds_list()
    ] + [
        FileMetric('root_dataset_configuration', '/conf/truenas_root_ds.json', extension='.json'),
        MiddlewareClientMetric('bootenvs', [MiddlewareCommand('boot.environment.query')]),
        PythonMetric('developer_mode', get_root_ds),
    ]
