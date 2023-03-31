import pytest

from ixdiagnose.plugins.prerequisites.service import ServiceRunningPrerequisite
from subprocess import CompletedProcess


@pytest.mark.parametrize('name,args,returncode,should_work', [
    ('scst', ('systemctl', 'is-active', '--quiet', 'scst'), 0, True),
    ('scst', ('systemctl', 'is-active', '--quiet', 'scst'), 1, False),
])
def test_service_prerequisite(mocker, name, args, returncode, should_work):
    mocker.patch(
        'ixdiagnose.plugins.prerequisites.service.run', return_value=CompletedProcess(
            args=args, returncode=returncode, stdout='', stderr=''
        )
    )
    assert ServiceRunningPrerequisite(service_name=name).evaluate_impl() is should_work
