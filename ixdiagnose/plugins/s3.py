from ixdiagnose.utils.command import Command
from ixdiagnose.utils.formatter import remove_keys
from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import CommandMetric, FileMetric, MiddlewareClientMetric

S3_SERVICE_UNIT = "truenas_s3"


class S3(Plugin):
    name = "s3"
    metrics = [
        MiddlewareClientMetric(
            "s3_config",
            [
                MiddlewareCommand("s3.config", result_key="config"),
                MiddlewareCommand(
                    "s3.accesskey.query", result_key="accesskeys", format_output=remove_keys(["access_key", "secret"])
                ),
                MiddlewareCommand("sharing.s3.query", result_key="buckets"),
            ],
        ),
        CommandMetric(
            "services_status",
            [
                Command(
                    ["systemctl", "status", S3_SERVICE_UNIT],
                    "S3 Service Status",
                    serializable=False,
                    safe_returncodes=[0, 3],
                ),
            ],
        ),
        CommandMetric(
            "config_check",
            [
                # Reads the rendered files the way a start or a reload would and names what would be refused.
                # Serves, registers and writes nothing. The refusal goes to stderr with exit code 1, so merge it
                # into the output rather than discarding it.
                Command(
                    "s3d --check 2>&1",
                    "S3 Service Configuration Check",
                    serializable=False,
                    safe_returncodes=[0, 1],
                ),
            ],
        ),
        # The credentials file the S3 service also reads is deliberately not collected
        FileMetric("buckets", "/etc/truenas_s3/buckets.conf", extension=".conf"),
        FileMetric("policies", "/etc/truenas_s3/policies.conf", extension=".conf"),
    ]
