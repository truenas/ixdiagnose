from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Prerequisite


class ActiveDirectoryStatePrerequisite(Prerequisite):

    def evaluate_impl(self) -> bool:
        response = MiddlewareCommand('directoryservices.get_state').execute()
        return (response.output or {}).get('activedirectory') != 'DISABLED'

    def __str__(self):
        return f'{self.cache_key!r} active directory service state check'


class LDAPStatePrerequisite(Prerequisite):

    def evaluate_impl(self) -> bool:
        response = MiddlewareCommand('directoryservices.get_state').execute()
        return (response.output or {}).get('ldap') != 'DISABLED'

    def __str__(self):
        return f'{self.cache_key!r} ldap service state check'
