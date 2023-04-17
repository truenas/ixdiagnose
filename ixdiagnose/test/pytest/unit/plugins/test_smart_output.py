import pytest
from subprocess import CompletedProcess

from ixdiagnose.plugins.smart import smart_output


@pytest.mark.parametrize('run_output', [
    [
        CompletedProcess(
            args=(
                'lsblk', '-ndo', 'name', '-I', '8,65,66,67,68,69,70,71,128,129,130,131,132,133,134,135,254,259'
            ),
            returncode=0,
            stdout='vda\nvdb\nvdc\n',
            stderr=''
        ),
        CompletedProcess(
            args=(
                'smartctl', '-a', '/dev/vda'
            ),
            returncode=1,
            stdout='smartctl 7.2 2020-12-30 r5155 [x86_64-linux-5.15.79+truenas] (local build)\n'
                   'Copyright (C) 2002-20, Bruce Allen, Christian Franke, www.smartmontools.org\n\n'
                   '/dev/vda: Unable to detect device type\nPlease specify device type with the -d option.\n\n'
                   'Use smartctl -h to get a usage summary\n\n',
            stderr=''
        ),
        CompletedProcess(
            args=(
                'smartctl', '-a', '/dev/vdb'
            ),
            returncode=1,
            stdout='smartctl 7.2 2020-12-30 r5155 [x86_64-linux-5.15.79+truenas] (local build)\n'
                   'Copyright (C) 2002-20, Bruce Allen, Christian Franke, www.smartmontools.org\n\n'
                   '/dev/vdb: Unable to detect device type\nPlease specify device type with the -d option.\n\n'
                   'Use smartctl -h to get a usage summary\n\n',
            stderr=''
        ),
        CompletedProcess(
            args=(
                'smartctl', '-a', '/dev/vdc'
            ),
            returncode=1,
            stdout='smartctl 7.2 2020-12-30 r5155 [x86_64-linux-5.15.79+truenas] (local build)\n'
                   'Copyright (C) 2002-20, Bruce Allen, Christian Franke, www.smartmontools.org\n\n'
                   '/dev/vdc: Unable to detect device type\n'
                   'Please specify device type with the -d option.\n\n'
                   'Use smartctl -h to get a usage summary\n\n',
            stderr=''
        ),
    ]
])
def test_smart_output(mocker, run_output):
    client = mocker.MagicMock()
    mocker.patch('ixdiagnose.plugins.smart.run', side_effect=run_output)
    assert isinstance(smart_output(client, {'serializable': False}), str) is True
