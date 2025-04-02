from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Prerequisite


class FibreChannelPrerequisite(Prerequisite):

    def evaluate_impl(self) -> bool:
        return MiddlewareCommand('fc.capable').execute().output

    def __str__(self):
        return 'Fibre Channel is licensed and available check'
