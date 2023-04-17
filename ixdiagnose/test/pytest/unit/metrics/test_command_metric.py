import pytest

from ixdiagnose.plugins.metrics.command import CommandMetric
from ixdiagnose.test.pytest.unit.utils import get_asset
from ixdiagnose.utils.command import Command
from subprocess import CompletedProcess


@pytest.mark.parametrize('name,cmds,return_values,input_file,output_file,should_work', [
    (
        'cmd',
        [Command(['lsblk', '-o', 'NAME,FSTYPE,LABEL,UUID,PARTUUID', '-l', '-e', '230'], 'lsblk', serializable=False)],
        [
            CompletedProcess(
                args=('lsblk', '-o', 'NAME,FSTYPE,LABEL,UUID,PARTUUID', '-l', '-e', '230'),
                returncode=0,
                stderr=''
            )
        ],
        'cmd_context1.txt',
        'command_metric_output1.txt',
        True
    ),
    (
        'cmd',
        [Command(['lsblk', '-o', 'NAME,FSTYPE,LABEL,UUID,PARTUUID', '-l', '-e', '230'], 'lsblk',
                 serializable=False)],
        [
            CompletedProcess(
                args=('lsblk', '-o', 'NAME,FSTYPE,LABEL,UUID,PARTUUID', '-l', '-e', '230'),
                returncode=0,
                stderr=''
            )
        ],
        'cmd_context2.txt',
        'command_metric_output2.txt',
        False
    )
])
def test_command_metric(mocker, name, cmds, return_values, input_file, output_file, should_work):
    input_params = get_asset(input_file)
    output = get_asset(output_file)

    return_values[0].stdout = output
    mocker.patch('ixdiagnose.utils.command.Command.execute', side_effect=return_values)
    mocker.patch('ixdiagnose.plugins.metrics.command.CommandMetric.format_data', return_value=input_params)
    if should_work:
        metric_report, result = CommandMetric(name, cmds).execute_impl()
        # We do not assert metric report because everytime when command run, execution time changes.
        assert result == output
    else:
        metric_report, result = CommandMetric(name, cmds).execute_impl()
        # We do not assert metric report because everytime when command run, execution time changes.
        assert result != output
