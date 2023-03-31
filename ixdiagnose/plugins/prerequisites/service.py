from ixdiagnose.utils.run import run

from .base import Prerequisite


class ServiceRunningPrerequisite(Prerequisite):

    def __init__(self, service_name: str):
        super().__init__(True)
        self.service_name: str = service_name
        self.cache_key = self.service_name

    def evaluate_impl(self) -> bool:
        return run(['systemctl', 'is-active', '--quiet', self.service_name], check=False).returncode == 0

    def __str__(self):
        return f'{self.service_name!r} systemctl service active check'
