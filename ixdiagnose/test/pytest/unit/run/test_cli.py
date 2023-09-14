import pytest

from click.testing import CliRunner
from ixdiagnose.cli import main
from ixdiagnose.config import conf

runner = CliRunner()


@pytest.fixture
def cli():
    return runner.invoke(main)


@pytest.fixture(autouse=True)
def reset_config():
    conf.compress = False
    conf.compressed_path = None
    conf.clean_debug_path = False
    conf.debug_path = None
    conf.exclude_artifacts = []
    conf.exclude_plugins = []
    conf.structured_data = False
    conf.timeout = 20


def test_plugin_with_required_args(cli):
    result = runner.invoke(main, ['plugin', '--debug-path', '/tmp/debug'])
    assert result.exit_code == 0
    assert 'Generated plugins\' dump at /tmp/debug' in result.output


def test_plugin_without_debug_path(cli):
    result = runner.invoke(main, ['plugin'])
    assert result.exit_code == 2
    assert 'Missing option \'--debug-path\'' in result.output


def test_plugin_with_exclude_option(cli):
    result = runner.invoke(main, ['plugin', '--debug-path', '/tmp/debug', '-X', 'vm,network'])
    assert result.exit_code == 0
    assert 'exclude plugins: [\'vm\', \'network\']' in result.output
    assert 'Generated plugins\' dump at /tmp/debug' in result.output


def test_plugin_progressbar(cli):
    result = runner.invoke(main, ['plugin', '--debug-path', '/tmp/debug'])
    assert result.exit_code == 0
    assert 'Completed debug' in result.output


def test_artifact_with_required_args(cli):
    result = runner.invoke(main, ['artifact', '--debug-path', '/tmp/debug'])
    assert result.exit_code == 0
    assert 'Collected artifacts at /tmp/debug' in result.output


def test_artifact_without_debug_path(cli):
    result = runner.invoke(main, ['artifact'])
    assert result.exit_code == 2
    assert 'Missing option \'--debug-path\'' in result.output


def test_artifact_with_exclude_option(cli):
    result = runner.invoke(main, ['artifact', '--debug-path', '/tmp/debug', '-X', 'logs'])
    assert result.exit_code == 0
    assert 'exclude artifacts: [\'logs\']' in result.output
    assert 'Gathered artifact \'logs\'' not in result.output
    assert 'Collected artifacts at /tmp/debug' in result.output


def test_artifact_progressbar(cli):
    result = runner.invoke(main, ['artifact', '--debug-path', '/tmp/debug'])
    assert result.exit_code == 0
    assert 'Completed debug' in result.output


def test_artifact_with_no_exclude(cli):
    result = runner.invoke(main, ['artifact', '--debug-path', '/tmp/debug', '-X'])
    assert result.exit_code == 2
    assert 'Option \'-X\' requires an argument.' in result.output


def test_run_with_serialized(cli):
    result = runner.invoke(main, ['run', '-s'])
    assert result.exit_code == 0
    assert 'generate debug in structured form.' in result.output


def test_run_with_exclude_artifacts(cli):
    result = runner.invoke(main, ['run', '-Xa', 'logs,sys_info'])
    assert result.exit_code == 0
    assert 'exclude artifacts: [\'logs\', \'sys_info\']' in result.output


def test_run_command_custom_options(cli):
    result = runner.invoke(main, ['run', '-s', '-c', '-t', '5', '-Xa', 'logs,sys_info', '-Xp', 'vm,network'])
    assert result.exit_code == 0
    assert 'generate debug in structured form.' in result.output
    assert 'save debug as a compressed folder.' in result.output
    assert 'timeout for debug generation: 5 seconds.' in result.output
    assert 'exclude artifacts: [\'logs\', \'sys_info\']' in result.output
    assert 'exclude plugins: [\'vm\', \'network\']' in result.output
