from subprocess import CompletedProcess

from ixdiagnose.plugins.smb import get_smb_shares


def test_get_smb_shares_passes_share_name_and_path_as_arguments(mocker):
    share = {"name": "a$(touch /tmp/pwned) b", "path": "/mnt/tank/x;touch /tmp/pwned y"}
    responses = {
        "sharing.smb.query": [share],
        "sharing.smb.getacl": {},
        "filesystem.statfs": {},
    }
    client = mocker.Mock()
    client.call.side_effect = lambda method, *args: responses[method]
    run = mocker.patch("ixdiagnose.plugins.smb.run", return_value=CompletedProcess([], 0, "", ""))

    get_smb_shares(client, None)

    assert run.call_args_list == [
        mocker.call(["testparm", "-s", "--section-name=a$(touch /tmp/pwned) b"], check=False),
        mocker.call(["truenas_getfacl", "/mnt/tank/x;touch /tmp/pwned y"], check=False),
    ]
