from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Prerequisite


class ActiveDirectoryStatePrerequisite(Prerequisite):

    def evaluate_impl(self) -> bool:
        response = MiddlewareCommand('directoryservices.status').execute()
        return (response.output or {}).get('type') == 'ACTIVEDIRECTORY'

    def __str__(self):
        return 'Active directory service state check'


class DomainJoinedPrerequisite(Prerequisite):
    # Check whether the directory service has some join state
    def evaluate_impl(self) -> bool:
        response = MiddlewareCommand('directoryservices.status').execute()

        return (response.output or {}).get('type') in ('IPA', 'ACTIVEDIRECTORY')

    def __str__(self):
        return 'Domain joined state check'
