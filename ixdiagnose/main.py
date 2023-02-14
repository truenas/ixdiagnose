import click

from .config import conf
from .plugin import generate_plugins_debug


@click.group()
@click.option('--debug-path')
@click.pass_context
def cli(ctx, debug_path):
    ctx.ensure_object(dict)
    ctx.obj['debug_path'] = debug_path
    conf.debug_path = debug_path


@cli.command()
@click.pass_context
def run(ctx):
    click.echo('Generating debug of plugins')
    generate_plugins_debug()


@cli.command()
@click.option('--debug/--no-debug', default=False)
def debug(debug):
    # PluginFactory()
    click.echo('Debug')


def main():
    cli(obj={})
