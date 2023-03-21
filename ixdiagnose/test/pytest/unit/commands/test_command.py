import pytest

from ixdiagnose.utils.command import Command
from subprocess import CompletedProcess


lsblk_output = '''
NAME  FSTYPE            LABEL         UUID                                 PARTUUID
sda
sda1                                                                       766d2699-8b89-4658-bf73-c52a3b128669
sda2  vfat              EFI           5FB5-019E                            bd2a0586-e0af-4124-bfc2-838ba06ab144
sda3  zfs_member        boot-pool     13121244495553945090                 94e05128-0010-4f64-beeb-e9437371499a
sdb
sdb1  linux_raid_member truenas:swap0 033751b0-88c4-9bf8-183f-9db325a55fa6 8d81acbf-3dfa-4d68-8719-7630510ada40
sdb2  zfs_member        tank          16172535520268519460                 a44727fc-7bf1-4b12-ab84-051d6a4845d2
sdc
sdc1  linux_raid_member truenas:swap0 033751b0-88c4-9bf8-183f-9db325a55fa6 7906a2f4-0d91-4f0b-8699-b6c2e40b6471
sdc2  zfs_member        tank          16172535520268519460                 c71e679e-227b-483c-b6d7-e5fd12d9dfae
'''


@pytest.mark.parametrize('args,returncode,stdout,stderr,cmd,description,shell,should_work', [
    (
        ('lsblk', '-o', 'NAME,FSTYPE,LABEL,UUID,PARTUUID', '-l', '-e', '230'),
        0,
        lsblk_output,
        '',
        ['lsblk', '-o', 'NAME,FSTYPE,LABEL,UUID,PARTUUID', '-l', '-e', '230'],
        'lsblk',
        False,
        True,
    ),
    (
        ('lsblk', '-o', 'NAME,FSTYPE,LABEL,UUID,PARTUUID', '-l', '-e', '230'),
        0,
        lsblk_output,
        '',
        ['lsblk', '-o', 'NAME,FSTYPE,LABEL,UUID,PARTUUID', '-l', '-e', '230'],
        'lsblk',
        True,
        False,
    ),
    (
        'lsblk -o NAME,FSTYPE,LABEL,UUID,PARTUUID -l -e 230',
        0,
        lsblk_output,
        '',
        'lsblk -o NAME,FSTYPE,LABEL,UUID,PARTUUID -l -e 230',
        'lsblk',
        False,
        False,
    ),
])
def test_command(mocker, args, returncode, stdout, stderr, cmd, description, shell, should_work):
    mocker.patch(
        'ixdiagnose.utils.command.run', return_value=CompletedProcess(
            args=args, returncode=returncode, stdout=stdout, stderr=stderr
        )
    )
    if not should_work:
        with pytest.raises(Exception):
            Command(cmd, description, shell).execute()
    else:
        assert Command(cmd, description, shell).execute() is not None
