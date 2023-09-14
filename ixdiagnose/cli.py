import click

from ixdiagnose.event import event_callbacks
from typing import Callable, List, Optional

from .artifact import gather_artifacts
from .config import conf
from .plugin import generate_plugins_debug
from .run import generate_debug


text = ['Specified configuration for debug generation is ']


@click.group()
def main() -> None:
    pass


timeout_option = click.option(
    '-t', '--timeout', type=click.INT, default=20, show_default=True,
    help='timeout value in seconds'
)

debug_path_option = click.option(
    '--debug-path', type=click.Path(), required=True,  help='path where you want to save debug'
)


def list_type(values: str) -> List[str]:
    return [value.strip() for value in values.split(',')]


def update_configuration(
    timeout: int, compress: Optional[bool] = None, debug_path: Optional[str] = None,
    excluded_artifacts: Optional[List[str]] = None, excluded_plugins: Optional[List[str]] = None,
) -> None:
    if compress:
        conf.compress = True
        text.append('- save debug as a compressed folder.')

    if timeout:
        conf.timeout = timeout
        text.append(f'- timeout for debug generation: {timeout} seconds.')

    if excluded_artifacts:
        conf.exclude_artifacts = excluded_artifacts
        text.append(f'- exclude artifacts: {excluded_artifacts}')

    if excluded_plugins:
        conf.exclude_plugins = excluded_plugins
        text.append(f'- exclude plugins: {excluded_plugins}')

    if debug_path:
        conf.debug_path = debug_path
        text.append(f'- debug path set to {debug_path}')


def progress_bar(func: Callable) -> str:
    bar = click.progressbar(length=100, label='Generating debug')
    cumulative_progress = 0
    last_iteration_label = 'Completed debug'

    def callback(progress, desc):
        nonlocal cumulative_progress
        progress -= cumulative_progress
        cumulative_progress += progress
        if cumulative_progress == 100:
            bar.label = last_iteration_label
        else:
            bar.label = desc
        bar.update(progress)

    with bar:
        event_callbacks.register(callback)
        path = func()

    return path


@main.command(short_help='Generate complete debug')
@click.option('-s', '--serialized', is_flag=True, default=False, help='generate debug in structured form')
@click.option('-c', '--compress', is_flag=True, default=False, help='get compressed debug')
@timeout_option
@click.option(
    '-Xa', '--exclude-artifacts', type=list_type,
    help='artifacts you want to exclude in debug (logs,sys_info). A comma separated list without space or in quotes'
)
@click.option(
    '-Xp', '--exclude-plugins', type=list_type,
    help='plugins you want to exclude in debug (smb,vm,network). A comma separated list without space or in quotes'
)
def run(
    serialized: bool, compress: bool, timeout: int, exclude_artifacts: List[str],
    exclude_plugins: List[str]
) -> None:
    if serialized:
        conf.structured_data = True
        text.append('- generate debug in structured form.')
    else:
        text.append('- generate debug in default non-structured form.')

    update_configuration(timeout, compress, None, exclude_artifacts, exclude_plugins)

    click.echo('\n'.join(text))
    path = progress_bar(generate_debug)
    click.echo(f'Debug saved at {path}')


@main.command(short_help='Gather artifacts')
@debug_path_option
@timeout_option
@click.option(
    '-X', '--exclude', type=list_type,
    help='artifacts you want to exclude in debug (logs,sys_info). A comma separated list without space or in quotes'
)
def artifact(debug_path: str, timeout: int, exclude: List[str]) -> None:
    update_configuration(timeout, debug_path=debug_path, excluded_artifacts=exclude)

    click.echo('\n'.join(text))
    progress_bar(gather_artifacts)
    click.echo(f'Collected artifacts at {debug_path}')


@main.command(short_help='Generate plugins\' debug')
@debug_path_option
@timeout_option
@click.option(
    '-X', '--exclude', type=list_type,
    help='plugins you want to exclude in debug (smb,vm,network). A comma separated list without space or in quotes'
)
def plugin(debug_path: str, timeout: int, exclude: List[str]) -> None:
    update_configuration(timeout, debug_path=debug_path, excluded_plugins=exclude)

    click.echo('\n'.join(text))
    progress_bar(generate_plugins_debug)
    click.echo(f'Generated plugins\' dump at {debug_path}')
