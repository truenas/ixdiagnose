import json

from subprocess import CompletedProcess
from unittest.mock import MagicMock

from ixdiagnose.plugins.factory import plugin_factory
from ixdiagnose.plugins.webshare import WEBSHARE_UNITS, WebShare, get_webshare_shares


def middleware_client(shares, statfs):
    def call(method, *args):
        if method == "sharing.webshare.query":
            return shares
        if method == "filesystem.statfs":
            result = statfs[args[0]]
            if isinstance(result, Exception):
                raise result
            return result
        raise AssertionError(f"unexpected call {method}")

    client = MagicMock()
    client.call.side_effect = call
    return client


def test_webshare_shares_record_statfs_and_acl(mocker):
    run = mocker.patch(
        "ixdiagnose.plugins.webshare.run",
        return_value=CompletedProcess(["truenas_getfacl"], 0, "# file: mnt/tank/share\n", ""),
    )
    client = middleware_client([{"name": "share", "path": "/mnt/tank/share"}], {"/mnt/tank/share": {"fstype": "zfs"}})

    shares = json.loads(get_webshare_shares(client, None))

    assert shares == [
        {
            "name": "share",
            "path": "/mnt/tank/share",
            "statfs": {"fstype": "zfs"},
            "fsacl": "# file: mnt/tank/share\n",
        }
    ]
    run.assert_called_once_with(["truenas_getfacl", "/mnt/tank/share"], check=False)


def test_a_locked_share_records_the_statfs_failure_and_skips_the_acl(mocker):
    run = mocker.patch("ixdiagnose.plugins.webshare.run")
    client = middleware_client(
        [{"name": "locked", "path": "/mnt/tank/locked"}], {"/mnt/tank/locked": Exception("path is locked")}
    )

    shares = json.loads(get_webshare_shares(client, None))

    assert shares[0]["statfs"] == "Failed to get statfs for share: path is locked"
    assert "fsacl" not in shares[0]
    run.assert_not_called()


def test_a_failed_acl_read_is_recorded(mocker):
    mocker.patch(
        "ixdiagnose.plugins.webshare.run",
        return_value=CompletedProcess(["truenas_getfacl"], 1, "", "Permission denied"),
    )
    client = middleware_client([{"name": "share", "path": "/mnt/tank/share"}], {"/mnt/tank/share": {}})

    shares = json.loads(get_webshare_shares(client, None))

    assert shares[0]["fsacl"] == "Failed to get fs acl: Permission denied"


def test_the_plugin_is_registered():
    assert isinstance(plugin_factory.get_items()["webshare"], WebShare)


def test_every_unit_has_a_status_and_a_log():
    metrics = {metric.name: metric for metric in WebShare.metrics}
    status = [cmd.command for cmd in metrics["services_status"].cmds]
    logs = [cmd.command for cmd in metrics["services_logs"].cmds]

    for unit in WEBSHARE_UNITS:
        assert ["systemctl", "status", unit] in status
        assert any(cmd[:3] == ["journalctl", "-u", unit] for cmd in logs)
