from json import loads
from typing import Any

from ixdiagnose.utils.command import Command
from ixdiagnose.utils.middleware import MiddlewareClient, MiddlewareCommand
from ixdiagnose.utils.run import run

from .base import Plugin
from .metrics import CommandMetric, FileMetric, MiddlewareClientMetric, PythonMetric
from .prerequisites import LibvirtContainersPrerequisite


CONTAINERS_LIBVIRT_URI = "lxc:///system?socket=/run/truenas_libvirt/libvirt-sock"


def nspawn_containers(client, context):
    try:
        return [i for i in loads(run(["machinectl", "list", "-o", "json"]).stdout) if i["service"] == "systemd-nspawn"]
    except Exception:
        return []


def libvirt_container_domains(client: MiddlewareClient, context: Any) -> str:
    """Dump the libvirt view of every container domain (state plus rendered XML)."""
    sections = []

    listing = run(["virsh", "-c", CONTAINERS_LIBVIRT_URI, "list", "--all"], check=False)
    sections.append(f"$ virsh list --all\n{listing.stdout or listing.stderr}")

    names = run(["virsh", "-c", CONTAINERS_LIBVIRT_URI, "list", "--all", "--name"], check=False)
    for name in filter(None, (line.strip() for line in names.stdout.splitlines())):
        dumpxml = run(["virsh", "-c", CONTAINERS_LIBVIRT_URI, "dumpxml", name], check=False)
        sections.append(f"$ virsh dumpxml {name}\n{dumpxml.stdout or dumpxml.stderr}")

    return "\n\n".join(sections)


class Containers(Plugin):
    name = "containers"
    metrics = [
        PythonMetric("nspawn_containers", nspawn_containers, serializable=True),
        MiddlewareClientMetric(
            "global_config",
            [
                MiddlewareCommand("lxc.config"),
                MiddlewareCommand("lxc.bridge_choices"),
                MiddlewareCommand("container.pool_choices"),
            ],
        ),
        MiddlewareClientMetric("containers", [MiddlewareCommand("container.query")]),
        MiddlewareClientMetric("container_devices", [MiddlewareCommand("container.device.query")]),
        MiddlewareClientMetric(
            "device_choices",
            [
                MiddlewareCommand("container.device.nic_attach_choices"),
                MiddlewareCommand("container.device.usb_choices"),
                MiddlewareCommand("container.device.gpu_choices"),
            ],
        ),
        MiddlewareClientMetric("images", [MiddlewareCommand("container.image.query_registry")]),
        PythonMetric(
            "libvirt_domains",
            libvirt_container_domains,
            description="Libvirt container domains",
            prerequisites=[LibvirtContainersPrerequisite()],
            serializable=False,
        ),
        FileMetric("dnsmasq_conf", "/var/lib/dnsmasq/test.dnsmasq.raw", extension=".conf"),
        FileMetric("dnsmasq_hosts", "/var/lib/dnsmasq/test.dnsmasq.hosts"),
        FileMetric("dnsmasq_leases", "/var/lib/dnsmasq/dnsmasq.leases"),
        CommandMetric(
            "runtime_state",
            [
                Command(
                    ["find", "/run/truenas_containers", "-maxdepth", "2", "-ls"],
                    "Container runtime/idmap state tree",
                    serializable=False,
                ),
            ],
        ),
    ]
    raw_metrics = [
        CommandMetric(
            "bridge",
            [
                Command(["ip", "-d", "link", "show", "truenasbr0"], "Container bridge link", serializable=False),
                Command(["ip", "addr", "show", "truenasbr0"], "Container bridge addresses", serializable=False),
                Command(["bridge", "link", "show"], "Bridge ports", serializable=False),
                Command(["bridge", "fdb", "show"], "Bridge forwarding database", serializable=False),
            ],
        ),
    ]
    serializable_metrics = [
        CommandMetric(
            "bridge",
            [
                Command(["ip", "-d", "-j", "link", "show", "truenasbr0"], "Container bridge link"),
                Command(["ip", "-j", "addr", "show", "truenasbr0"], "Container bridge addresses"),
                Command(["bridge", "-j", "link", "show"], "Bridge ports"),
                Command(["bridge", "-j", "fdb", "show"], "Bridge forwarding database"),
            ],
        ),
    ]
