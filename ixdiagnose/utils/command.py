import subprocess
from typing import Any, Optional, Union

from .run import check_shell_command, run


class Command:
    def __init__(
        self,
        command: Union[str, list],
        description: str,
        serializable: bool = True,
        safe_returncodes: list = None,
        env: Optional[dict] = None,
        max_lines: Optional[int] = None,
        shell: bool = False,
    ):
        check_shell_command(command, shell)
        self.command: Union[str, list] = command
        self.description: str = description
        self.env: Optional[dict] = env
        self.max_lines: Optional[int] = max_lines
        self.serializable: bool = serializable
        self.safe_returncodes: list = safe_returncodes or [0]
        self.shell: bool = shell
        self.execution_context: Any = None

    def execute(self) -> subprocess.CompletedProcess:
        cp = run(self.command, shell=self.shell, check=False, env=self.env)
        if cp.returncode in self.safe_returncodes:
            if self.max_lines:
                cp.stdout = "\n".join(cp.stdout.splitlines()[: self.max_lines])
        return cp
