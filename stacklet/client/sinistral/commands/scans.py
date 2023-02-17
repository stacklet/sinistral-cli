from stacklet.client.sinistral.utils import default_options, click_group_entry
from stacklet.client.sinistral.executor import make_request

import click


@click.group(short_help='Scans command')
@default_options()
@click.pass_context
def scans(*args, **kwargs):
    click_group_entry(*args, **kwargs)


@scans.command()
@click.pass_context
def get(ctx, *args, **kwargs):
    click.echo(make_request(ctx, 'get', '/scans',))
