import pytest

from ixdiagnose.test.pytest.unit.utils import get_asset
from ixdiagnose.utils.run import run
from subprocess import CompletedProcess


ASSETS_FILENAME = "swapon_output.txt"


def test_run(mocker):
    mock_popen = mocker.patch("subprocess.Popen")
    stdout = get_asset(ASSETS_FILENAME)
    mock_popen.return_value.communicate.return_value = (stdout, "")
    mock_popen.return_value.returncode = 0
    result = run(["swapon", "-s"], check=False, env=None)
    assert result.__dict__ == CompletedProcess(("swapon", "-s"), 0, stdout=stdout, stderr="").__dict__


def test_run_timeout():
    result = run(["tail", "-f", "/dev/null"], check=False, timeout=2)
    assert result.stderr is not None


def test_run_list_is_not_shell_parsed():
    result = run(["echo", "$(echo injected); `echo injected`"])
    assert result.stdout == "$(echo injected); `echo injected`\n"


def test_run_shell():
    assert run("echo $((1 + 2)) | tr 3 4", shell=True).stdout == "4\n"


@pytest.mark.parametrize("cmd,shell", [("echo hi", False), (["echo", "hi"], True)])
def test_run_shell_must_match_type(mocker, cmd, shell):
    mock_popen = mocker.patch("subprocess.Popen")
    with pytest.raises(TypeError, match="shell=True"):
        run(cmd, shell=shell)
    mock_popen.assert_not_called()
