from collections.abc import Callable
import subprocess
from typing import Any, Optional, Union

from .run import run


class Command:

    def __init__(
        self, command: Union[str, list], description: str, serializable: bool = True,
        safe_returncodes: list = None, env: Optional[dict] = None, max_lines: Optional[int] = None,
        postprocess: Optional[Callable[[Any, str], str]] = None,
    ):
        self.command: Union[str, list] = command
        self.description: str = description
        self.env: Optional[dict] = env
        self.max_lines: Optional[int] = max_lines
        self.serializable: bool = serializable
        self.safe_returncodes: list = safe_returncodes or [0]
        self.postprocess = postprocess
        self.execution_context: Any = None

    def execute(self) -> subprocess.CompletedProcess:
        cp = run(self.command, check=False, env=self.env)
        if cp.returncode in self.safe_returncodes:
            if self.postprocess:
                cp.stdout = self.postprocess(self.execution_context, cp.stdout)
            if self.max_lines:
                cp.stdout = "\n".join(cp.stdout.splitlines()[:self.max_lines])
        return cp
