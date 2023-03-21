import pytest

from ixdiagnose.plugins.prerequisites import ActiveDirectoryStatePrerequisite
from ixdiagnose.utils.middleware import MiddlewareCommand, MiddlewareResponse


@pytest.mark.parametrize('status,output,should_work', [
    ('HEALTHY', 'HEALTHY', True),
    ('HEALTHY', 'DISABLED', False),
])
def test_activedirectory_prerequisite(mocker, status, output, should_work):
    mocker.patch.object(
        MiddlewareCommand, 'execute', return_value=MiddlewareResponse(output=output, result_key='pre_requisite')
    )
    assert ActiveDirectoryStatePrerequisite(status).evaluate_impl() is should_work
