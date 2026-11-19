import os
import subprocess
from typing import Union

from ixdiagnose.config import conf


def check_shell_command(command: Union[str, list, tuple], shell: bool) -> None:
    if shell and not isinstance(command, str):
        raise TypeError(f"{command!r}: a command run with shell=True must be a string")

    if not shell and not isinstance(command, (list, tuple)):
        raise TypeError(f"{command!r}: a command must be an argument list, unless it is run with shell=True")


def run(command: Union[str, list, tuple], *, shell: bool = False, **kwargs) -> subprocess.CompletedProcess:
    check_shell_command(command, shell)
    args = command if shell else tuple(command)
    kwargs.setdefault("stdout", subprocess.PIPE)
    kwargs.setdefault("stderr", subprocess.PIPE)
    kwargs.setdefault("timeout", conf.timeout)
    check = kwargs.pop("check", True)
    env = kwargs.pop("env", None) or os.environ

    proc = subprocess.Popen(
        args,
        stdout=kwargs["stdout"],
        stderr=kwargs["stderr"],
        shell=shell,
        encoding="utf8",
        errors="ignore",
        env=env,
    )
    stdout = ""
    try:
        stdout, stderr = proc.communicate(timeout=kwargs["timeout"])
    except subprocess.TimeoutExpired:
        proc.kill()
        stderr = "Timed out waiting for response"
        proc.returncode = -1

    cp = subprocess.CompletedProcess(args, proc.returncode, stdout=stdout, stderr=stderr)
    if check and cp.returncode:
        raise subprocess.CalledProcessError(cp.returncode, cp.args, stderr=stderr)
    return cp
