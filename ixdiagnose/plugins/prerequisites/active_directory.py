from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Prerequisite


class ActiveDirectoryStatePrerequisite(Prerequisite):

    def __init__(self, ad_status: str):
        super().__init__(True)
        self.cache_key = ad_status

    def evaluate_impl(self) -> bool:
        response = MiddlewareCommand('activedirectory.get_state').execute()
        return response.output == self.cache_key

    def __str__(self):
        return f'{self.cache_key!r} active directory service state check'
