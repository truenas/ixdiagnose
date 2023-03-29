import pytest

from ixdiagnose.plugins.prerequisites import ActiveDirectoryStatePrerequisite
from ixdiagnose.utils.middleware import MiddlewareCommand, MiddlewareResponse


@pytest.mark.parametrize('output,should_work', [
    ({'activedirectory': 'DISABLED', 'ldap': 'DISABLED'}, True),
    ({'activedirectory': 'FAULTED', 'ldap': 'DISABLED'}, True),
])
def test_activedirectory_prerequisite(mocker, status, output, should_work):
    mocker.patch.object(
        MiddlewareCommand, 'execute', return_value=MiddlewareResponse(output=output, result_key='pre_requisite')
    )
    assert ActiveDirectoryStatePrerequisite().evaluate_impl() is should_work
