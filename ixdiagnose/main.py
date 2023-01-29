import click

from .plugins.factory import PluginFactory


@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    click.echo(f"Debug mode is {'on' if debug else 'off'}")


@cli.command()
def ixdiagnose():
    # PluginFactory()
    click.echo('Syncing')
