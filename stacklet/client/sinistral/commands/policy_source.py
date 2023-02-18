from stacklet.client.sinistral.utils import default_options, click_group_entry
from stacklet.client.sinistral.executor import make_request

import click


@click.group(short_help="Policy sources command")
@default_options()
@click.pass_context
def policy_sources(*args, **kwargs):
    click_group_entry(*args, **kwargs)


def _list(ctx, raw=True):
    return make_request(ctx, "get", "/policy-sources", raw=raw)


@policy_sources.command()
@click.pass_context
def list(ctx, *args, **kwargs):
    click.echo(_list(ctx, raw=False))
