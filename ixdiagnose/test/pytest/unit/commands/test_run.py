import pytest

from subprocess import CompletedProcess
from ixdiagnose.utils.run import run


swapon_output = '''
Filename				Type		Size	Used	Priority
/dev/dm-0                              	partition	2095036	0	-2
/dev/dm-1                              	partition	2095036	0	-3
/dev/dm-2                              	partition	2095036	0	-4
/dev/dm-3                              	partition	2095036	0	-5
'''


@pytest.mark.parametrize('command,stdout,stderr,expected_output,', [
    (
        ['swapon', '-s'],
        swapon_output,
        '',
        CompletedProcess(args=('swapon', '-s'), returncode=0, stdout=swapon_output, stderr=''),
    ),
    (
        ['swapon', '-s'],
        swapon_output,
        '',
        CompletedProcess(args=('swapon', '-s'), returncode=0, stdout=swapon_output, stderr=''),
    )
])
def test_run(mocker, command, stdout, stderr, expected_output):
    mock_popen = mocker.patch('subprocess.Popen')
    mock_popen.return_value.communicate.return_value = (stdout, stderr)
    mock_popen.return_value.returncode = 0
    result = run(command, shell=False, check=False, env=None)
    assert result.stdout == expected_output.stdout
