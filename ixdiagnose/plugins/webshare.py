from ixdiagnose.utils.command import Command
from ixdiagnose.utils.formatter import dumps
from ixdiagnose.utils.middleware import MiddlewareClient, MiddlewareCommand
from ixdiagnose.utils.run import run
from typing import Any

from .base import Plugin
from .metrics import CommandMetric, FileMetric, MiddlewareClientMetric, PythonMetric

# Per-session truenas-file-manager processes write to the auth unit's journal, so it gets the largest window.
WEBSHARE_UNITS = {
    "truenas-webshare-auth": 5000,
    "truenas-webshare-link": 2000,
    "truenas-webshare-mcp": 1000,
    "truenas-webshare-caddy": 1000,
    "truenas-webshare-link-caddy": 1000,
    "truenas-webshare-caddy-config": 200,
    "truenas-webshare-link-caddy-config": 200,
}


def get_webshare_shares(client: MiddlewareClient, context: Any) -> str:
    webshare_shares = client.call("sharing.webshare.query")
    for webshare_share in webshare_shares:
        try:
            webshare_share["statfs"] = client.call("filesystem.statfs", webshare_share["path"])
        except Exception as exc:
            # Most likely a locked path, so there is no ACL to read either.
            webshare_share["statfs"] = f"Failed to get statfs for share: {exc}"
            continue

        getacl = run(["truenas_getfacl", webshare_share["path"]], check=False)
        if getacl.returncode:
            webshare_share["fsacl"] = f"Failed to get fs acl: {getacl.stderr}"
        else:
            webshare_share["fsacl"] = getacl.stdout

    return dumps(webshare_shares)


class WebShare(Plugin):
    name = "webshare"
    metrics = [
        MiddlewareClientMetric(
            "webshare_info",
            [
                MiddlewareCommand("webshare.config"),
                MiddlewareCommand("webshare.bindip_choices"),
                MiddlewareCommand("sharing.webshare.query"),
            ],
        ),
        PythonMetric(
            "webshare_shares",
            callback=get_webshare_shares,
            description="WebShare Shares and Permissions",
            serializable=False,
        ),
        FileMetric("webshare-auth-config", "/etc/webshare-auth/config.json", extension=".json"),
        FileMetric("webshare-shares-config", "/etc/webshare/config.json", extension=".json"),
        FileMetric("webshare-link-config", "/etc/webshare-link/config.json", extension=".json"),
        FileMetric("webshare-auth-caddy", "/run/webshare-auth-caddy/caddy.json", extension=".json"),
        FileMetric("webshare-link-caddy", "/run/webshare-link-caddy/caddy.json", extension=".json"),
        FileMetric("etc-default-truenas-webshare", "/etc/default/truenas-webshare"),
        CommandMetric(
            "webshare_general",
            [
                Command(
                    "ps -eo pid,ppid,user,etime,rss,args | grep -E '[t]ruenas-(webshare|file-manager)|[c]addy run'",
                    "WebShare Processes",
                    serializable=False,
                    # grep exits 1 when nothing matches, which is the answer when the service is stopped.
                    safe_returncodes=[0, 1],
                ),
                Command(
                    "ls -la /var/run/webshare /var/db/system/webshare /var/db/system/webshare/bulk-downloads 2>&1",
                    "WebShare Runtime and Data Directories",
                    serializable=False,
                    # ls exits 2 on a missing operand, and an unsafe return code discards the output.
                    safe_returncodes=[0, 1, 2],
                ),
            ],
        ),
        CommandMetric(
            "services_status",
            [
                Command(
                    ["systemctl", "status", unit],
                    f"{unit} Service Status",
                    serializable=False,
                    # 3 is an inactive unit, 4 one that is not installed; both are answers worth keeping.
                    safe_returncodes=[0, 3, 4],
                )
                for unit in WEBSHARE_UNITS
            ]
            + [
                Command(
                    [
                        "systemctl",
                        "show",
                        *WEBSHARE_UNITS,
                        "-p",
                        "Id,NRestarts,ActiveState,SubState,Result,ExecMainStartTimestamp",
                    ],
                    "WebShare unit state",
                    serializable=False,
                ),
            ],
        ),
        CommandMetric(
            "services_logs",
            [
                Command(
                    ["journalctl", "-u", unit, "-n", str(lines), "--no-pager"],
                    f"{unit} logs",
                    serializable=False,
                )
                for unit, lines in WEBSHARE_UNITS.items()
            ],
        ),
    ]
