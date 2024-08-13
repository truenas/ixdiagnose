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


def usr_postprocess(lines: str) -> str:
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
        # nvidia drivers and its dependencies
        "/usr/bin/cpp*",
        "/usr/bin/mesa-overlay-control.py",
        "/usr/bin/nvidia-*",
        "/usr/bin/x86_64-linux-gnu-cpp*",
        "/usr/include/*",
        "/usr/lib64/xorg/modules/*",
        "/usr/lib/cpp",
        "/usr/lib/firmware/nvidia/*",
        "/usr/lib/gcc/*",
        "/usr/lib/libGL*",
        "/usr/lib/modules/*",
        "/usr/lib/modules/*/kernel/drivers/video",
        "/usr/lib/modules/*/kernel/drivers/video/nvidia*",
        "/usr/lib/modules/*/modules.*",
        "/usr/lib/nvidia/*",
        "/usr/lib/systemd/system/nvidia-*",
        "/usr/lib/systemd/system-sleep/nvidia",
        "/usr/lib/x86_64-linux-gnu/gbm/*",
        "/usr/lib/x86_64-linux-gnu/libcuda*",
        "/usr/lib/x86_64-linux-gnu/libEGL*",
        "/usr/lib/x86_64-linux-gnu/libGL*",
        "/usr/lib/x86_64-linux-gnu/libisl*",
        "/usr/lib/x86_64-linux-gnu/libLLVM*",
        "/usr/lib/x86_64-linux-gnu/libmpc*",
        "/usr/lib/x86_64-linux-gnu/libnvcuvid*",
        "/usr/lib/x86_64-linux-gnu/libnvidia*",
        "/usr/lib/x86_64-linux-gnu/libnvoptix*",
        "/usr/lib/x86_64-linux-gnu/libOpenCL*",
        "/usr/lib/x86_64-linux-gnu/libOpenGL*",
        "/usr/lib/x86_64-linux-gnu/libvdpau*",
        "/usr/lib/x86_64-linux-gnu/libVkLayer*",
        "/usr/lib/x86_64-linux-gnu/libvulkan*",
        "/usr/lib/x86_64-linux-gnu/libwayland*",
        "/usr/lib/x86_64-linux-gnu/libX11*",
        "/usr/lib/x86_64-linux-gnu/libxcb*",
        "/usr/lib/x86_64-linux-gnu/libxshmfence.so*",
        "/usr/lib/x86_64-linux-gnu/pkgconfig",
        "/usr/lib/x86_64-linux-gnu/vdpau/*",
        "/usr/share/applications/nvidia-settings.desktop",
        "/usr/share/bug/mesa-vulkan-drivers/*",
        "/usr/share/doc/*",
        "/usr/share/drirc.d/*",
        "/usr/share/egl/*",
        "/usr/share/gdb/*",
        "/usr/share/glvnd/*",
        "/usr/share/icons/hicolor/*",
        "/usr/share/keyrings/*",
        "/usr/share/lintian/overrides/*",
        "/usr/share/locale/*",
        "/usr/share/man/man*",
        "/usr/share/nvidia/*",
        "/usr/share/pkgconfig",
        "/usr/share/vulkan/*",
        "/usr/src/nvidia-*",
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
                f'changes of {ds} dataset', serializable=False,
                postprocess=usr_postprocess if ds.split('/')[-1] == 'usr' else None
            )],
        )
        for ds in get_ds_list()
    ] + [
        FileMetric('root_dataset_configuration', '/conf/truenas_root_ds.json', extension='.json'),
        MiddlewareClientMetric('bootenvs', [MiddlewareCommand('bootenv.query')]),
        PythonMetric('developer_mode', get_root_ds),
    ]
