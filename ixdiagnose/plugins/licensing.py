from ixdiagnose.utils.command import Command
from ixdiagnose.utils.middleware import AdminMiddlewareCommand, MiddlewareCommand

from .base import Plugin
from .metrics import CommandMetric, MiddlewareClientMetric

LICENSE_DAEMON_UNIT = "truenas-licensed"


class Licensing(Plugin):
    name = "licensing"
    metrics = [
        MiddlewareClientMetric(
            "license_info",
            [
                MiddlewareCommand("truenas.license.info", result_key="license"),
                MiddlewareCommand("truenas.entitlements.info", result_key="entitlements"),
            ],
        ),
        MiddlewareClientMetric(
            "entitlements_debug",
            [
                # Private: the public views omit the daemon verdict, the hardware facts and the
                # matrix column, which is what traces a denial back to its cause.
                AdminMiddlewareCommand("truenas.entitlements.debug_info", result_key="debug_info"),
                AdminMiddlewareCommand("system.is_ha_capable", result_key="is_ha_capable"),
            ],
        ),
        CommandMetric(
            "license_files",
            [
                Command(
                    "ls -la /data/subsystems/truenas_license/ /data/license 2>&1",
                    "License files on disk",
                    serializable=False,
                    # ls exits 2 on a missing operand, and an unsafe return code discards the output.
                    safe_returncodes=[0, 1, 2],
                ),
            ],
        ),
        CommandMetric(
            "daemon_service",
            [
                Command(
                    [
                        "systemctl",
                        "show",
                        LICENSE_DAEMON_UNIT,
                        "-p",
                        "NRestarts,ActiveState,SubState,Result,ExecMainStartTimestamp",
                    ],
                    "License daemon unit state",
                    serializable=False,
                ),
                Command(
                    ["journalctl", "-u", LICENSE_DAEMON_UNIT, "-n", "200", "--no-pager"],
                    "License daemon logs",
                    serializable=False,
                ),
            ],
        ),
    ]
