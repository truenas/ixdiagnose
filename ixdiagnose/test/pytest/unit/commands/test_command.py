import pytest

from ixdiagnose.test.pytest.unit.utils import get_asset
from ixdiagnose.utils.command import Command
from subprocess import CompletedProcess


ASSETS_FILE_NAME = 'lsblk_output.txt'


@pytest.mark.parametrize('args,cmd', [
    (
        ('lsblk', '-o', 'NAME,FSTYPE,LABEL,UUID,PARTUUID', '-l', '-e', '230'),
        ['lsblk', '-o', 'NAME,FSTYPE,LABEL,UUID,PARTUUID', '-l', '-e', '230'],
    ),
    (
        ('lsblk', '-o', 'NAME,FSTYPE,LABEL,UUID,PARTUUID', '-l', '-e', '230'),
        ['lsblk', '-o', 'NAME,FSTYPE,LABEL,UUID,PARTUUID', '-l', '-e', '230'],
    ),
    (
        'lsblk -o NAME,FSTYPE,LABEL,UUID,PARTUUID -l -e 230',
        'lsblk -o NAME,FSTYPE,LABEL,UUID,PARTUUID -l -e 230',
    ),
])
def test_command_shell(mocker, args, cmd):
    mocker.patch(
        'ixdiagnose.utils.command.run', return_value=CompletedProcess(
            args=args, returncode=0, stdout=get_asset(ASSETS_FILE_NAME), stderr=''
        )
    )
    assert Command(cmd, 'lsblk').execute() is not None
