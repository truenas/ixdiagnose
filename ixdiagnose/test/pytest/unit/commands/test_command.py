import pytest

from ixdiagnose.test.pytest.unit.utils import get_asset
from ixdiagnose.utils.command import Command
from subprocess import CompletedProcess


ASSETS_FILE_NAME = "lsblk_output.txt"


@pytest.mark.parametrize(
    "args,cmd,shell",
    [
        (
            ("lsblk", "-o", "NAME,FSTYPE,LABEL,UUID,PARTUUID", "-l", "-e", "230"),
            ["lsblk", "-o", "NAME,FSTYPE,LABEL,UUID,PARTUUID", "-l", "-e", "230"],
            False,
        ),
        (
            ("lsblk", "-o", "NAME,FSTYPE,LABEL,UUID,PARTUUID", "-l", "-e", "230"),
            ["lsblk", "-o", "NAME,FSTYPE,LABEL,UUID,PARTUUID", "-l", "-e", "230"],
            False,
        ),
        (
            "lsblk -o NAME,FSTYPE,LABEL,UUID,PARTUUID -l -e 230",
            "lsblk -o NAME,FSTYPE,LABEL,UUID,PARTUUID -l -e 230",
            True,
        ),
    ],
)
def test_command_shell(mocker, args, cmd, shell):
    run = mocker.patch(
        "ixdiagnose.utils.command.run",
        return_value=CompletedProcess(args=args, returncode=0, stdout=get_asset(ASSETS_FILE_NAME), stderr=""),
    )
    assert Command(cmd, "lsblk", shell=shell).execute() is not None
    run.assert_called_once_with(cmd, shell=shell, check=False, env=None)


@pytest.mark.parametrize("cmd,shell", [("lsblk -l", False), (["lsblk", "-l"], True)])
def test_command_shell_must_match_type(cmd, shell):
    with pytest.raises(TypeError, match="shell=True"):
        Command(cmd, "lsblk", shell=shell)
