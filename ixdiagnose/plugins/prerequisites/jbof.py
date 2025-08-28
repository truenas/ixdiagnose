from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Prerequisite


class JBOFPrerequisite(Prerequisite):

    def evaluate_impl(self) -> bool:
        return int(MiddlewareCommand('jbof.query', [[], {'count': True}]).execute().output) > 0

    def __str__(self):
        return 'JBOF is configured check'
