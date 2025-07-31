import pytest

from ixdiagnose.plugins.prerequisites import ActiveDirectoryStatePrerequisite, DomainJoinedPrerequisite
from ixdiagnose.utils.middleware import MiddlewareCommand, MiddlewareResponse

DISABLED = {"type": None, "status": None, "status_msg": None}
AD_HEALTHY = {"type": "ACTIVEDIRECTORY", "status": "HEALTHY", "status_msg": None}
AD_FAULTED = {"type": "ACTIVEDIRECTORY", "status": "FAULTED", "status_msg": "Some error"}
IPA_HEALTHY = {"type": "IPA", "status": "HEALTHY", "status_msg": None}
IPA_FAULTED = {"type": "IPA", "status": "FAULTED", "status_msg": "Some error"}
LDAP_HEALTHY = {"type": "LDAP", "status": "HEALTHY", "status_msg": None}
LDAP_FAULTED = {"type": "LDAP", "status": "FAULTED", "status_msg": "Some error"}


@pytest.mark.parametrize('output,should_work', [
    (DISABLED, False),
    (AD_HEALTHY, True),
    (AD_FAULTED, True),
    (IPA_HEALTHY, False),
    (IPA_FAULTED, False),
    (LDAP_HEALTHY, False),
    (LDAP_FAULTED, False),
])
def test_activedirectory_prerequisite(mocker, output, should_work):
    mocker.patch.object(
        MiddlewareCommand, 'execute', return_value=MiddlewareResponse(output=output, result_key='pre_requisite')
    )
    assert ActiveDirectoryStatePrerequisite().evaluate_impl() is should_work


@pytest.mark.parametrize('output,should_work', [
    (DISABLED, False),
    (AD_HEALTHY, True),
    (AD_FAULTED, True),
    (IPA_HEALTHY, True),
    (IPA_FAULTED, True),
    (LDAP_HEALTHY, False),
    (LDAP_FAULTED, False),
])
def test_domain_join_prerequisite(mocker, output, should_work):
    mocker.patch.object(
        MiddlewareCommand, 'execute', return_value=MiddlewareResponse(output=output, result_key='pre_requisite')
    )
    assert DomainJoinedPrerequisite().evaluate_impl() is should_work
