from ixdiagnose.utils.command import Command

from .base import Plugin
from .metrics import CommandMetric, FileMetric
from .prerequisites import ServiceRunningPrerequisite


class Discovery(Plugin):
    name = "discovery"
    metrics = [
        CommandMetric(
            "discovery_status",
            [
                Command(
                    ["truenas-discovery-status"],
                    "TrueNAS discovery daemon runtime status (mDNS/NetBIOS/WS-Discovery)",
                    serializable=True,
                ),
            ],
            prerequisites=[ServiceRunningPrerequisite("truenas-discoveryd")],
        ),
        FileMetric("truenas-discoveryd", "/etc/truenas-discovery/truenas-discoveryd.conf", extension=".conf"),
    ]
    raw_metrics = [
        CommandMetric(
            "service_status",
            [
                Command(
                    ["systemctl", "status", "truenas-discoveryd"],
                    "TrueNAS discovery service status",
                    serializable=False,
                    safe_returncodes=[0, 3],
                ),
            ],
        ),
    ]
