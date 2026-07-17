from collections import defaultdict
from pathlib import Path

from .base import Plugin
from .metrics import PythonMetric


def cpu_ppin(client, context):
    final = defaultdict(list)
    for i in Path("/sys/devices/system/cpu/").glob("cpu*/topology/ppin"):
        try:
            final[i.read_text().strip()].append(i.parent.parent.name.strip())
        except Exception:
            continue

    return dict(final)


def cpu_topology(client, context):
    topology_files = ("core_cpus_list", "thread_siblings_list", "core_id", "physical_package_id", "die_id")
    final = {}
    for cpu_dir in Path("/sys/devices/system/cpu/").glob("cpu[0-9]*"):
        entry = {}
        for filename in topology_files:
            try:
                entry[filename] = (cpu_dir / "topology" / filename).read_text().strip()
            except Exception:
                continue

        if entry:
            final[cpu_dir.name] = entry

    return final


class Cpu(Plugin):
    name = "cpu"
    metrics = [
        PythonMetric("cpu_ppin_info", cpu_ppin, serializable=True),
        PythonMetric("cpu_topology_info", cpu_topology, serializable=True),
    ]
