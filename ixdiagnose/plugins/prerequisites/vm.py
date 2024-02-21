from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Prerequisite


class VMPrerequisite(Prerequisite):

    def evaluate_impl(self) -> bool:
        return MiddlewareCommand('vm.supports_virtualization').execute().output

    def __str__(self):
        return 'VM service state check'
