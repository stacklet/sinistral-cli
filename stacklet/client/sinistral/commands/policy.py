from stacklet.client.sinistral.utils import default_options, click_group_entry
from stacklet.client.sinistral.executor import make_request

import click


@click.group(short_help='Policy command')
@default_options()
@click.pass_context
def policies(*args, **kwargs):
    click_group_entry(*args, **kwargs)


def _list(ctx, raw=True):
    return make_request(ctx, 'get', '/policies', raw=raw)


@policies.command()
@click.pass_context
def list(ctx, *args, **kwargs):
    click.echo(_list(ctx, raw=False))
