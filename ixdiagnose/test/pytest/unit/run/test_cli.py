import pytest
import os

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
    conf.include_plugins = []
    conf.structured_data = False
    conf.timeout = 20

    yield

    if conf.compress:
        os.remove(conf.compressed_path)


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
    result = runner.invoke(
        main, [
            'run', '-s', '-c', '/tmp/compress', '--debug-path', '/tmp/debug',
            '-t', '5', '-Xa', 'logs,sys_info', '-Xp', 'vm,network'
        ]
    )
    assert result.exit_code == 0
    assert 'generate debug in structured form.' in result.output
    assert 'save debug as a compressed folder at: /tmp/compress' in result.output
    assert 'timeout for debug generation: 5 seconds.' in result.output
    assert 'debug path set to /tmp/debug' in result.output
    assert 'exclude artifacts: [\'logs\', \'sys_info\']' in result.output
    assert 'exclude plugins: [\'vm\', \'network\']' in result.output


def test_path_validation(cli):
    result = runner.invoke(main, ['run', '--debug-path', 'tmp/debug'])
    result2 = runner.invoke(main, ['run', '-c', 'tmp/compress'])
    assert result.exit_code == 2
    assert result2.exit_code == 2
    assert 'Path must be absolute' in result.output
    assert 'Path must be absolute' in result2.output


def test_plugin_with_include_option(cli):
    result = runner.invoke(main, ['plugin', '--debug-path', '/tmp/debug', '-I', 'apps,system'])
    assert result.exit_code == 0
    assert 'include plugins: [\'apps\', \'system\']' in result.output
    assert 'Generated plugins\' dump at /tmp/debug' in result.output


def test_plugin_mutual_exclusion_include_exclude(cli):
    result = runner.invoke(main, ['plugin', '--debug-path', '/tmp/debug', '-X', 'vm', '-I', 'apps'])
    assert result.exit_code == 2
    assert 'Cannot use both --exclude and --include at the same time' in result.output


def test_run_with_include_plugins(cli):
    result = runner.invoke(main, ['run', '-Ip', 'apps,system'])
    assert result.exit_code == 0
    assert 'include plugins: [\'apps\', \'system\']' in result.output


def test_run_mutual_exclusion_include_exclude_plugins(cli):
    result = runner.invoke(main, ['run', '-Xp', 'vm', '-Ip', 'apps'])
    assert result.exit_code == 2
    assert 'Cannot use both --exclude-plugins and --include-plugins at the same time' in result.output


def test_run_include_plugins_with_other_options(cli):
    result = runner.invoke(
        main, [
            'run', '-s', '--debug-path', '/tmp/debug',
            '-t', '5', '-Xa', 'logs', '-Ip', 'apps,system'
        ]
    )
    assert result.exit_code == 0
    assert 'generate debug in structured form.' in result.output
    assert 'timeout for debug generation: 5 seconds.' in result.output
    assert 'debug path set to /tmp/debug' in result.output
    assert 'exclude artifacts: [\'logs\']' in result.output
    assert 'include plugins: [\'apps\', \'system\']' in result.output


def test_plugin_with_no_include_argument(cli):
    result = runner.invoke(main, ['plugin', '--debug-path', '/tmp/debug', '-I'])
    assert result.exit_code == 2
    assert 'Option \'-I\' requires an argument.' in result.output


def test_run_with_no_include_plugins_argument(cli):
    result = runner.invoke(main, ['run', '-Ip'])
    assert result.exit_code == 2
    assert 'Option \'-Ip\' requires an argument.' in result.output
