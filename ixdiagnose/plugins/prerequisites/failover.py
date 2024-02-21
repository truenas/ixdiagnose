from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Prerequisite


class FailoverPrerequisite(Prerequisite):

    def evaluate_impl(self) -> bool:
        return MiddlewareCommand('failover.licensed').execute().output

    def __str__(self):
        return 'Failover is licensed check'
