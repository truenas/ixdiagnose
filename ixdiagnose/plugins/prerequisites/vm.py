from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Prerequisite


class VMPrerequisite(Prerequisite):

    def evaluate_impl(self) -> bool:
        return MiddlewareCommand('vm.supports_virtualization').execute()

    def __str__(self):
        return f'{self.cache_key!r} vm service state check'
