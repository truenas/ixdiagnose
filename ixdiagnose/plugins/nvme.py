import os
import re
from typing import Any

from .base import Plugin
from .metrics import CommandMetric, PythonMetric
from ixdiagnose.utils.command import Command
from ixdiagnose.utils.middleware import MiddlewareClient
from ixdiagnose.utils.run import run

NVME_RE = re.compile(r"^nvme\dn\d+$")


def get_nvme_devs() -> list[str]:
    nvmes = list()
    with os.scandir("/dev/") as sdir:
        for i in filter(lambda x: NVME_RE.match(x.name), sdir):
            nvmes.append(i.path)
    return nvmes


def run_nvme_cmd(action: str, nvme: str) -> str:
    header = f"nvme {action} {nvme!r}\n"
    cp = run(["nvme", action, nvme], check=False)
    if cp.returncode:
        footer = f"FAILED: {cp.stderr}\n\n"
    else:
        footer = cp.stdout + "\n\n"

    return header + footer


def get_nvme_id_ctrl(client: MiddlewareClient, context: Any) -> str:
    output = ""
    for nvme in get_nvme_devs():
        output += run_nvme_cmd("id-ctrl", nvme)
    return output


def get_nvme_id_ns(client: MiddlewareClient, context: Any) -> str:
    output = ""
    for nvme in get_nvme_devs():
        output += run_nvme_cmd("id-ns", nvme)
    return output


def get_nvme_smart_log(client: MiddlewareClient, context: Any) -> str:
    output = ""
    for nvme in get_nvme_devs():
        output += run_nvme_cmd("smart-log", nvme)
    return output


class NVME(Plugin):
    name = "nvme"
    metrics = [
        CommandMetric(
            "nvme_list_v",
            [
                Command(["nvme", "list", "-v"], "nvme list -v", serializable=False),
            ],
        ),
        CommandMetric(
            "nvme_discover",
            [
                Command(["nvme", "discover"], "nvme discover", serializable=False),
            ],
        ),
        PythonMetric(
            "nvme_id_ctrl",
            callback=get_nvme_id_ctrl,
            description="Identify Controller",
            serializable=False,
        ),
        PythonMetric(
            "nvme_id_ns",
            callback=get_nvme_id_ns,
            description="Identify Namespace",
            serializable=False,
        ),
        PythonMetric(
            "nvme_smart_log",
            callback=get_nvme_smart_log,
            description="SMART Log",
            serializable=False,
        ),
    ]
