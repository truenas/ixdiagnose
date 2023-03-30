import subprocess

from typing import Optional, Union

from .run import run


class Command:

    def __init__(
        self, command: Union[str, list], description: str, serializable: bool = True,
        safe_returncodes: list = None, env: Optional[dict] = None, max_lines: Optional[int] = None,
    ):
        self.command: Union[str, list] = command
        self.description: str = description
        self.env: Optional[dict] = env
        self.max_length: Optional[int] = max_lines
        self.serializable: bool = serializable
        self.safe_returncodes: list = safe_returncodes or [0]

    def execute(self) -> subprocess.CompletedProcess:
        cp = run(self.command, check=False, env=self.env)
        if self.max_length and cp.returncode in self.safe_returncodes:
            cp.stdout = cp.stdout.splitlines()[:self.max_length]
        return cp
