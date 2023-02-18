from stacklet.client.sinistral.utils import default_options, click_group_entry
from stacklet.client.sinistral.executor import make_request

import click


@click.group(short_help="Policy Collections command")
@default_options()
@click.pass_context
def policy_collections(*args, **kwargs):
    click_group_entry(*args, **kwargs)


def _list(ctx, raw=True):
    return make_request(ctx, "get", "/policy-collections", raw=raw)


@policy_collections.command()
@click.pass_context
def list(ctx, *args, **kwargs):
    click.echo(_list(ctx, raw=False))


def _get(ctx, name, raw=True):
    return make_request(ctx, "get", f"/policy-collections/{name}", raw=raw)


@policy_collections.command()
@click.option("--name", required=True)
@click.pass_context
def get(ctx, *args, **kwargs):
    click.echo(_get(ctx, kwargs["name"], raw=False))


def _get_policies(ctx, name, raw=True):
    return make_request(ctx, "get", f"/policy-collections/{name}/policies", raw=raw)


@policy_collections.command()
@click.option("--name", required=True)
@click.pass_context
def get_policies(ctx, *args, **kwargs):
    click.echo(_get_policies(ctx, kwargs["name"], raw=False))
