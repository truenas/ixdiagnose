import pytest

from ixdiagnose.utils.command import Command
from ixdiagnose.plugins.metrics.command import CommandMetric
from subprocess import CompletedProcess


@pytest.mark.parametrize('name,cmds,return_values,cmd_context,context,should_work', [(
        'cmd',
        [Command(['lsblk', '-o', 'NAME,FSTYPE,LABEL,UUID,PARTUUID', '-l', '-e', '230'], 'lsblk', serializeable=False)],
        [
            CompletedProcess(
                args=('lsblk', '-o', 'NAME,FSTYPE,LABEL,UUID,PARTUUID', '-l', '-e', '230'),
                returncode=0,
                stdout='NAME  FSTYPE            LABEL         UUID                                 PARTUUID\n'
                       'md127                                                                      \nsr0'
                       '                                            \nmd127 swap'
                       '                            684369b9-3ff2-4b34-8dad-fb20ee3636b7\nvda'
                       '                                                                        \nvda1'
                       '                                                                       '
                       'c46444bc-ef4a-4849-b1e5-c2a1686e2fa2\nvda2  vfat              EFI           86C1-7F14'
                       '1f8d1273-983d-4902-a8e3-9967c8b06305\nvda3  zfs_member        boot-pool'
                       '     17809027050300157700                 b45511be-5418-4b36-8d7f-6d4ec9eec78b\nvdb'
                       '                                                                        \n'
                       'vdb1  linux_raid_member truenas:swap0 fbc808a8-b6ad-852e-f1bc-b2970e88d6f6'
                       'd45f3a74-dac6-4e19-b2e2-44576b1e7343\nvdb2  zfs_member        crave         1481520261979659747'
                       '2a7959e0-e47e-4c3d-9057-147e120d8450\nvdc'
                       '\nvdc1  linux_raid_member truenas:swap0 fbc808a8-b6ad-852e-f1bc-b2970e88d6f6'
                       '073d3d89-c5ac-4453-95f5-0b4a4b368d52\nvdc2  zfs_member        rootd         6009907550966676357'
                       '       b33645d2-6cc9-40a0-9ade-e5c78874a9e5\n',
                stderr=''
            )
        ],
        '-------------------------------------------------------\n'
        '1) lsblk -o NAME,FSTYPE,LABEL,UUID,PARTUUID -l -e 230\n'
        '-------------------------------------------------------\n\n'
        'NAME  FSTYPE            LABEL         UUID                                 PARTUUID\n'
        'md127                                                                      \n'
        'sr0                                                                        \n'
        'md127 swap                            684369b9-3ff2-4b34-8dad-fb20ee3636b7\n'
        'vda                                                                        \n'
        'vda1                                                                       '
        'c46444bc-ef4a-4849-b1e5-c2a1686e2fa2\n'
        'vda2  vfat              EFI           86C1-7F14                            '
        '1f8d1273-983d-4902-a8e3-9967c8b06305\n'
        'vda3  zfs_member        boot-pool     17809027050300157700                 '
        'b45511be-5418-4b36-8d7f-6d4ec9eec78b\n'
        'vdb                                                                        \n'
        'vdb1  linux_raid_member truenas:swap0 fbc808a8-b6ad-852e-f1bc-b2970e88d6f6 '
        'd45f3a74-dac6-4e19-b2e2-44576b1e7343\n'
        'vdb2  zfs_member        crave         1481520261979659747                  '
        '2a7959e0-e47e-4c3d-9057-147e120d8450\n'
        'vdc                                                                        \n'
        'vdc1  linux_raid_member truenas:swap0 fbc808a8-b6ad-852e-f1bc-b2970e88d6f6 '
        '073d3d89-c5ac-4453-95f5-0b4a4b368d52\n'
        'vdc2  zfs_member        rootd         6009907550966676357                  '
        'b33645d2-6cc9-40a0-9ade-e5c78874a9e5\n',
        '-------------------------------------------------------\n'
        '1) lsblk -o NAME,FSTYPE,LABEL,UUID,PARTUUID -l -e 230\n'
        '-------------------------------------------------------\n\n'
        'NAME  FSTYPE            LABEL         UUID                                 PARTUUID\n'
        'md127                                                                      \n'
        'sr0                                                                        \n'
        'md127 swap                            684369b9-3ff2-4b34-8dad-fb20ee3636b7\n'
        'vda                                                                        \n'
        'vda1                                                                       '
        'c46444bc-ef4a-4849-b1e5-c2a1686e2fa2\n'
        'vda2  vfat              EFI           86C1-7F14                            '
        '1f8d1273-983d-4902-a8e3-9967c8b06305\n'
        'vda3  zfs_member        boot-pool     17809027050300157700                 '
        'b45511be-5418-4b36-8d7f-6d4ec9eec78b\n'
        'vdb                                                                        \n'
        'vdb1  linux_raid_member truenas:swap0 fbc808a8-b6ad-852e-f1bc-b2970e88d6f6 '
        'd45f3a74-dac6-4e19-b2e2-44576b1e7343\n'
        'vdb2  zfs_member        crave         1481520261979659747                  '
        '2a7959e0-e47e-4c3d-9057-147e120d8450\n'
        'vdc                                                                        \n'
        'vdc1  linux_raid_member truenas:swap0 fbc808a8-b6ad-852e-f1bc-b2970e88d6f6 '
        '073d3d89-c5ac-4453-95f5-0b4a4b368d52\n'
        'vdc2  zfs_member        rootd         6009907550966676357                  '
        'b33645d2-6cc9-40a0-9ade-e5c78874a9e5\n',
        True
),
    (
        'cmd',
        [Command(['lsblk', '-o', 'NAME,FSTYPE,LABEL,UUID,PARTUUID', '-l', '-e', '230'], 'lsblk',
                 serializeable=False)],
        [
            CompletedProcess(
                args=('lsblk', '-o', 'NAME,FSTYPE,LABEL,UUID,PARTUUID', '-l', '-e', '230'),
                returncode=0,
                stdout='NAME  FSTYPE            LABEL         UUID                                 PARTUUID\n'
                       'md127                                                                      \nsr0'
                       '                                            \nmd127 swap'
                       '                            684369b9-3ff2-4b34-8dad-fb20ee3636b7 \nvda'
                       '                                                                        \nvda1'
                       '                                                                       '
                       'c46444bc-ef4a-4849-b1e5-c2a1686e2fa2\nvda2  vfat              EFI           86C1-7F14'
                       '1f8d1273-983d-4902-a8e3-9967c8b06305\nvda3  zfs_member        boot-pool'
                       '     17809027050300157700                 b45511be-5418-4b36-8d7f-6d4ec9eec78b\nvdb'
                       '                                                                        \n'
                       'vdb1  linux_raid_member truenas:swap0 fbc808a8-b6ad-852e-f1bc-b2970e88d6f6'
                       'd45f3a74-dac6-4e19-b2e2-44576b1e7343\nvdb2  zfs_member        crave         '
                       '1481520261979659747'
                       '2a7959e0-e47e-4c3d-9057-147e120d8450\nvdc'
                       '\nvdc1  linux_raid_member truenas:swap0 fbc808a8-b6ad-852e-f1bc-b2970e88d6f6'
                       '073d3d89-c5ac-4453-95f5-0b4a4b368d52\nvdc2  zfs_member        rootd         '
                       '6009907550966676357'
                       '       b33645d2-6cc9-40a0-9ade-e5c78874a9e5\n',
                stderr=''
            )
        ],
        '-------------------------------------------------------\n'
        '1) lsblk -o NAME,FSTYPE,LABEL,UUID,PARTUUID -l -e 230\n'
        '-------------------------------------------------------\n\n'
        'NAME  FSTYPE            LABEL         UUID                                 PARTUUID\n'
        'md27                                                                      \n'
        'sr                                                                        \n'
        'md127 swap                            684369b9-3ff2-4b34-8dad-fb20ee3636b7\n'
        'vda                                                                        \n'
        'vda                                                                       '
        'c46444bc-ef4a-4849-b1e5-c2a1686e2fa2\n'
        'vda2  vfat              EFI           86C1-7F14                            '
        '1f8d1273-983d-4902-a8e3-9967c8b06305\n'
        'vda3  zfs_member        boot-pool     17809027050300157700                 '
        'b45511be-5418-4b36-8d7f-6d4ec9eec78b\n'
        'vdb                                                                        \n'
        'vdb1  linux_raid_member truenas:swap0 fbc808a8-b6ad-852e-f1bc-b2970e88d6f6 '
        'd45f3a74-dac6-4e19-b2e2-44576b1e7343\n'
        'vdb2  zfs_member        crave         1481520261979659747                  '
        '2a7959e0-e47e-4c3d-9057-147e120d8450\n'
        'vdc                                                                        \n'
        'vdc1  linux_raid_member truenas:swap0 fbc808a8-b6ad-852e-f1bc-b2970e88d6f6 '
        '073d3d89-c5ac-4453-95f5-0b4a4b368d52\n'
        'vdc2  zfs_member        rootd         6009907550966676357                  '
        'b33645d2-6cc9-40a0-9ade-e5c78874a9e5\n',
        '-------------------------------------------------------\n'
        '1) lsblk -o NAME,FSTYPE,LABEL,UUID,PARTUUID -l -e 230\n'
        '-------------------------------------------------------\n\n'
        'NAME  FSTYPE            LABEL         UUID                                 PARTUUID\n'
        'md127                                                                      \n'
        'sr0                                                                        \n'
        'md127 swap                            684369b9-3ff2-4b34-8dad-fb20ee3636b7\n'
        'vda                                                                        \n'
        'vda1                                                                       '
        'c46444bc-ef4a-4849-b1e5-c2a1686e2fa2\n'
        'vda2  vfat              EFI           86C1-7F14                            '
        '1f8d1273-983d-4902-a8e3-9967c8b06305\n'
        'vda3  zfs_member        boot-pool     17809027050300157700                 '
        'b45511be-5418-4b36-8d7f-6d4ec9eec78b\n'
        'vdb                                                                        \n'
        'vdb1  linux_raid_member truenas:swap0 fbc808a8-b6ad-852e-f1bc-b2970e88d6f6 '
        'd45f3a74-dac6-4e19-b2e2-44576b1e7343\n'
        'vdb2  zfs_member        crave         1481520261979659747                  '
        '2a7959e0-e47e-4c3d-9057-147e120d8450\n'
        'vdc                                                                        \n'
        'vdc1  linux_raid_member truenas:swap0 fbc808a8-b6ad-852e-f1bc-b2970e88d6f6 '
        '073d3d89-c5ac-4453-95f5-0b4a4b368d52\n'
        'vdc2  zfs_member        rootd         6009907550966676357                  '
        'b33645d2-6cc9-40a0-9ade-e5c78874a9e5\n',
        False
    )
]
                         )
def test_command_metric(mocker, name, cmds, return_values, cmd_context, context, should_work):
    mocker.patch('ixdiagnose.utils.command.Command.execute', side_effect=return_values)
    mocker.patch('ixdiagnose.plugins.metrics.command.CommandMetric.format_data', return_value=cmd_context)
    if not should_work:
        metric_report, result = CommandMetric(name, cmds).execute_impl()
        # We do not assert metric report because everytime when command run, execution time changes.
        assert result != context
    else:
        metric_report, result = CommandMetric(name, cmds).execute_impl()
        # We do not assert metric report because everytime when command run, execution time changes.
        assert result == context
