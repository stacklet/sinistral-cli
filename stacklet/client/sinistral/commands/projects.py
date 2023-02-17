from stacklet.client.sinistral.utils import default_options, click_group_entry
from stacklet.client.sinistral.executor import make_request

import click


@click.group(short_help='Projects command')
@default_options()
@click.pass_context
def projects(*args, **kwargs):
    click_group_entry(*args, **kwargs)


@projects.command()
@click.pass_context
def get(ctx, *args, **kwargs):
    click.echo(make_request(ctx, 'get', '/projects',))
