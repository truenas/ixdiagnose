import click


@click.group()
def cli():
    pass


@cli.command()
def run():
    # PluginFactory()
    click.echo('Syncing')


@cli.command()
@click.option('--debug/--no-debug', default=False)
def debug(debug):
    # PluginFactory()
    click.echo('Debug')


def main():
    cli()
