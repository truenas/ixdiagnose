import subprocess

from typing import Optional, Union

from ixdiagnose.exceptions import CallError

from .run import run


class Command:

    def __init__(
        self, command: Union[str, list], description: str, shell: bool = False,
        serializeable: bool = True, safe_returncodes: bool = None, env: Optional[dict] = None,
    ):
        self.command: Union[str, list] = command
        self.description: str = description
        self.env: Optional[dict] = env
        self.shell: bool = shell
        self.serializeable: bool = serializeable
        self.safe_returncodes: list = safe_returncodes or [0]
        if self.shell and not isinstance(self.command, str):
            raise CallError('Command must be a string as shell is specified')
        if not self.shell and not isinstance(self.command, (list, tuple)):
            raise CallError('Command must be list/tuple as shell is unset')

    def execute(self) -> subprocess.CompletedProcess:
        return run(self.command, shell=self.shell, check=False, env=self.env)
